package com.rag.dto;

import lombok.Data;

@Data
public class RagQueryRequest {
    private String query;
    private Integer topK;
}
