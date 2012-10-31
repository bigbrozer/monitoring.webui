/*
KB Rating Javascript code
-------------------------

Author: Vincent BESANCON <besancon.vincent@gmail.com>
*/

function handleKbEvents() {
    // All KB rows
    var kb_rows = $(".kb-row");
    var rating_box = $(".kb-rating-box");
    var selected_rows = [];

    // KB rows events
    //
    // Buttons selection
    $("#kb-btn-select-all").click(function() {
        kb_rows.each(function() {
            $(".kb-rating-box").show();
            $(this).addClass("kb-row-selected");
        });
    });
    $("#kb-btn-unselect-all").click(function() {
        kb_rows.each(function() {
            $(".kb-rating-box").hide();
            $(this).removeClass("kb-row-selected");
        });
    });

    // KB rows
    kb_rows.click(function() {
        $(this).toggleClass("kb-row-selected");
        if ($(this).hasClass("kb-row-selected")) {
            selected_rows.push(this);
        } else {
            selected_rows.splice(selected_rows.indexOf(this), 1);
        }

        if (selected_rows.length > 0) {
            rating_box.show();
        } else {
            rating_box.hide();
        }
    });
    kb_rows.mouseover(function() {
        $(this).addClass('kb-row-over');
    });
    kb_rows.mouseout(function() {
        $(this).removeClass('kb-row-over');
    });
}

$(document).ready(function() {
    handleKbEvents();
});