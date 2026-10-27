package com.layoffsindia.backend.service;


import com.layoffsindia.backend.dto.LayoffMapResponse;
import com.layoffsindia.backend.dto.LayoffRequest;
import com.layoffsindia.backend.dto.LayoffResponse;
import com.layoffsindia.backend.entity.Layoff;
import com.layoffsindia.backend.exception.ResourceNotFoundException;
import com.layoffsindia.backend.repository.LayoffRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Locale;
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
        layoff.setLatitude(request.getLatitude());
        layoff.setLongitude(request.getLongitude());
        layoff.setLocationStatus(request.getLocationStatus() == null ? "UNKNOWN" : request.getLocationStatus());

        Layoff savedLayoff = layoffRepository.save(layoff);
        System.out.println(savedLayoff);

        return toResponse(savedLayoff);
    }

    public List<LayoffResponse> getAllLayoffs() {
        return layoffRepository.findAll()
                .stream()
                .map(this::toResponse)
                .toList();
    }

    public LayoffResponse getLayoffById(Long id) {
        Layoff layoff = layoffRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Layoff not found: " + id)
                );

        return toResponse(layoff);
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
        response.setLocationStatus(layoff.getLocationStatus());
        response.setLatitude(layoff.getLatitude());
        response.setLongitude(layoff.getLongitude());
        response.setVerificationStatus(layoff.getVerificationStatus());
        response.setCreatedAt(layoff.getCreatedAt());
        response.setUpdatedAt(layoff.getUpdatedAt());

        return response;
    }

    public List<LayoffMapResponse> getLayoffsForMap() {
        return layoffRepository.findAll()
                .stream()
                .filter(layoff ->
                        layoff.getLatitude() != null
                        && layoff.getLongitude() != null
                )
                .map(layoff -> new LayoffMapResponse(
                        layoff.getId(),
                        layoff.getCompanyName(),
                        layoff.getEmployeesAffected(),
                        layoff.getLocation(),
                        layoff.getLocationStatus(),
                        layoff.getLatitude(),
                        layoff.getLongitude()
                ))
                .toList();
    }
}
