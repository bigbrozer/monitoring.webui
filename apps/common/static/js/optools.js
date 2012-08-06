/* Base Javascript for Optools */

/* Initialize */
function initialize_bootstrap() {
    $("[rel=tooltip]").tooltip();
    $("[rel=popover]").popover();
}

/* Events when document is ready */
$(document).ready(function() {
    initialize_bootstrap();
});

