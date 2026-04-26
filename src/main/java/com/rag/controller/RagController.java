package com.rag.controller;

import com.rag.dto.RagQueryRequest;
import com.rag.dto.RagQueryResponse;
import com.rag.service.RagService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/rag")
@CrossOrigin(origins = "*")
public class RagController {

    private final RagService ragService;

    public RagController(RagService ragService) {
        this.ragService = ragService;
    }

    @PostMapping("/query")
    public ResponseEntity<RagQueryResponse> query(@RequestBody RagQueryRequest request) {
        RagQueryResponse response = ragService.query(request.getQuery(), request.getTopK());
        return ResponseEntity.ok(response);
    }
}
