package br.com.flipfacil.service;

import java.math.BigDecimal;
import java.util.List;

import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;

import br.com.flipfacil.dto.FiltroAnuncioRequest;
import br.com.flipfacil.entity.Anuncio;
import br.com.flipfacil.repository.AnuncioRepository;
import br.com.flipfacil.repository.AnuncioSpecification;

@Service
public class AnuncioService {

    private final AnuncioRepository anuncioRepository;

    public AnuncioService(AnuncioRepository anuncioRepository) {
        this.anuncioRepository = anuncioRepository;
    }

    public List<Anuncio> filtrarAnuncios(FiltroAnuncioRequest filtro) {
        Specification<Anuncio> specification =
                AnuncioSpecification.tituloContains(filtro.getTitulo())
                        .and(AnuncioSpecification.descricaoContains(filtro.getDescricao()))
                        .and(AnuncioSpecification.precoGreaterThanOrEqualTo(
                                filtro.getPrecoMinimo() == null
                                        ? null
                                        : BigDecimal.valueOf(filtro.getPrecoMinimo())))
                        .and(AnuncioSpecification.precoLessThanOrEqualTo(
                                filtro.getPrecoMaximo() == null
                                        ? null
                                        : BigDecimal.valueOf(filtro.getPrecoMaximo())))
                        .and(AnuncioSpecification.categoriaEquals(filtro.getCategoria()))
                        .and(AnuncioSpecification.cidadeEquals(filtro.getCidade()))
                        .and(AnuncioSpecification.estadoEquals(filtro.getEstado()));

        return anuncioRepository.findAll(specification);
    }
}