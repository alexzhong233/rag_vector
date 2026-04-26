package com.rag.service;

import dev.langchain4j.model.chat.ChatLanguageModel;
import org.springframework.stereotype.Service;

@Service
public class LLMService {

    private final ChatLanguageModel chatLanguageModel;

    public LLMService(ChatLanguageModel chatLanguageModel) {
        this.chatLanguageModel = chatLanguageModel;
    }

    public String generateResponse(String prompt) {
        return chatLanguageModel.generate(prompt);
    }

    public String generateRagResponse(String query, String context) {
        String prompt = String.format("""
            你是一个有用的AI助手。请根据以下提供的上下文信息回答用户的问题。
            
            上下文信息：
            %s
            
            用户问题：
            %s
            
            如果上下文中没有足够的信息来回答问题，请诚实地说明。请基于上下文信息给出清晰、准确的回答。
            """, context, query);

        return chatLanguageModel.generate(prompt);
    }
}
