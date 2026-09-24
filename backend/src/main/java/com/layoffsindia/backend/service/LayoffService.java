package com.layoffsindia.backend.service;


import com.layoffsindia.backend.entity.Layoff;
import com.layoffsindia.backend.repository.LayoffRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class LayoffService {

    private final LayoffRepository layoffRepository;

    public LayoffService(LayoffRepository layoffRepository) {
        this.layoffRepository = layoffRepository;
    }

    public Layoff createLayoff(Layoff layoff) {
        return layoffRepository.save(layoff);
    }

    public List<Layoff> getAllLayoffs() {
        return layoffRepository.findAll();
    }

    public Optional<Layoff> getLayoffById(Long id) {
        return layoffRepository.findById(id);
    }

    public void deleteLayoff(Long id) {
        layoffRepository.deleteById(id);
    }
}
