var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

$(document).ready(function() {
    var current_tab = getUrlParameter('current_tab');
    var navbar_tab = $('a[href="#' + current_tab + '"]').parent();
    navbar_tab.addClass("active");
    var tab_pane = $("#" + current_tab);
    tab_pane.addClass("active");
});
