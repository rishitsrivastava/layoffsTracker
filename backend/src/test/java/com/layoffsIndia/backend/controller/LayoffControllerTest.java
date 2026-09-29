package com.layoffsIndia.backend.controller;

import com.layoffsindia.backend.controller.LayoffController;
import tools.jackson.databind.ObjectMapper;
import com.layoffsindia.backend.dto.LayoffRequest;
import com.layoffsindia.backend.dto.LayoffResponse;
import com.layoffsindia.backend.service.LayoffService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;

import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;


@WebMvcTest(LayoffController.class)
class LayoffControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockitoBean
    private LayoffService layoffService;

    @Test
    void shouldCreateLayoff() throws Exception {

        LayoffResponse response = new LayoffResponse();

        response.setId(1L);
        response.setCompanyName("Example Company");
        response.setEmployeesAffected(100);
        response.setCountry("India");

        when(layoffService.createLayoff(any(LayoffRequest.class)))
                .thenReturn(response);

        LayoffRequest request = new LayoffRequest();

        request.setCompanyName("Example Company");
        request.setEmployeesAffected(100);
        request.setCountry("India");

        mockMvc.perform(post("/api/v1/layoffs")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.companyName")
                        .value("Example Company"))
                .andExpect(jsonPath("$.employeesAffected")
                        .value(100))
                .andExpect(jsonPath("$.country")
                        .value("India"));
    }

    @Test
    void shouldRejectInvalidLayoff() throws Exception {

        LayoffRequest request = new LayoffRequest();

        request.setCompanyName("");
        request.setEmployeesAffected(-100);
        request.setCountry("");

        mockMvc.perform(post("/api/v1/layoffs")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest());
    }

    @Test
    void shouldGetAllLayoffs() throws Exception {

        LayoffResponse response = new LayoffResponse();

        response.setId(1L);
        response.setCompanyName("Example Company");
        response.setCountry("India");

        when(layoffService.getAllLayoffs())
                .thenReturn(List.of(response));

        mockMvc.perform(get("/api/v1/layoffs"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].id").value(1))
                .andExpect(jsonPath("$[0].companyName")
                        .value("Example Company"));
    }
}