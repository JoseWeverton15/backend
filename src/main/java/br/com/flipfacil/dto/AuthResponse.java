package br.com.flipfacil.dto;

import lombok.Setter;
import lombok.Getter;

@Getter
@Setter 
public class AuthResponse{
    private String token;
    private String type = "Bearer";
}