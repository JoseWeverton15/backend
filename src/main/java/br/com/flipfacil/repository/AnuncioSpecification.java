package br.com.flipfacil.repository;

import java.math.BigDecimal;
import java.util.Locale;

import org.springframework.data.jpa.domain.Specification;

import br.com.flipfacil.entity.Anuncio;

public class AnuncioSpecification {

    public static Specification<Anuncio> tituloContains(String titulo) {
        if (titulo == null || titulo.isBlank()) {
            return Specification.unrestricted();
        }

        String texto = titulo.toLowerCase(Locale.ROOT);

        return (root, query, criteriaBuilder) ->
                criteriaBuilder.like(
                        criteriaBuilder.lower(root.get("titulo")),
                        "%" + texto + "%"
                );
    }

    public static Specification<Anuncio> descricaoContains(String descricao) {
        if (descricao == null || descricao.isBlank()) {
            return Specification.unrestricted();
        }

        String texto = descricao.toLowerCase(Locale.ROOT);

        return (root, query, criteriaBuilder) ->
                criteriaBuilder.like(
                        criteriaBuilder.lower(root.get("descricao")),
                        "%" + texto + "%"
                );
    }

    public static Specification<Anuncio> precoGreaterThanOrEqualTo(
            BigDecimal precoMinimo) {
        if (precoMinimo == null) {
            return Specification.unrestricted();
        }

        return (root, query, criteriaBuilder) ->
                criteriaBuilder.greaterThanOrEqualTo(
                        root.get("preco"), precoMinimo
                );
    }

    public static Specification<Anuncio> precoLessThanOrEqualTo(
            BigDecimal precoMaximo) {
        if (precoMaximo == null) {
            return Specification.unrestricted();
        }

        return (root, query, criteriaBuilder) ->
                criteriaBuilder.lessThanOrEqualTo(
                        root.get("preco"), precoMaximo
                );
    }

    
    public static Specification<Anuncio> categoriaEquals(String categoria) {
        if (categoria == null || categoria.isBlank()) {
            return Specification.unrestricted();
        }

        String texto = categoria.toLowerCase(Locale.ROOT);

        return (root, query, criteriaBuilder) ->
                criteriaBuilder.equal(
                        criteriaBuilder.function(
                                "unaccent",
                                String.class,
                                criteriaBuilder.lower(root.get("categoria"))
                        ),
                        criteriaBuilder.function(
                                "unaccent",
                                String.class,
                                criteriaBuilder.literal(texto)
                        )
                );
    }

    public static Specification<Anuncio> cidadeEquals(String cidade) {
        if (cidade == null || cidade.isBlank()) {
            return Specification.unrestricted();
        }

        String texto = cidade.toLowerCase(Locale.ROOT);

        return (root, query, criteriaBuilder) ->
                criteriaBuilder.equal(
                        criteriaBuilder.lower(root.get("cidade")),
                        texto
                );
    }

    public static Specification<Anuncio> estadoEquals(String estado) {
        if (estado == null || estado.isBlank()) {
            return Specification.unrestricted();
        }

        String texto = estado.toLowerCase(Locale.ROOT);

        return (root, query, criteriaBuilder) ->
                criteriaBuilder.equal(
                        criteriaBuilder.lower(root.get("estado")),
                        texto
                );
    }

    public static Specification<Anuncio> notaGreaterThanOrEqualTo(Double notaMinima) {
        if (notaMinima == null) {
            return Specification.unrestricted();
        }

        return (root, query, criteriaBuilder) ->
                criteriaBuilder.greaterThanOrEqualTo(
                        root.get("pontuacaoPreliminar"), notaMinima
                );
    }
}