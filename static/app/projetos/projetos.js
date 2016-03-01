/**
 * Created by guile on 05/02/16.
 */
angular
    .module('projetos', []) // [] são as dependências
    .controller('ProjetoController', ProjetoController)
    .controller('CriarProjeto', CriarProjeto)
    .factory('ProjetoFactory', ProjetoFactory)
    .config(csrf)
    .config(interpolateProvider);

function ProjetoController($scope, ProjetoFactory) {
    var self = this;


    //// LIST
    ProjetoFactory.list()
        .success(function (response) {
            $scope.lista_de_projetos = response;
        })
        .error(function (data, status, headers) {
            alert("Não foi possível listar os projetos");
        });


    // ___ REMOVE ___
    this.delete = function (id, index) {
        ProjetoFactory.delete(id)
            .success(function (data) {
                $scope.lista_de_projetos.splice(index, 1);
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
        ProjetoFactory.update(self.projeto)
            .success(function (data, status, headers) {
                // Atualiza a lista de projetos
                $scope.lista_de_projetos[self.index_list] = data;
                $('#atualizarProjeto').modal('hide');
                $.alert("O projeto foi atualizado!");

            })
            .error(function (data, status, headers) {
                alert("O correu um erro!")
            });

        // Limpa o form do projeto e insere o usuário (usado no ng-init)
        var form_copia = angular.copy(self.projeto); // Copia para não gerar referência

        self.projeto = {};
        self.projeto.usuario = form_copia.usuario;
    };
}


function CriarProjeto(ProjetoFactory, $scope) {
    var self = this;

    // ___ CREATE ___
    self.projeto = {};
    this.addProjeto = function () {

        ProjetoFactory.save(self.projeto)
            .success(function (data) {
                $scope.lista_de_projetos.push(data);
                $('#criarProjeto').modal('hide');
                $.alert("Parabéns, você criou um novo projeto!");

            })
            .error(function (data) {
                $.alert("Ocorreu um erro!", {type: 'danger'});
            });

        // Limpa o form do projeto e insere o usuário (usado no ng-init)
        var form_copia = angular.copy(self.projeto); // Copia para não gerar referência

        self.projeto = {};
        self.projeto.usuario = form_copia.usuario;
    };
}


function ProjetoFactory($http) {
    /*
     Faz o CRUD como banco de dados. Cada uma das funções returna success() ou error()
     */
    return {
        list: function () {
            return $http.get('/projetos/api/');
        },
        save: function (objeto) {
            return $http.post('/projetos/api/', JSON.stringify(objeto));
        },
        delete:function(id){
            return $http.delete('/projetos/api/' + id + '/');
        },
        update: function (objeto) {
            return $http.put('/projetos/api/' + objeto.pk + '/', JSON.stringify(objeto));
        },
        get: function (id) {
            return $http.get('/projetos/api/' + id + '/');
        }
    }
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










