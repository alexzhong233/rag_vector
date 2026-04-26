package com.rag.service;

import com.rag.config.RagConfig;
import com.rag.dto.RagQueryResponse;
import com.rag.repository.DocumentChunkRepository;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class RagService {

    private final DocumentChunkRepository documentChunkRepository;
    private final EmbeddingService embeddingService;
    private final LLMService llmService;
    private final RagConfig ragConfig;

    public RagService(DocumentChunkRepository documentChunkRepository,
                      EmbeddingService embeddingService,
                      LLMService llmService,
                      RagConfig ragConfig) {
        this.documentChunkRepository = documentChunkRepository;
        this.embeddingService = embeddingService;
        this.llmService = llmService;
        this.ragConfig = ragConfig;
    }

    public RagQueryResponse query(String query, Integer topKParam) {
        int topK = topKParam != null ? topKParam : ragConfig.getTopK();

        float[] queryEmbedding = embeddingService.generateEmbedding(query);
        List<Object[]> similarChunks = documentChunkRepository.findSimilarChunks(queryEmbedding, topK);

        List<RagQueryResponse.DocumentChunkInfo> sources = new ArrayList<>();
        StringBuilder contextBuilder = new StringBuilder();

        for (Object[] row : similarChunks) {
            String content = (String) row[1];
            Integer chunkIndex = (Integer) row[2];
            String documentTitle = (String) row[4];
            String fileName = (String) row[5];
            Double similarity = ((Number) row[6]).doubleValue();

            sources.add(new RagQueryResponse.DocumentChunkInfo(
                    content, documentTitle, fileName, chunkIndex, similarity
            ));

            contextBuilder.append(content).append("\n\n");
        }

        String answer = llmService.generateRagResponse(query, contextBuilder.toString());

        return new RagQueryResponse(answer, sources);
    }
}
