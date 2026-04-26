package com.rag.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;
import java.util.UUID;

@Data
@Entity
@Table(name = "documents")
public class Document {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;

    @Column(nullable = false, length = 500)
    private String title;

    @Column(name = "file_name", nullable = false, length = 500)
    private String fileName;

    @Column(name = "file_path", length = 1000)
    private String filePath;

    @Column(name = "file_type", length = 100)
    private String fileType;

    @Column(name = "file_size")
    private Long fileSize;

    @Column(name = "upload_time")
    private LocalDateTime uploadTime;

    private Boolean processed = false;

    @Column(name = "processing_error", columnDefinition = "TEXT")
    private String processingError;

    @PrePersist
    protected void onCreate() {
        uploadTime = LocalDateTime.now();
        if (processed == null) {
            processed = false;
        }
    }
}
