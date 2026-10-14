package com.layoffsindia.backend.dto;

import jakarta.validation.constraints.*;
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

    @Pattern(
            regexp = "CONFIRMED|OFFICE_REFERENCE|UNKNOWN",
            message = "Invalid location status"
    )
    private String locationStatus;

    @DecimalMin("-180.0")
    @DecimalMax("180.0")
    private Double longitude;

    @DecimalMin("-90.0")
    @DecimalMax("90.0")
    private Double latitude;

    @AssertTrue(message = "Latitudde and longitude must be provided together")
    public boolean isCoordiantesPairValid() {
        return (latitude ==null && longitude ==null)
                || (latitude != null && longitude != null);
    }
}
