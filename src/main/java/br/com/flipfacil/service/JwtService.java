package br.com.flipfacil.service;

import java.nio.charset.StandardCharsets;
import java.util.Date;

import javax.crypto.SecretKey;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;

@Service
public class JwtService {

    private final String secretString;
    private final SecretKey secretKey;

    public JwtService(@Value("${jwt.secret}") String secretString) {
        this.secretString = secretString;
        this.secretKey = Keys.hmacShaKeyFor(this.secretString.getBytes(StandardCharsets.UTF_8));
    }

    public String gerarToken(String username) {
        long tempoExpiracao = 3600000; // 1 hora em milissegundos

        return Jwts.builder()
                .subject(username) // Define o usuário (Subject)
                .issuedAt(new Date()) // Data de geração
                .expiration(new Date(System.currentTimeMillis() + tempoExpiracao)) // Expiração
                .signWith(secretKey) // Assina o token com a chave gerada
                .compact(); // Constrói e compacta para a String final do JWT
    }

    public String validar(String jwt) {
        try {
            return Jwts.parser()
                    .verifyWith(secretKey) // Define a chave para validação
                    .build()
                    .parseSignedClaims(jwt) // Analisa o JWT
                    .getPayload() // Obtém o corpo do token
                    .getSubject(); // Retorna o usuário (Subject)
        } catch (Exception e) {
            return null; // Retorna null se o token for inválido ou expirado
        }
    }
}
