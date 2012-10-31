/*
KB Rating Javascript code
-------------------------

Author: Vincent BESANCON <besancon.vincent@gmail.com>
*/

function handleKbEvents() {
    var kb_rows = $(".kb-row");
    var rating_box = $(".kb-rating-box");
    var num_row_selected = $("#num_row_selected");
    var selected_rows = [];

    // Button selection events
    $("#kb-btn-select-all").click(function() {
        kb_rows.each(function() {
            $(".kb-rating-box").show();
            $(this).addClass("kb-row-selected");
            selected_rows.push(this);
            num_row_selected.html(selected_rows.length + " selected");
        });
    });
    $("#kb-btn-unselect-all").click(function() {
        kb_rows.each(function() {
            $(".kb-rating-box").hide();
            $(this).removeClass("kb-row-selected");
            selected_rows.splice(selected_rows.indexOf(this), 1);
            num_row_selected.html("");
        });
    });

    // Click event on KB rows
    kb_rows.click(function() {
        $(this).toggleClass("kb-row-selected");
        if ($(this).hasClass("kb-row-selected")) {
            selected_rows.push(this);
            num_row_selected.html(selected_rows.length + " selected");
        } else {
            selected_rows.splice(selected_rows.indexOf(this), 1);
            num_row_selected.html(selected_rows.length + " selected");
        }

        if (selected_rows.length > 0) {
            rating_box.show();
        } else {
            rating_box.hide();
            num_row_selected.html("");
        }
    });

    // Mouse events on KB rows
    kb_rows.mouseover(function() {
        $(this).addClass('kb-row-over');
    });
    kb_rows.mouseout(function() {
        $(this).removeClass('kb-row-over');
    });
}

// On document fully loaded and ready
$(document).ready(function() {
    // Handle all events
    handleKbEvents();
});