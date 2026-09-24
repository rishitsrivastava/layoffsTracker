package com.layoffsindia.backend.repository;

import com.layoffsindia.backend.entity.Layoff;
import org.springframework.data.jpa.repository.JpaRepository;

public interface LayoffRepository extends JpaRepository<Layoff, Long> {
}