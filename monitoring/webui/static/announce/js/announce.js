// Toggle display state of announcement details and scroll to it
$(document).ready(function() {
    $("a.show-details").click(function () {
        $("div.announcement-details").slideDown("slow", function() {
                $.scrollTo($(this), 800, {offset:-40});
        });
    }); 
});
