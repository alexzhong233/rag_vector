package com.rag.repository;

import com.pgvector.PGvector;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public class DocumentChunkRepositoryImpl implements DocumentChunkRepositoryCustom {

    @PersistenceContext
    private EntityManager entityManager;

    @Override
    public List<Object[]> findSimilarChunks(float[] embedding, int topK) {
        String sql = """
            SELECT dc.id, dc.content, dc.chunk_index, dc.document_id,
                   d.title, d.file_name,
                   1 - (dc.embedding <-> :embedding) as similarity
            FROM document_chunks dc
            JOIN documents d ON dc.document_id = d.id
            ORDER BY dc.embedding <-> :embedding
            LIMIT :topK
            """;

        Query query = entityManager.createNativeQuery(sql);
        query.setParameter("embedding", new PGvector(embedding));
        query.setParameter("topK", topK);

        return query.getResultList();
    }
}
