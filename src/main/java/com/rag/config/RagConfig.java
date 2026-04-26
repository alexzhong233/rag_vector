package com.rag.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Component
@ConfigurationProperties(prefix = "rag")
public class RagConfig {
    private Integer chunkSize = 1000;
    private Integer chunkOverlap = 200;
    private Integer topK = 5;
}
