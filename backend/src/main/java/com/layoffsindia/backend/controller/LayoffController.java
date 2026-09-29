package com.layoffsindia.backend.controller;


import com.layoffsindia.backend.dto.LayoffRequest;
import com.layoffsindia.backend.dto.LayoffResponse;
import com.layoffsindia.backend.entity.Layoff;
import com.layoffsindia.backend.service.LayoffService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/layoffs")
public class LayoffController {

    private final LayoffService layoffService;

    public LayoffController(LayoffService layoffService) {
        this.layoffService = layoffService;
    }

    @PostMapping
    public ResponseEntity<LayoffResponse> createLayoff(@Valid @RequestBody LayoffRequest layoff) {
        return ResponseEntity.ok(layoffService.createLayoff(layoff));
    }

    @GetMapping
    public ResponseEntity<List<LayoffResponse>> getAllLayoffs() {
        return ResponseEntity.ok(layoffService.getAllLayoffs());
    }

    @GetMapping("/{id}")
    public ResponseEntity<LayoffResponse> getLayoffById(@PathVariable Long id) {
        LayoffResponse response = layoffService.getLayoffById(id);
        if(response == null)
            return ResponseEntity.notFound().build();

        return ResponseEntity.ok(response);
    }
}
