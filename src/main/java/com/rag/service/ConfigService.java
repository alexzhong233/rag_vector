package com.rag.service;

import com.rag.entity.SystemConfig;
import com.rag.repository.SystemConfigRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class ConfigService {

    private final SystemConfigRepository systemConfigRepository;

    public ConfigService(SystemConfigRepository systemConfigRepository) {
        this.systemConfigRepository = systemConfigRepository;
    }

    public List<SystemConfig> getAllConfigs() {
        return systemConfigRepository.findAll();
    }

    public Optional<SystemConfig> getConfigByKey(String configKey) {
        return systemConfigRepository.findByConfigKey(configKey);
    }

    public SystemConfig updateConfig(String configKey, String configValue, String description) {
        SystemConfig config = systemConfigRepository.findByConfigKey(configKey)
                .orElseGet(() -> {
                    SystemConfig newConfig = new SystemConfig();
                    newConfig.setConfigKey(configKey);
                    return newConfig;
                });

        config.setConfigValue(configValue);
        if (description != null) {
            config.setDescription(description);
        }

        return systemConfigRepository.save(config);
    }

    public void deleteConfig(UUID id) {
        systemConfigRepository.deleteById(id);
    }
}
