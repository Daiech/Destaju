// Avoid `console` errors in browsers that lack a console.
if (!(window.console && console.log)) {
    (function() {
        var noop = function() {};
        var methods = ['assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error', 'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log', 'markTimeline', 'profile', 'profileEnd', 'markTimeline', 'table', 'time', 'timeEnd', 'timeStamp', 'trace', 'warn'];
        var length = methods.length;
        var console = window.console = {};
        while (length--) {
            console[methods[length]] = noop;
        }
    }());
}

// Place any jQuery/helper plugins in here.
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
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
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
$(function(){
    function editValue (elem) {
        var data = elem.val();
        if(elem.attr("data-value-saved") != data){
            var ctx = {
                obj_id: elem.attr("data-obj-id"),
                name: elem.attr("name"),
                reference: elem.attr("data-reference"),
                data: data,
                old_data: elem.attr("data-value-saved")
            };
            send_ajax(
                "/ajax/editinline",
                ctx,
                function (data) {
                    console.log(data);
                    if (data.value != "Error"){
                        elem.attr("value", data.value);
                        elem.attr("data-value-saved", data.value)
                    }else{
                        console.log('este es editinline');
                        setAlertError(data.value, data.message)
                    }
                },
                {"load_elem":"#load", "method":"post"}
            );
        }
    }
    $(document).on("keypress", "input.editable", function (e) {
        if (e.keyCode === 13){
            //editValue($(this));
            $(this).blur();
        }
    });
    $(document).on("blur", "input.editable", function (e) {
        editValue($(this));
    });
    $(document).on("click", "input.editable", function (e) {
        this.select();
    });
});

function main () {
    $("a.btn-delete").on("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        if ( confirm("Seguro que quiere eliminar?") ){
            top.location = $(this).attr("href");
        }
    });
}
function hasHash (hash) {
    if(window.location.hash && window.location.hash == hash){
        return true;
    }
    else{
        return false;
    }
}

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

function setAlert(tittle, message, type){
    var l = message.length;
    var t=0;
    if (l===0) t=0;
    else if (l<=50)  t=3000;
    else if (l<=100) t=5000;
    else if (l<=200) t=6000;
    else if (l> 200) t=7000;
    $(type+" h4").html(tittle);
    $(type+" p").html(message);
    $(type).fadeIn().delay(t).fadeOut(1500);
}
function setAlertError(t, m){
    setAlert(t, m, '#alert-error');
}
function setAlertMessage(t, m){
    setAlert(t, m, '#alert-message');
}
function sendAjax(url, params, load_elem, myCallback){
    // $(load_elem).show().html('<img src="/static/img/load16.gif" />');
    $("#ac-load").fadeIn().html('<img src="/static/img/load.gif" />');
    $.get(url, params, function(data,error) {
            myCallback(data,error);
            // $(load_elem).hide();
            $("#ac-load").fadeOut();
        }
    );
}
function send_ajax(url, params, myCallback, args) {
    if (typeof args === "undefined") {
        load_elem = "#load";
    } else {
        load_elem = args.load_elem;
    }
    /*$(load_elem).show().html('<img src="/static/img/load16.gif" />');*/
    $(load_elem).show().html('Cargando...');
    if (typeof args === "undefined" || args.method === "get") {
        $.get(url, params)
                .done(function(data) {
            myCallback(data);
            $(load_elem).fadeOut();
        }).fail(function(error) {
            console.log(error);
        });
    } else if (args.method === "post") {
        $.post(url, params)
                .done(function(data) {
            myCallback(data);
            $(load_elem).fadeOut();
        }).fail(function(error) {
            console.log(error);
        });
    }
}
function setDataTables(id_table){
	var oTable = $(id_table).dataTable( {
		"iDisplayLength": 30,
        "aLengthMenu": [
            [30, 100, 1000, -1],
            [30, 100, 1000, "Todos"]
        ],
        "aaSorting": [],
		"oLanguage": {
			"sLengthMenu": "Mostrar _MENU_ registros",
			"sZeroRecords": "No hay datos para mostrar",
			"sInfo": "Mostrando _START_ a _END_ de _TOTAL_ registros",
			"sInfoEmpty": "Mostrando 0 a 0 de 0 registros",
			"sInfoFiltered": "(filtro de _MAX_ registros en total)",
			"sSearch": "_INPUT_",
			"oPaginate": {
                "sFirst": "Primera",
                "sLast": "Ultima",
                "sNext": "Siguiente",
                "sPrevious": "Anterior"
                },
            },
        } );
    $("#usersList_filter > label > input").attr("placeholder", "Filtrar");
}
$(document).ready(main);
