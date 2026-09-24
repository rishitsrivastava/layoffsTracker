package com.layoffsindia.backend.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "layoffs")
@Getter
@Setter
public class Layoff {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @Column(name = "company_name", nullable = false)
    private String companyName;

    @Column(name = "employees_affected")
    private Integer employeesAffected;

    @Column(name = "sources", columnDefinition = "text[]")
    private String[] sources;

    @Column(name = "country", nullable = false)
    private String country;

    @Column(name = "location")
    private String location;

    @Column(name = "headquarters")
    private String headquarters;

    @Column(name = "layoff_date")
    private LocalDate layoffDate;

    @Column(name = "reason")
    private String reason;

    @Column(name = "verification_status", nullable = false)
    private String verificationStatus;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        LocalDateTime now = LocalDateTime.now();
        createdAt = now;
        updatedAt = now;
    }

    @PreUpdate
    protected void onUpdate() {
        LocalDateTime now = LocalDateTime.now();
        updatedAt = now;
    }

}