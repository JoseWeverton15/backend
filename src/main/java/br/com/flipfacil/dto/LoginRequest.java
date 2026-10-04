package br.com.flipfacil.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.Getter;
import lombok.Setter;

@Getter 
@Setter 
public class LoginRequest {
    @NotBlank
    @Email(message = "Email inválido")
    private String email;
    
    @NotBlank
    private String senha;
}
