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
    $('.checkTarefa').change(mudou);
});

// Mudou o change (precisa ativar o trigger)
function mudou() {
    var id = $(this).attr("idTarefa");
    var csrftoken = getCookie('csrftoken');

    if ($(this).prop('checked')) {
        $.post( "/tarefas/alterar-status", { id: id, estado: "marcado", csrfmiddlewaretoken: csrftoken }, function( data ) {
             $(".progress").load(location.href + " .progress");
             $('#mostrar-alerta').show(5)
             $('#resultado').html(data.mensagem)
        });

    } else {
        $.post( "/tarefas/alterar-status", { id: id, estado: "desmarcado", csrfmiddlewaretoken: csrftoken }, function( data ) {
            $('#mostrar-alerta').show(5)
            $('#resultado').html(data.mensagem)
        });
    }
}
<!-- Fim Script Checkbox tarefa -->

<!-- Submit form Criar Lembrete -->
<!-- todo testar ajaxSubmit malsup.com/jquery/form   jsfiddle.net/hRTcE/ -->

// Editar projeto
function editar_projeto(id){
    event.preventDefault();
    var csrftoken = getCookie('csrftoken');

    $.get("/projetos/editar/", { id: id, csrfmiddlewaretoken: csrftoken}, function(data){
     try{
         // dados = $.parseJSON(data);
         $("#id_nome_projeto").val(data.nome);
         $("#id_descricao_projeto").val(data.descricao);
         $("#id_id_projeto").val(data.id);
         $("#criar_editar_projeto").attr('action', '/projetos/editar/');
         $('#criarProjeto').modal('show');

     } catch(e){
          console.log(data);
     }
    });
}

// Editar tarefa
function editar_tarefa(id){
    event.preventDefault();
    var csrftoken = getCookie('csrftoken');

    $.get("/tarefas/editar/", { id: id, csrfmiddlewaretoken: csrftoken}, function(data){
     try{
         $('#criarTarefa').modal('show');
         $("#form_tarefa").attr('action', '/tarefas/editar/');
         // dados = $.parseJSON(data);
         $("#id_titulo_tarefa").val(data.titulo);
         $("#id_descricao_tarefa").val(data.descricao);
         $("#id_data_tarefa").val(data.data);
         $("#id_hora_tarefa").val(data.hora);
         $("#id_duracao_tarefa").val(data.duracao);
         $("#id_prioridade_tarefa").val(data.prioridade);
         $("#id_papel_tarefa").val(data.papel);
         $("#id_projeto_tarefa").val(data.projeto);
         $("#id_usuario_tarefa").val(data.usuario.id);
         $("#id_id_tarefa").val(data.id);

         /* todo problema: Ao abrir e preeencher o formulário com jquery fica o mesmo para Adicionar tarefa" */
         /*
            * id_repeticao_tarefa
            * numRepeticoes
            id_url_tarefa (acho que não precisa, pois já tem a url no contexto do template
         */

     } catch(e){
          console.log(data);
     }
    });
}