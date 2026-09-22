package com.layoffsindia.backend.entity;

import jakarta.persistence.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "layoffs")
public class Layoff {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @Column(name = "company_name", nullable = false)
    private String companyName;

    @Column(name = "employees_affected")
    private Integer employeesAffected;

    @Column(name = "sources", columnDefinition = "text[]")
    private List<String> sources;

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


    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }public LocalDateTime getCreatedAt() {
        return createdAt;
    }public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }public String getVerificationStatus() {
        return verificationStatus;
    }public void setVerificationStatus(String verificationStatus) {
        this.verificationStatus = verificationStatus;
    }public String getReason() {
        return reason;
    }public void setReason(String reason) {
        this.reason = reason;
    }public LocalDate getLayoffDate() {
        return layoffDate;
    }public void setLayoffDate(LocalDate layoffDate) {
        this.layoffDate = layoffDate;
    }public String getHeadquarters() {
        return headquarters;
    }public void setHeadquarters(String headquarters) {
        this.headquarters = headquarters;
    }public String getLocation() {
        return location;
    }public void setLocation(String location) {
        this.location = location;
    }public String getCountry() {
        return country;
    }public void setCountry(String country) {
        this.country = country;
    }public List<String> getSources() {
        return sources;
    }public void setSources(List<String> sources) {
        this.sources = sources;
    }public Integer getEmployeesAffected() {
        return employeesAffected;
    }public void setEmployeesAffected(Integer employeesAffected) {
        this.employeesAffected = employeesAffected;
    }public String getCompanyName() {
        return companyName;
    }public void setCompanyName(String companyName) {
        this.companyName = companyName;
    }public long getId() {
        return id;
    }public void setId(long id) {
        this.id = id;
    }
}