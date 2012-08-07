/* Base Javascript for Optools */

/* Initialize */
function initialize_bootstrap() {
    $("[rel=tooltip]").tooltip();
    $("[rel=popover]").popover();
    $("button").button();
}

/* Events when document is ready */
$(document).ready(function() {
    initialize_bootstrap();

    // Make submit buttons in forms in waiting mode
    $("button[type=submit]").click(function() {
        $(this).button('loading');
    });
});

