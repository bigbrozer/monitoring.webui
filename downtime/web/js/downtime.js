/*
** Javascript for Downtime web app
** Author: Vincent BESANCON <besancon.vincent@gmail.com>
*/

$(document).ready(function() {
    /* --- Init --- */
    // Init date and time pickers
    $('#start_period').datetimepicker();
    $('#end_period').datetimepicker();
    $('#start_hour').timepicker({});
    $('#end_hour').timepicker({});
    
    /* --- Handle events --- */
    // Recurrent check box
	$("#recurrent_checkbox").click(function() {
		$("#recurrent_options").toggle();
		$('#recurrent_options input[type=checkbox]').attr('checked', false);
		$('#recurrent_options #start_hour').attr('value', "");
		$('#recurrent_options #end_hour').attr('value', "");
		
		// Disable Start and End period input if recurrent
		$("#period_box").toggle();
		$('#start_period').attr('value', "");
		$('#end_period').attr('value', "");
	});
});
