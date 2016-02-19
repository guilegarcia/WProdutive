/**
 * Created by guile on 13/02/16.
 */
angular
    .module('dia', [
        'tarefas',
        'lembretes',
        'projetos',
        'papeis'
    ])    // [] são as dependências
    .config(csrf)
    .config(interpolateProvider);

function DiaController($http, $scope) {
    $scope.lista_tarefas = [];
    $scope.lista_lembretes = [];
    $scope.date = new Date();
    // configurar o data
    data_string = $filter('date')($scope.date, "yyyy-MM-dd");
    alert(data_string);


    // ___ LIST LEMBRETES do dia (data atual) ___
    // todo ideia: passar como parametro a data atual (gerada via jquery)
    $http.get('/lembretes/api/')
        .success(function (data) {
            $scope.lista_lembretes = data;
        })
        .error(function (data, status, headers) {
            alert("Não foi possível listar os lembretes!");
        });

    // ___ LIST TAREFAS do dia (data atual) ___
    // todo ideia: passar como parametro a data atual (gerada via jquery)
    $http.get('/tarefas/api/')
        .success(function (data) {
            $scope.lista_tarefas = data;
        })
        .error(function (data, status, headers) {
            alert("Não foi possível listar as tarefas!");
        });


    this.proximo_anterior = function (data, prox_ant) {
        // Envia para o servidor a data e se é próximo ou anterior
        $http.get('/lembretes/api/', {params: {data: data, ant_prox: prox_ant}})
            .success(function (data) {
                $scope.lista_lembretes = data;
            })
            .error(function (data, status, headers) {
                alert("Não foi possível listar os lembretes");
            });

        // todo lista tarefas

    };
}


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