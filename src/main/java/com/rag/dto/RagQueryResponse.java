package com.rag.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RagQueryResponse {
    private String answer;
    private List<DocumentChunkInfo> sources;

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class DocumentChunkInfo {
        private String content;
        private String documentTitle;
        private String fileName;
        private Integer chunkIndex;
        private Double similarity;
    }
}
