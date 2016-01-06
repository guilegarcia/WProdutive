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
<!-- todo adicionar o botão editar em projetos.html e adaptar views.py -->
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

