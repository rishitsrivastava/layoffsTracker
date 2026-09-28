package com.layoffsindia.backend.dto;

import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;

@Getter
@Setter
public class LayoffRequest {

    private String companyName;
    private Integer employeesAffected;
    private String[] sources;
    private String country;
    private String location;
    private String headquarters;
    private LocalDate layoffDate;
    private String reason;
    private String verificationStatus;
}
