/**
 * Created by guile on 12/02/16.
 */
angular
    .module('lembretes', []) // [] são as dependências
    .controller('LembreteController', LembreteController)
    .controller('CriarLembrete', CriarLembrete);

function LembreteController($http, $scope) {
    var self = this;
    $scope.lista_lembretes = [];

    // ___ PRÓXIMO DIA E ANTERIOR ___
    $scope.$watch('data_atual', function () { // mudei o 'ant_prox'
        // ___ LIST ___
        $http.get('/lembretes/api/', {params: {data: $scope.data_atual}})
            .success(function (data) {
                $scope.lista_lembretes = data;
            })
            .error(function (data, status, headers) {
                alert("Não foi possível listar os lembretes");
            });
    });


    // ___ REMOVE ___
    this.delete = function (id, index) {
        $http.delete('/lembretes/api/' + id + '/')
            .success(function (data) {
                $scope.lista_lembretes.splice(index, 1);
                $.alert("Lembrete excluído com sucesso!");
            })
            .error(function (data, status, headers) {
                alert("Não foi possível excluir!" + data);
            });
    };

    // ___ ABRIR LEMBRETE (modal) ___
    this.abrirLembrete = function (index) {
        self.lembrete = angular.copy($scope.lista_lembretes[index]);
        $('#atualizarLembrete').modal('show');
        self.index_list = index;
    };

    // ___ UPDATE ___
    this.atualizaLembrete = function () {
        $http.put('/lembretes/api/' + self.lembrete.pk + '/', JSON.stringify(self.lembrete))
            .success(function (data, status, headers) {
                // Atualiza a lista de lembretes
                $scope.lista_lembretes[self.index_list] = data;
                $('#atualizarLembrete').modal('hide');
                $.alert("O lembrete foi atualizado!");

            })
            .error(function (data, status, headers) {
                alert("O correu um erro!" + " Dados: " + JSON.stringify(data) + " Status: " + status + " Headers: " + headers)
            });

        // Limpa o form do lembrete e insere o usuário (usado no ng-init)
        var form_copia = angular.copy(self.lembrete); // Copia para não gerar referência
        self.lembrete = {};
        self.lembrete.usuario = form_copia.usuario;
    };
}


function CriarLembrete($http, $scope, $filter) {
    var self = this;

    // ___ CREATE ___
    self.lembrete = {};
    self.lembrete.data = new Date(); // Seta a data de hoje (ng-init) não funciona com Date()

    this.adicionar = function () {
        // Atualiza o padrão da data
        self.lembrete.data = $filter('date')(self.lembrete.data, 'yyyy-MM-dd');

        $http.post('/lembretes/api/', JSON.stringify(self.lembrete))
            .success(function (data, status, headers) {
                // Verifica se é a data atual para inserir na lista
                if($scope.data_atual == data.data){
                    $scope.lista_lembretes.push(data);
                }

                $('#criarLembrete').modal('hide');
                $.alert("Parabéns, você criou um novo lembrete!");
            })
            .error(function (data, status, headers) {
                alert("Errado!" + " Dados: " + JSON.stringify(data) + " Status: " + status + " Headers: " + headers)
            });

        // Limpa o form do lembrete e insere o usuário (usado no ng-init)
        var form_copia = angular.copy(self.lembrete); // Copia para não gerar referência

        self.lembrete = {};
        self.lembrete.usuario = form_copia.usuario;
        self.lembrete.data = new Date(); // Seta a data de hoje (ng-init) não funciona com Date()
    };
}