package com.layoffsindia.backend.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;

@Getter
@Setter
public class LayoffRequest {

    @NotBlank(message = "Company name is required")
    private String companyName;

    @Positive(message = "Employees affected must be greater than 0")
    private Integer employeesAffected;

    private String[] sources;

    @NotBlank(message = "Country is required")
    private String country;

    private String location;
    private String headquarters;
    private LocalDate layoffDate;
    private String reason;
    private String verificationStatus;
}
