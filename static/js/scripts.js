/**
 * Created by GuiLe Garcia on 12/06/2015.
 */

<!-- gera token -->
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

<!-- Script Checkbox tarefa -->
$(document).ready(function () {
    $(document).on("change", ".checkTarefa", mudou);

    /* TESTE JQUERY SUBMIT
     $("#button_editar_tarefa").click(function () {
     $.ajax({
     type: "POST",
     url: '/tarefas/editar/',
     data: $("#form_tarefa").serialize(), // serializes the form's elements.
     success: function (data) {
     $('#criarTarefa').modal('toggle');
     $("#lista_de_tarefas").load(location.href + " #lista_de_tarefas");
     }
     });
     return false; // avoid to execute the actual submit of the form.
     });
     */
});


// Mudou o change (precisa ativar o trigger)
function mudou() {
    var id = $(this).attr("idTarefa");
    var csrftoken = getCookie('csrftoken');

    // Concluída
    if ($(this).prop('checked')) {
        $.post("/tarefas/alterar-status", {id: id, estado: "marcado", csrfmiddlewaretoken: csrftoken}, function (data) {
            $('#mostrar-alerta').show(5);
            $('#resultado').html(data.mensagem);
            $("#tabelaTarefas").load(location.href + " #tabelaTarefas>*");
            $(".progress").load(location.href + " .progress");
        });
    }
    // Tarefa reativada
    else {
        $.post("/tarefas/alterar-status", {
            id: id,
            estado: "desmarcado",
            csrfmiddlewaretoken: csrftoken
        }, function (data) {
            $('#mostrar-alerta').show(5);
            $('#resultado').html(data.mensagem);
            $("#tabelaTarefas").load(location.href + " #tabelaTarefas>*");
            $(".progress").load(location.href + " .progress");
        });
    }
}
<!-- Fim Script Checkbox tarefa -->


// Editar projeto
function editar_projeto(id) {
    event.preventDefault();
    var csrftoken = getCookie('csrftoken');

    $.get("/projetos/editar/", {id: id, csrfmiddlewaretoken: csrftoken}, function (data) {
        try {
            // dados = $.parseJSON(data);
            $("#id_nome_projeto").val(data.nome);
            $("#id_descricao_projeto").val(data.descricao);
            $("#id_id_projeto").val(data.id);
            $("#criar_editar_projeto").attr('action', '/projetos/editar/');
            $('#criarProjeto').modal('show');

        } catch (e) {
            console.log(data);
        }
    });
}

// Editar tarefa
function editar_tarefa(id) {
    event.preventDefault();
    var csrftoken = getCookie('csrftoken');

    $.get("/tarefas/editar/", {id: id, csrfmiddlewaretoken: csrftoken}, function (data) {
        try {

            $("#form_tarefa").attr('action', '/tarefas/editar/');
            $('#criarTarefa').modal('show');
            $("#id_titulo_tarefa").val(data.titulo);
            $("#id_descricao_tarefa").val(data.descricao);
            $("#id_data_tarefa").val(data.data);
            $("#id_hora_tarefa").val(data.hora);
            $("#id_duracao_tarefa").val(data.duracao);
            $("#id_prioridade_tarefa").val(data.prioridade);
            $("#id_papel_tarefa").val(data.papel);
            $("#id_projeto_tarefa").val(data.projeto);
            $("#id_usuario_tarefa").val(data.usuario);
            $("#tarefa_id_id").val(data.id);
            /* todo problema: Ao abrir e preeencher o formulário com jquery fica o mesmo para Adicionar tarefa" (criar outor form) */
            // todo adicionar checkbox para verificar se o usuário quer editar todas repetições (caso haja repetição)

        } catch (e) {
            console.log(data);
        }
    });
}

$('#abrirTarefa').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal

    var titulo = button.data('titulo'); // Extract info from data-* attributes
    var descricao = button.data('descricao');

    var modal = $(this);
    modal.find('.modal-title').text(titulo);
    modal.find('.modal-body p').text(descricao);
});

// Próximo dia anterior (dia.html)
function proximo_dia_anterior(ant_prox, date) {
    event.preventDefault();
    var csrftoken = getCookie('csrftoken');

    $.post("/dia/", {ant_prox: ant_prox, data: date, csrfmiddlewaretoken: csrftoken}, function (data) {
        // location.reload(true);
        $("#tabelaTarefas").load(location.href + " #tabelaTarefas>*");
        $(".progress").load(location.href + " .progress");
    });

}





