/**
 * Created by guile on 12/02/16.
 */
angular
    .module('papeis', []) // [] são as dependências
    .controller('PapelController', PapelController)
    .controller('CriarPapel', CriarPapel)
    .config(csrf)
    .config(interpolateProvider);

function PapelController($http, $scope) {

    var self = this;
    $scope.lista_papeis = [];

    // ___ LIST ___
    $http.get('/papeis/api/')
        .success(function (data) {
            $scope.lista_papeis = data;
        })
        .error(function (data, status, headers) {
            alert("Não foi possível listar os papeis");
        });


    // ___ REMOVE ___
    this.delete = function (id, index) {
        $http.delete('/papeis/api/' + id + '/')
            .success(function (data) {
                $scope.lista_papeis.splice(index, 1);
                $.alert("Papel excluído com sucesso!");
            })
            .error(function (data, status, headers) {
                alert("Não foi possível excluir!" + data);
            });
    };

    // ___ ABRIR PROJETO (modal) ___
    this.abrirPapel = function (index) {
        self.papel = angular.copy($scope.lista_papeis[index]);
        $('#atualizarPapel').modal('show');
        self.index_list = index;
    };

    // ___ UPDATE ___
    this.atualizaPapel = function () {
        $http.put('/papeis/api/' + self.papel.pk + '/', JSON.stringify(self.papel))
            .success(function (data, status, headers) {
                // Atualiza a lista de papeis
                $scope.lista_papeis[self.index_list] = data;
                $('#atualizarPapel').modal('hide');
                $.alert("O papel foi atualizado!");

            })
            .error(function (data, status, headers) {
                alert("O correu um erro!" + " Dados: " + JSON.stringify(data) + " Status: " + status + " Headers: " + headers)
            });

        // Limpa o form do papel e insere o usuário (usado no ng-init)
        var form_copia = angular.copy(self.papel); // Copia para não gerar referência

        self.papel = {};
        self.papel.usuario = form_copia.usuario;
    };
}


function CriarPapel($http, $scope) {
    var self = this;

    // todo quando o escopo não tiver a lista_papeis (ex: TarefaController) usar if($scope.lista)
    // ___ CREATE ___
    self.papel = {};
    this.addPapel = function () {
        $http.post('/papeis/api/', JSON.stringify(self.papel))
            .success(function (data, status, headers) {
                $scope.lista_papeis.push(data);
                $('#criarPapel').modal('hide');
                $.alert("Parabéns, você criou um novo papel!");

            })
            .error(function (data, status, headers) {
                alert("Errado!" + " Dados: " + JSON.stringify(data) + " Status: " + status + " Headers: " + headers)
            });

        // Limpa o form do papel e insere o usuário (usado no ng-init)
        var form_copia = angular.copy(self.papel); // Copia para não gerar referência

        self.papel = {};
        self.papel.usuario = form_copia.usuario;
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











