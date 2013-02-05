/* Base Javascript for Optools */

/* Initialize */
function initialize_bootstrap() {
    $("[rel=tooltip]").tooltip();
    $("[rel=popover]").popover();
    $("button[type=submit], .btn-loading").button();
}

/* Events when document is ready */
$(document).ready(function() {
    initialize_bootstrap();

    // Make submit buttons in forms in waiting mode
    $("button[type=submit], .btn-loading").click(function() {
        $(this).button('loading');
    });

    // Show browser not supported modal if defined in template
    $('#modal-browser-not-supported').modal();
});

