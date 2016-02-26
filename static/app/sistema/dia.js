/**
 * Created by guile on 13/02/16.
 */
angular
    .module('dia', [
        'lembretes',
        'projetos',
        'papeis',
        'tarefas'
    ])    // [] são as dependências
    .config(csrf)
    .config(interpolateProvider)
    .controller('DiaController', DiaController);

function DiaController($scope, $filter) {
    // Pega a data atual e insere no scopo
    var data_aux = new Date();
    $scope.data_atual = $filter('date')(data_aux, 'yyyy-MM-dd');

    this.proximo_anterior = function (prox_ant, data) {
        // Cria uma nova data com a data atual (em string)
        data_aux = new Date($scope.data_atual);
        dia_atual = data_aux.getDate();

        if(prox_ant == 'proximo'){
            data_aux.setDate(dia_atual+2);
        }
        $scope.data_atual = $filter('date')(data_aux, 'yyyy-MM-dd')
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