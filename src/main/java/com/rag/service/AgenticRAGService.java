package com.rag.service;

import com.rag.config.RagConfig;
import com.rag.entity.DocumentChunk;
import com.rag.repository.DocumentChunkRepository;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
public class AgenticRAGService {

    private final DocumentChunkRepository documentChunkRepository;
    private final EmbeddingService embeddingService;
    private final RagConfig ragConfig;

    public AgenticRAGService(DocumentChunkRepository documentChunkRepository,
                             EmbeddingService embeddingService,
                             RagConfig ragConfig) {
        this.documentChunkRepository = documentChunkRepository;
        this.embeddingService = embeddingService;
        this.ragConfig = ragConfig;
    }

    @Transactional
    public void processAndSaveChunks(UUID documentId, String content) {
        List<String> chunks = splitIntoChunks(content);

        for (int i = 0; i < chunks.size(); i++) {
            String chunkContent = chunks.get(i);
            float[] embedding = embeddingService.generateEmbedding(chunkContent);

            DocumentChunk chunk = new DocumentChunk();
            chunk.setDocumentId(documentId);
            chunk.setContent(chunkContent);
            chunk.setChunkIndex(i);
            chunk.setEmbedding(embedding);

            documentChunkRepository.save(chunk);
        }
    }

    private List<String> splitIntoChunks(String content) {
        List<String> chunks = new ArrayList<>();
        int chunkSize = ragConfig.getChunkSize();
        int chunkOverlap = ragConfig.getChunkOverlap();

        int index = 0;
        while (index < content.length()) {
            int end = Math.min(index + chunkSize, content.length());
            
            if (end < content.length()) {
                int lastSpace = content.lastIndexOf(' ', end);
                if (lastSpace > index) {
                    end = lastSpace;
                }
            }

            String chunk = content.substring(index, end).trim();
            if (!chunk.isEmpty()) {
                chunks.add(chunk);
            }

            index = end - chunkOverlap;
            if (index < 0) index = 0;
        }

        return chunks;
    }
}
