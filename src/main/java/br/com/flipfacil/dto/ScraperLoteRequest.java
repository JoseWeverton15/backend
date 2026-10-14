package br.com.flipfacil.dto;

import jakarta.validation.constraints.NotEmpty;
import lombok.Data;
import java.util.List;

@Data
public class ScraperLoteRequest {
    @NotEmpty(message = "A lista de links não pode estar vazia")
    private List<String> links;
}