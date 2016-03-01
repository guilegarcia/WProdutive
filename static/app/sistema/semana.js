/**
 * Created by guile on 13/02/16.
 */
angular
    .module('semana', [
        'tarefas',
        'lembretes',
        'projetos',
        'papeis'
    ])    // [] são as dependências
    .controller('SemanaController', SemanaController)
    .config(csrf)
    .config(interpolateProvider);


function SemanaController($scope, $filter) {
    // Pega a data atual e insere no scopo
    var data_aux = new Date();
    //data_aux.toLocaleDateString('pt-BR', {timezone: 'BRT'});
    //console.log("Locale", data_aux.toLocaleDateString('pt-BR', {weekday: 'long', hour:'numeric', minute:'numeric', timezone: 'BRT'}));
    // Pega a segunda-feira
    data_aux = data_aux.setDate(data_aux.getDate() - data_aux.getDay()+2);
    $scope.data_semana = $filter('date')(data_aux, 'yyyy-MM-dd');

    // Clica no botão < > (semana.html)
    this.proximo_anterior = function (prox_ant) {
        // Cria uma nova data com a data atual (em string)
        data_aux = new Date($scope.data_semana);
        data_aux.setDate(data_aux.getDate() - data_aux.getDay()+2); // Gera a segunda-feira
        dia_atual = data_aux.getDate();

        if(prox_ant == 'proximo'){
            data_aux.setDate(dia_atual + 7);
        } else {
            data_aux.setDate(dia_atual-7);
        }
        console.log("Atual, depois de mudar", data_aux);
        $scope.data_semana = $filter('date')(data_aux, 'yyyy-MM-dd')
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



