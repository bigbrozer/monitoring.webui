/*
** Javascript for Downtime web app
** Author: Vincent BESANCON <besancon.vincent@gmail.com>
*/

$(document).ready(function() {
    /* --- Init --- */
    // Init date and time pickers
    $('#id_start_period').datetimepicker();
    $('#id_end_period').datetimepicker();
    $('#id_start_time').timepicker({});
    $('#id_end_time').timepicker({});
    
    /* --- Handle events --- */
    // Recurrent check box
	$("#recurrent_checkbox").click(function() {
		$("#recurrent_options").toggle();
		$('#recurrent_options input[type=checkbox]').attr('checked', false);
		$('#recurrent_options #id_start_time').attr('value', "");
		$('#recurrent_options #id_end_time').attr('value', "");
		
		// Disable Start and End period input if recurrent
		$("#period_box").toggle();
		$('#id_start_period').attr('value', "");
		$('#id_end_period').attr('value', "");
	});
});
