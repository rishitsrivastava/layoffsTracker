package com.layoffsindia.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public class LayoffMapResponse {

    private Long id;
    private String companyName;
    private Integer employeesAffected;
    private String location;
    private String locationStatus;
    private Double latitude;
    private Double longitude;
}
