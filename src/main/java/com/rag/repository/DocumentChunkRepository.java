package com.rag.repository;

import com.rag.entity.DocumentChunk;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface DocumentChunkRepository extends JpaRepository<DocumentChunk, UUID>, DocumentChunkRepositoryCustom {

    @Modifying
    @Query("DELETE FROM DocumentChunk dc WHERE dc.documentId = :documentId")
    void deleteByDocumentId(@Param("documentId") UUID documentId);

    @Query("SELECT dc FROM DocumentChunk dc WHERE dc.documentId = :documentId ORDER BY dc.chunkIndex ASC")
    List<DocumentChunk> findByDocumentIdOrderByChunkIndexAsc(@Param("documentId") UUID documentId);
}
