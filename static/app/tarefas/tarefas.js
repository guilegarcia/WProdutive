/**
 * Created by guile on 12/02/16.
 */
angular
    .module('tarefas', []) // [] são as dependências
    .controller('TarefaController', TarefaController)
    .controller('CriarTarefa', CriarTarefa);

function TarefaController($http, $scope, $filter) {
    var self = this;
    $scope.lista_tarefas = [];

    // ___ PRÓXIMO DIA E ANTERIOR (dia.html) ___
    $scope.$watch('data_atual', function () { // mudei o 'ant_prox'
        // ___ LIST ___
        $http.get('/tarefas/api/', {params: {data: $scope.data_atual}})
            .success(function (data) {
                $scope.lista_tarefas = data;
            })
            .error(function (data, status, headers) {
                alert("Não foi possível listar os tarefas");
            });
    });

    // ___ REMOVE ___
    this.delete = function (id, index) {
        $http.delete('/tarefas/api/' + id + '/')
            .success(function (data) {
                $scope.lista_tarefas.splice(index, 1);
                $.alert("Tarefa excluída com sucesso!");
            })
            .error(function (data, status, headers) {
                alert("Não foi possível excluir!" + data);
            });
    };

    // ___ ABRIR (modal) ___
    this.abrirTarefa = function (index) {
        self.tarefa = angular.copy($scope.lista_tarefas[index]);
        // Insere a data corretamente no template (insere mais um pois o new date subtrai um dia)
        // todo verificar pq subtrai (pode ser pelo timezone)
        self.tarefa.data = new Date(self.tarefa.data);
        self.tarefa.data.setDate(self.tarefa.data.getDate()+1);

        $('#atualizarTarefa').modal('show');
        self.index_list = index;
    };

    // ___ UPDATE ___
    this.update = function () {
        // Atualiza a data para o padrão
        self.tarefa.data = $filter('date')(self.tarefa.data, 'yyyy-MM-dd');
        // Insere a tarefa no banco de dados
        $http.put('/tarefas/api/' + self.tarefa.pk + '/', JSON.stringify(self.tarefa))
            .success(function (data, status, headers) {
                // Atualiza a lista de tarefas
                $scope.lista_tarefas[self.index_list] = data;
                $('#atualizarTarefa').modal('hide');
                $.alert("Tarefa atualizada com sucesso!");

            })
            .error(function (data, status, headers) {
                alert("O correu um erro!" + " Dados: " + JSON.stringify(data) + " Status: " + status + " Headers: " + headers)
            });

        // Limpa o form do tarefa e insere o usuário (usado no ng-init)
        var form_copia = angular.copy(self.tarefa); // Copia para não gerar referência

        self.tarefa = {};
        self.tarefa.usuario = form_copia.usuario;
    };
}

function CriarTarefa($http, $scope, $filter) {
    var self = this;

    // todo quando o escopo não tiver a lista_tarefas (ex: TarefaController) usar if($scope.lista)
    // ___ CREATE ___
    self.tarefa = {};
    this.addTarefa = function () {
        // Atualiza o padrão da data
        self.tarefa.data = $filter('date')(self.tarefa.data, 'yyyy-MM-dd');

        $http.post('/tarefas/api/', JSON.stringify(self.tarefa))
            .success(function (data, status, headers) {
                $scope.lista_tarefas.push(data);
                $('#criarTarefa').modal('hide');
                $.alert("Parabéns, você criou um novo tarefa!");

            })
            .error(function (data, status, headers) {
                alert("Errado!" + " Dados: " + JSON.stringify(data) + " Status: " + status + " Headers: " + headers)
            });

        // Limpa o form do tarefa e insere o usuário (usado no ng-init)
        var form_copia = angular.copy(self.tarefa); // Copia para não gerar referência

        self.tarefa = {};
        self.tarefa.usuario = form_copia.usuario;
    };
}










