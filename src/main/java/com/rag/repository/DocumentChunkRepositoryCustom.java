package com.rag.repository;

import java.util.List;
import java.util.UUID;

public interface DocumentChunkRepositoryCustom {
    List<Object[]> findSimilarChunks(float[] embedding, int topK);
}
