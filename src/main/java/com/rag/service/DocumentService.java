package com.rag.service;

import com.rag.entity.Document;
import com.rag.repository.DocumentChunkRepository;
import com.rag.repository.DocumentRepository;
import jakarta.transaction.Transactional;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class DocumentService {

    private final DocumentRepository documentRepository;
    private final DocumentChunkRepository documentChunkRepository;
    private final AgenticRAGService agenticRAGService;

    public DocumentService(DocumentRepository documentRepository,
                           DocumentChunkRepository documentChunkRepository,
                           AgenticRAGService agenticRAGService) {
        this.documentRepository = documentRepository;
        this.documentChunkRepository = documentChunkRepository;
        this.agenticRAGService = agenticRAGService;
    }

    public List<Document> getAllDocuments() {
        return documentRepository.findAll();
    }

    public Optional<Document> getDocumentById(UUID id) {
        return documentRepository.findById(id);
    }

    @Transactional
    public Document uploadDocument(MultipartFile file, String title) throws IOException {
        String fileName = file.getOriginalFilename();
        String fileType = file.getContentType();
        Long fileSize = file.getSize();

        String uploadDir = "uploads";
        Path uploadPath = Paths.get(uploadDir);
        if (!Files.exists(uploadPath)) {
            Files.createDirectories(uploadPath);
        }

        String uniqueFileName = UUID.randomUUID() + "_" + fileName;
        Path filePath = uploadPath.resolve(uniqueFileName);
        Files.copy(file.getInputStream(), filePath);

        Document document = new Document();
        document.setTitle(title != null ? title : fileName);
        document.setFileName(fileName);
        document.setFilePath(filePath.toString());
        document.setFileType(fileType);
        document.setFileSize(fileSize);

        Document savedDocument = documentRepository.save(document);

        processDocumentAsync(savedDocument);

        return savedDocument;
    }

    private void processDocumentAsync(Document document) {
        new Thread(() -> {
            try {
                String content = extractTextFromFile(document.getFilePath());
                agenticRAGService.processAndSaveChunks(document.getId(), content);
                document.setProcessed(true);
                documentRepository.save(document);
            } catch (Exception e) {
                document.setProcessed(false);
                document.setProcessingError(e.getMessage());
                documentRepository.save(document);
            }
        }).start();
    }

    private String extractTextFromFile(String filePath) throws IOException {
        File file = new File(filePath);
        if (filePath.toLowerCase().endsWith(".pdf")) {
            try (PDDocument pdDocument = PDDocument.load(file)) {
                PDFTextStripper stripper = new PDFTextStripper();
                return stripper.getText(pdDocument);
            }
        } else {
            return Files.readString(Path.of(filePath));
        }
    }

    @Transactional
    public void deleteDocument(UUID id) {
        documentChunkRepository.deleteByDocumentId(id);
        documentRepository.deleteById(id);
    }
}
