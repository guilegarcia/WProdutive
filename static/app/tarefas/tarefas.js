/**
 * Created by guile on 12/02/16.
 */
angular
    .module('tarefas', []) // [] são as dependências
    .factory('TarefaFactory', TarefaFactory)
    .controller('TarefasSemana', TarefasSemana)
    .controller('TarefaController', TarefaController)
    .controller('CriarTarefa', CriarTarefa);

function TarefaController($http, $scope, $filter, TarefaFactory) {
    var self = this;
    $scope.lista_tarefas = [];

    // ___ PRÓXIMO DIA E ANTERIOR (dia.html) ___
    $scope.$watch('data_atual', function () { // mudei o 'ant_prox'
        // ___ LIST ___
        // todo usar TarefaFactory
        $http.get('/tarefas/api/', {params: {data: $scope.data_atual}})
            .success(function (data) {
                $scope.lista_tarefas = data.tarefas;
                $scope.total_duracao = data.total_duracao;
            })
            .error(function (data, status, headers) {
                alert("Não foi possível listar os tarefas");
            });
    });

    // ___ REMOVE ___
    this.delete = function (id, index) {
        //$http.delete('/tarefas/api/' + id + '/')
        TarefaFactory.delete(id)
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
        self.tarefa.data.setDate(self.tarefa.data.getDate() + 1);

        $('#atualizarTarefa').modal('show');
        self.index_list = index;
    };

    // ___ MUDAR STATUS ___
    this.mudar_status = function (id, index) {
        self.tarefa = angular.copy($scope.lista_tarefas[index]);

        // Tarefa pendente ou atrasada
        if (self.tarefa.status == 0 || self.tarefa.status == 2) {
            self.tarefa.status = 1;
            $.alert("Parabéns, você concluíu mais uma tarefa!");
        }
        // Tarefa já concluída
        else {
            self.tarefa.status = 0;
            $.alert("Tarefa reativada com sucesso!");
        }

        // Atualiza o scopo:
        $scope.lista_tarefas[index] = self.tarefa;

        // Atualiza o banco de dados:
        TarefaFactory.update(self.tarefa)
            .error(function (data, status, headers) {
                alert("O correu um erro!" + " Dados: " + JSON.stringify(data) + " Status: " + status + " Headers: " + headers)
            });

    };

    // ___ UPDATE ___
    this.update = function () {
        // Atualiza a data para o padrão
        self.tarefa.data = $filter('date')(self.tarefa.data, 'yyyy-MM-dd');
        // Insere a tarefa no banco de dados
        TarefaFactory.update(self.tarefa)
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

function TarefasSemana($scope, $filter, TarefaFactory) {
    var data_inicio, data_fim, data_aux, i;

    $scope.$watch('data_semana', function () { // mudei o 'ant_prox'
        $scope.tarefas_semana = [[], [], [], [], [], [], []];
        data_inicio = $filter('date')(new Date($scope.data_semana), 'yyyy-MM-dd');
        data_fim = new Date(data_inicio);
        data_fim = data_fim.setDate(data_fim.getDate() + 7);
        data_fim = $filter('date')(data_fim, 'yyyy-MM-dd');

        // Recebe lista de tarefas da semana
        TarefaFactory.list_semana(data_inicio, data_fim).success(function (data) {
            // Insere o total de duração dos dias no scopo (lista de 7 dias)
            $scope.total_duracao_dias = data.total_duracao;

            // Cria um for para listar as tarefas de cada dia
            angular.forEach(data.tarefas, function (tarefa, x) {
                // Percorre os 7 dias para cada tarefa: // todo buscar ordenado por data
                for (i = 0; i < 7; i++) {
                    if (new Date(tarefa.data).getDay() == i) {
                        $scope.tarefas_semana[i].push(tarefa);
                    }
                }
            });
        });

        //// Insere as datas
        data_aux = new Date(data_inicio);
        $scope.dias_semana = [];
        for (i = 0; i < 7; i++) {
            data_aux.setDate(data_aux.getDate() + 1);
            $scope.dias_semana.push($filter('date')(data_aux, 'yyyy-MM-dd'));
        }

    });
}


function TarefaFactory($http) {
    /*
     Faz o CRUD como banco de dados. Cada uma das funções returna success() ou error()
     */
    return {
        list: function () {
            return $http.get('/tarefas/api/');
        },
        save: function (objeto) {
            return $http.post('/tarefas/api/', JSON.stringify(objeto));
        },
        delete: function (id) {
            return $http.delete('/tarefas/api/' + id + '/');
        },
        update: function (objeto) {
            return $http.put('/tarefas/api/' + objeto.pk + '/', JSON.stringify(objeto));
        },
        get: function (id) {
            return $http.get('/tarefas/api/' + id + '/');
        },
        list_semana: function (inicio, fim) {
            return $http.get('/tarefas/semana/api/', {params: {inicio: inicio, fim: fim}})
        }
    }
}









