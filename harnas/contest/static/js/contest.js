$(document).ready(function() {
    var current_tab = $("#current_tab").val();
    var navbar_tab = $('a[href="#' + current_tab + '"]').parent();
    navbar_tab.addClass("active");
    var tab_pane = $("#" + current_tab);
    tab_pane.addClass("active");
});
