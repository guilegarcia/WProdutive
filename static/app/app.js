/**
 * Created by guile on 06/02/16.
 */
angular
    .module('app', [
        'projetos',
        'lembretes',
        'papeis'
    ])    // [] são as dependências
    .config(csrf)
    .config(interpolateProvider);

// CONFIGURAÇÕES
function interpolateProvider($interpolateProvider) {
    // Configura para usar [[ ]]  no template
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
}

// Configura o CSRF para o Django
function csrf($httpProvider) {
    // CSRF Support
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}



