package br.com.flipfacil.entity;

import java.math.BigDecimal;

import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.PrePersist;
import jakarta.persistence.Table;

import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;

import lombok.Getter;
import lombok.Setter;

import jakarta.persistence.PreUpdate;

@Getter 
@Setter 
@Entity 
@Table(name = "anuncio") 
public class Anuncio {
    @Id 
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String titulo;
    private String descricao;
    private BigDecimal preco;
    private String url;
    private String marketplace;
    private String categoria;
    private String cidade;
    private String estado;
    private BigDecimal precoReferencia;
    private Double pontuacaoPreliminar;
    private LocalDateTime dataCriacao;
    private LocalDateTime dataAtualizacao;

    @PrePersist 
    public void atualizarDataCriacao() {
        dataCriacao = LocalDateTime.now();
        dataAtualizacao = LocalDateTime.now();
    }

    @PreUpdate
    public void atualizarDataAtualizacao() {
        dataAtualizacao = LocalDateTime.now();
    }
}
