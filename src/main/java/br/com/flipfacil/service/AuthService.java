package br.com.flipfacil.service;

import org.springframework.stereotype.Service;

import br.com.flipfacil.repository.UserRepository;

import org.springframework.security.crypto.password.PasswordEncoder;

import br.com.flipfacil.dto.RegisterRequest;

import br.com.flipfacil.entity.User;

import br.com.flipfacil.dto.LoginRequest;

import br.com.flipfacil.exception.InvalidCredentialsException;

@Service 
public class AuthService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    public AuthService(UserRepository userRepository, PasswordEncoder passwordEncoder, JwtService jwtService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
    }

    public boolean isEmailRegistered(String email) {
        return userRepository.existsByEmail(email);
    }

    public void registerUser(RegisterRequest registerRequest) {
        if (isEmailRegistered(registerRequest.getEmail())) {
            throw new IllegalArgumentException("Email already registered");
        }
        User user = new User();
        user.setName(registerRequest.getName());
        user.setEmail(registerRequest.getEmail());
        user.setSenha(passwordEncoder.encode(registerRequest.getSenha()));
        userRepository.save(user);
    }
    public String authenticateUser(LoginRequest loginRequest){
        User user = userRepository.findByEmail(loginRequest.getEmail()).orElse(null);
        if (user == null) {
            throw new InvalidCredentialsException("Invalid username or password");
        }
        if (!user.getAtivo()) {
            throw new InvalidCredentialsException("Invalid username or password");
        }
        if (passwordEncoder.matches(loginRequest.getSenha(), user.getSenha())) {
            return jwtService.gerarToken(user.getEmail());
        }
        throw new InvalidCredentialsException("Invalid username or password");
    }
}
