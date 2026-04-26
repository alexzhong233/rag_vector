package com.rag.dto;

import lombok.Data;

@Data
public class ConfigUpdateRequest {
    private String configKey;
    private String configValue;
    private String description;
}
