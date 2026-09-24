package com.layoffsindia.backend.controller;


import com.layoffsindia.backend.entity.Layoff;
import com.layoffsindia.backend.service.LayoffService;
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
    public ResponseEntity<Layoff> createLayoff(@RequestBody Layoff layoff) {
        Layoff createdLayoff = layoffService.createLayoff(layoff);
        return ResponseEntity.ok(createdLayoff);
    }

    @GetMapping
    public ResponseEntity<List<Layoff>> getAllLayoffs() {
        return ResponseEntity.ok(layoffService.getAllLayoffs());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Layoff> getLayoffById(@PathVariable Long id) {
        return layoffService.getLayoffById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
