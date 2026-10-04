package br.com.flipfacil.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import br.com.flipfacil.service.UsuarioAutenticadoService;

@RestController
public class TesteController {
    private final UsuarioAutenticadoService usuarioAutenticadoService;

    public TesteController(UsuarioAutenticadoService usuarioAutenticadoService) {
        this.usuarioAutenticadoService = usuarioAutenticadoService;
    }

    @GetMapping("/teste")
    public String teste() {
        return usuarioAutenticadoService.authenticatedUser();
    } 
    
}
