package br.com.flipfacil.service;

import br.com.flipfacil.dto.ScraperRequest;
import br.com.flipfacil.dto.ScraperResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class ScraperService {

    private final RestClient restClient;

    public ScraperService(RestClient.Builder builder) {
        this.restClient = builder
                .baseUrl("http://localhost:5001")
                .build();
    }

    public ScraperResponse extrairAnuncio(ScraperRequest request) {

        return restClient
                .post()
                .uri("/scrape/anuncio")
                .body(request)
                .retrieve()
                .body(ScraperResponse.class);
    }
}