package br.com.flipfacil.controller;

import org.springframework.web.bind.annotation.RestController;
import jakarta.validation.Valid;

import br.com.flipfacil.service.AuthService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import br.com.flipfacil.dto.LoginRequest;
import br.com.flipfacil.dto.RegisterRequest;
import br.com.flipfacil.dto.AuthResponse;

@RestController
@RequestMapping("/auth")
public class AuthController {
    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register") 
    public String register(@Valid @RequestBody RegisterRequest registerRequest){
        authService.registerUser(registerRequest);
        return "User registered successfully";
    }

    @PostMapping("/login")
    public AuthResponse login(@Valid @RequestBody LoginRequest loginRequest) {
        String token = authService.authenticateUser(loginRequest);
        AuthResponse authResponse = new AuthResponse();
        authResponse.setToken(token);
        return authResponse;
    }
}
