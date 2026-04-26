package com.rag.controller;

import com.rag.dto.ConfigUpdateRequest;
import com.rag.entity.SystemConfig;
import com.rag.service.ConfigService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/config")
@CrossOrigin(origins = "*")
public class ConfigController {

    private final ConfigService configService;

    public ConfigController(ConfigService configService) {
        this.configService = configService;
    }

    @GetMapping
    public ResponseEntity<List<SystemConfig>> getAllConfigs() {
        return ResponseEntity.ok(configService.getAllConfigs());
    }

    @GetMapping("/{configKey}")
    public ResponseEntity<SystemConfig> getConfigByKey(@PathVariable String configKey) {
        return configService.getConfigByKey(configKey)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PutMapping
    public ResponseEntity<SystemConfig> updateConfig(@RequestBody ConfigUpdateRequest request) {
        SystemConfig config = configService.updateConfig(
                request.getConfigKey(),
                request.getConfigValue(),
                request.getDescription()
        );
        return ResponseEntity.ok(config);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteConfig(@PathVariable UUID id) {
        configService.deleteConfig(id);
        return ResponseEntity.noContent().build();
    }
}
