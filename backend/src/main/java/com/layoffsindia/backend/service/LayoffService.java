package com.layoffsindia.backend.service;


import com.layoffsindia.backend.dto.LayoffRequest;
import com.layoffsindia.backend.dto.LayoffResponse;
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

    public LayoffResponse createLayoff(LayoffRequest request) {
        Layoff layoff = new Layoff();
        layoff.setCompanyName(request.getCompanyName());
        layoff.setEmployeesAffected(request.getEmployeesAffected());
        layoff.setSources(request.getSources());
        layoff.setCountry(request.getCountry());
        layoff.setLocation(request.getLocation());
        layoff.setHeadquarters(request.getHeadquarters());
        layoff.setLayoffDate(request.getLayoffDate());
        layoff.setReason(request.getReason());
        layoff.setVerificationStatus(request.getVerificationStatus());

        Layoff savedLayoff = layoffRepository.save(layoff);

        return toResponse(savedLayoff);
    }

    public List<LayoffResponse> getAllLayoffs() {
        return layoffRepository.findAll()
                .stream()
                .map(this::toResponse)
                .toList();
    }

    public LayoffResponse getLayoffById(Long id) {
        return layoffRepository.findById(id)
                .map(this::toResponse)
                .orElse(null);
    }

    public void deleteLayoff(Long id) {
        layoffRepository.deleteById(id);
    }

    private LayoffResponse toResponse(Layoff layoff) {

        LayoffResponse response = new LayoffResponse();

        response.setId(layoff.getId());
        response.setCompanyName(layoff.getCompanyName());
        response.setEmployeesAffected(layoff.getEmployeesAffected());
        response.setSources(layoff.getSources());
        response.setCountry(layoff.getCountry());
        response.setLocation(layoff.getLocation());
        response.setHeadquarters(layoff.getHeadquarters());
        response.setLayoffDate(layoff.getLayoffDate());
        response.setReason(layoff.getReason());
        response.setVerificationStatus(layoff.getVerificationStatus());
        response.setCreatedAt(layoff.getCreatedAt());
        response.setUpdatedAt(layoff.getUpdatedAt());

        return response;
    }
}
