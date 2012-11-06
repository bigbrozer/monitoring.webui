/*
KB Rating Javascript code
-------------------------

Author: Vincent BESANCON <besancon.vincent@gmail.com>
*/

function show_rating_box() {
    var rating_box = $(".kb-rating-box");
    rating_box.show();
}

function reset_rating_box() {
    var rating_box = $(".kb-rating-box");
    rating_box.hide();
}

// On document fully loaded and ready
$(document).ready(function() {
    var kb_rows = $(".kb-row");
    var num_row_selected = $("#num_row_selected");
    var selected_rows = [];

    // Init DataTable
    $("#kb_table").dataTable({
        "iDisplayLength": 25,
        "bStateSave": true,
        "oSearch": {
            "sSearch": "",
            "bRegex": true
        },
        "aoColumnDefs": [
            { "bSearchable": true, "aTargets": [ 0 ] },
            { "bSearchable": false, "aTargets": [ "_all" ] }
        ]
    });

    // Button selection events
    $("#kb-btn-select-all").click(function() {
        show_rating_box();
        kb_rows.each(function() {
            $(this).addClass("kb-row-selected");
            selected_rows.push($(this).data("rowId"));
            num_row_selected.html(selected_rows.length + " selected");
        });
    });
    $("#kb-btn-unselect-all").click(function() {
        reset_rating_box();
        kb_rows.each(function() {
            $(".kb-rating-box").hide();
            $(this).removeClass("kb-row-selected");
            selected_rows.splice(selected_rows.indexOf($(this).data("rowId")), 1);
            num_row_selected.html("");
        });
    });

    // Click event on KB rows
    kb_rows.click(function() {
        $(this).toggleClass("kb-row-selected");
        if ($(this).hasClass("kb-row-selected")) {
            selected_rows.push($(this).data("rowId"));
            num_row_selected.html(selected_rows.length + " selected");
        } else {
            selected_rows.splice(selected_rows.indexOf($(this).data("rowId")), 1);
            num_row_selected.html(selected_rows.length + " selected");
        }

        if (selected_rows.length > 0) {
            show_rating_box();
        } else {
            reset_rating_box();
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

    // Handle rating buttons events
    $("span[data-rating]").click(function() {
        var rating_button = $(this);
        var rating = rating_button.data("rating");
        var comment = $("#comment").val();
        var request;

        request = jQuery.ajax("/kb/rating/", {
            "data": {"kb": selected_rows, "rating": rating, "comment": comment}
        });

        $("#kb-btn-unselect-all").trigger("click");
        location.reload();
    });
});