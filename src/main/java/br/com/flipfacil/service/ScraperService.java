package br.com.flipfacil.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;

import br.com.flipfacil.dto.ScraperLoteRequest;
import br.com.flipfacil.dto.ScraperLoteResponse;
import br.com.flipfacil.dto.ScraperPaginaRequest;
import br.com.flipfacil.dto.ScraperPaginaResponse;
import br.com.flipfacil.dto.ScraperRequest;
import br.com.flipfacil.dto.ScraperResponse;
import br.com.flipfacil.exception.ScraperException;

import java.util.concurrent.CompletableFuture;

@Service
public class ScraperService {

    private static final Logger log = LoggerFactory.getLogger(ScraperService.class);
    private final RestClient restClient;

    public ScraperService() {
        this.restClient = RestClient
                .builder()
                .baseUrl("http://localhost:5001") // Aponta para o Flask em Python
                .build();
    }

    // 1. Extração unitária de um anúncio 
    public ScraperResponse extrairAnuncio(ScraperRequest request) {
        try {
            return restClient
                    .post()
                    .uri("/api/scraper/anuncio") 
                    .body(request)
                    .retrieve()
                    .body(ScraperResponse.class);

        } catch (ResourceAccessException e) {
            log.error("Falha ao acessar o serviço de scraping para anúncio", e);
            throw new ScraperException("Serviço de scraping temporariamente indisponível.", e);
        } catch (HttpServerErrorException | HttpClientErrorException e) {
            log.error("Erro HTTP do microsserviço Python. Status: {}", e.getStatusCode());
            throw e;
        } catch (RestClientException e) {
            log.error("Erro na comunicação com o serviço de scraping", e);
            throw new ScraperException("Erro na comunicação com o serviço de scraping.", e);
        }
    }

    // Buscar links de anúncios na página da OLX
    @Async("taskExecutor")
    public CompletableFuture<ScraperPaginaResponse> buscarLinksPagina(ScraperPaginaRequest request) {
        try {
            ScraperPaginaResponse response = restClient
                    .post()
                    .uri("/api/scraper/buscar-links") // Nova rota validada no Flask
                    .body(request)
                    .retrieve()
                    .body(ScraperPaginaResponse.class);

            return CompletableFuture.completedFuture(response);

        } catch (Exception e) {
            log.error("Erro ao buscar links de anúncios na página", e);
            return CompletableFuture.failedFuture(
                    new ScraperException("Erro ao processar busca de links na OLX.", e)
            );
        }
    }

    // Extrair um lote de anuncios detalhados a partir da lista de links selecionados
    @Async("taskExecutor")
    public CompletableFuture<ScraperLoteResponse> extrairLoteAnuncios(ScraperLoteRequest requestPayload) {
        try {
            ScraperLoteResponse response = restClient
                    .post()
                    .uri("/api/scraper/extrair-lote")
                    .body(requestPayload)
                    .retrieve()
                    .body(ScraperLoteResponse.class);

            return CompletableFuture.completedFuture(response);

        } catch (Exception e) {
            log.error("Erro ao extrair lote de anúncios", e);
            return CompletableFuture.failedFuture(
                    new ScraperException("Erro ao extrair lote detalhado de anúncios.", e)
            );
        }
    }
}