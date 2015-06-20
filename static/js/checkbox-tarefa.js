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
             $('#resultado').html(data.mensagem)
        });

    } else {
        $.post( "/tarefas/alterar-status", { id: id, estado: "desmarcado", csrfmiddlewaretoken: csrftoken }, function( data ) {
            alert( data.mensagem );
        });
    }
}

<!-- Fim Script Checkbox tarefa -->