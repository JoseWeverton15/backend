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

import br.com.flipfacil.dto.ScraperPaginaRequest;
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
                .baseUrl("http://localhost:5001")
                .build();
    }

    public ScraperResponse extrairAnuncio(ScraperRequest request) {
        try {
            return restClient
                    .post()
                    .uri("/scrape/anuncio")
                    .body(request)
                    .retrieve()
                    .body(ScraperResponse.class);

        } catch (ResourceAccessException e) {
            log.error("Falha ao acessar o serviço de scraping para anúncio", e);
            throw new ScraperException(
                    "Serviço de scraping temporariamente indisponível.", e);

        } catch (HttpServerErrorException e) {
            log.error(
                    "Serviço de scraping retornou erro 5xx. Status: {}",
                    e.getStatusCode(),
                    e
            );
            throw new ScraperException(
                    "Serviço de scraping temporariamente indisponível.", e);

        } catch (HttpClientErrorException e) {
            log.error(
                    "Serviço de scraping retornou erro 4xx. Status: {}",
                    e.getStatusCode(),
                    e
            );
            throw e;

        } catch (RestClientException e) {
            log.error("Erro na comunicação com o serviço de scraping", e);
            throw new ScraperException(
                    "Erro na comunicação com o serviço de scraping.", e);
        }
    }

    @Async("taskExecutor")
    public CompletableFuture<ScraperResponse> extrairPagina(
            ScraperPaginaRequest request) {

        try {
            ScraperResponse response = restClient
                    .post()
                    .uri("/scrape/getItems")
                    .body(request)
                    .retrieve()
                    .body(ScraperResponse.class);

            return CompletableFuture.completedFuture(response);

        } catch (ResourceAccessException e) {
            log.error("Falha ao acessar o serviço de scraping para página", e);

            return CompletableFuture.failedFuture(
                    new ScraperException(
                            "Serviço de scraping temporariamente indisponível.", e)
            );

        } catch (HttpServerErrorException e) {
            log.error(
                    "Serviço de scraping retornou erro 5xx. Status: {}",
                    e.getStatusCode(),
                    e
            );

            return CompletableFuture.failedFuture(
                    new ScraperException(
                            "Serviço de scraping temporariamente indisponível.", e)
            );

        } catch (HttpClientErrorException e) {
            log.error(
                    "Serviço de scraping retornou erro 4xx. Status: {}",
                    e.getStatusCode(),
                    e
            );

            return CompletableFuture.failedFuture(e);

        } catch (RestClientException e) {
            log.error("Erro na comunicação com o serviço de scraping", e);

            return CompletableFuture.failedFuture(
                    new ScraperException(
                            "Erro na comunicação com o serviço de scraping.", e)
            );
        }
    }
}