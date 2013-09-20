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

function main () {
    
}


function fixtures(){
    var codes = [
        "AD_US_READ",
        "AD_AC_CREATE",
        "AD_AC_UPDATE",
        "AD_AC_DELETE",
        "AD_AC_READ",
        "AD_DE_CREATE",
        "AD_DE_UPDATE",
        "AD_DE_DELETE",
        "AD_DE_READ",
        "OP_GE_CREATE",
        "OP_GE_UPDATE",
        "OP_GE_DELETE",
        "OP_GE_DISABLE",
        "OP_GE_READ",
        "OP_LL_CREATE",
        "OP_LL_UPDATE",
        "OP_LL_DELETE",
        "OP_LL_READ",
        "OP_CA_CREATE",
        "OP_CA_UPDATE",
        "OP_CA_DELETE",
        "OP_CA_READ",
        "OP_VE_CREATE",
        "OP_VE_UPDATE",
        "OP_VE_DELETE",
        "OP_VE_READ",
        "NO_AD_CREATE",
        "NO_AD_UPDATE",
        "NO_AD_DELETE",
        "NO_AD_READ",
        "NO_GE_CREATE",
        "NO_GE_UPDATE",
        "NO_GE_DELETE",
        "NO_GE_READ",
        "RE_HI_CREATE",
        "RE_HI_UPDATE",
        "RE_HI_DELETE",
        "RE_HI_READ",
        "RE_RE_CREATE",
        "RE_RE_UPDATE",
        "RE_RE_DELETE",
        "RE_RE_READ"
    ]
    i=0;
    s = "";
    for (i;i<codes.length;i++){
        /*console.log(codes[i]);*/
        s = s + '{<br>'+
            '"model": "process_admin.permissions",<br>'+
            '"pk":' + parseInt(i + 6) + ',<br>'+
            '"fields":<br>'+
            '{<br>'+
                '"name":"'+ codes[i] +'",<br>'+
                '"description":"...",<br>'+
                '"is_active":1,<br>'+
                '"user_type": [1, 2],<br>'+
                '"date_added":"2013-09-19 21:57:05",<br>'+
                '"date_modified":"2013-09-19 21:57:05"<br>'+
            '}<br>'+
        '},<br>';
    }
    console.log(s);
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
$(document).ready(main);
