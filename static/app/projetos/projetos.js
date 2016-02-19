/**
 * Created by guile on 05/02/16.
 */
angular
    .module('projetos', []) // [] são as dependências
    .controller('ProjetoController', ProjetoController)
    .controller('CriarProjeto', CriarProjeto)
    .config(csrf)
    .config(interpolateProvider);

function ProjetoController($http, $scope) {
    var self = this;
    $scope.lista_de_projetos = [];

    // ___ LIST ___
    $http.get('/projetos/api/')
        .success(function (data) {
            $scope.lista_de_projetos = data;
        })
        .error(function (data, status, headers) {
            alert("Não foi possível listar os projetos");
        });


    // ___ REMOVE ___
    this.delete = function (id, index) {
        $http.delete('/projetos/api/' + id + '/')
            .success(function (data) {
                $scope.lista_de_projetos.splice(index, 1);
                // Adiciona o alerta do boostrap
                //$('#alerta').after(
                //    '<div class="alert alert-success alert-dismissable">' +
                //    '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
                //    '<strong>Projeto excluído com sucesso!</strong> ' +
                //    '</div>');
                $.alert("Projeto excluído com sucesso!");
            })
            .error(function (data, status, headers) {
                alert("Não foi possível excluir!" + data);
            });
    };

    // ___ ABRIR PROJETO (modal) ___
    this.abrirProjeto = function (index) {
        self.projeto = angular.copy($scope.lista_de_projetos[index]);
        $('#atualizarProjeto').modal('show');
        self.index_list = index;
    };

    // ___ UPDATE ___
    this.atualizaProjeto = function () {
        $http.put('/projetos/api/' + self.projeto.pk + '/', JSON.stringify(self.projeto))
            .success(function (data, status, headers) {
                // Atualiza a lista de projetos
                $scope.lista_de_projetos[self.index_list] = data;
                $('#atualizarProjeto').modal('hide');
                $.alert("O projeto foi atualizado!");

            })
            .error(function (data, status, headers) {
                alert("O correu um erro!" + " Dados: " + JSON.stringify(data) + " Status: " + status + " Headers: " + headers)
            });

        // Limpa o form do projeto e insere o usuário (usado no ng-init)
        var form_copia = angular.copy(self.projeto); // Copia para não gerar referência

        self.projeto = {};
        self.projeto.usuario = form_copia.usuario;
    };
}


function CriarProjeto($http, $scope) {
    var self = this;

    // todo quando o escopo não tiver a lista_de_projetos (ex: TarefaController) usar if($scope.lista)
    // ___ CREATE ___
    self.projeto = {};
    this.addProjeto = function () {
        $http.post('/projetos/api/', JSON.stringify(self.projeto))
            .success(function (data, status, headers) {
                $scope.lista_de_projetos.push(data);
                $('#criarProjeto').modal('hide');
                // Adiciona o alerta do boostrap
                //$('#alerta').after(
                //    '<div class="alert alert-success alert-dismissable">' +
                //    '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
                //    '<strong>Parabéns!</strong> Você criou um novo projeto!' +
                //    '</div>');
                $.alert("Parabéns, você criou um novo projeto!");

            })
            .error(function (data, status, headers) {
                alert("Errado!" + " Dados: " + JSON.stringify(data) + " Status: " + status + " Headers: " + headers)
            });

        // Limpa o form do projeto e insere o usuário (usado no ng-init)
        var form_copia = angular.copy(self.projeto); // Copia para não gerar referência

        self.projeto = {};
        self.projeto.usuario = form_copia.usuario;
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










