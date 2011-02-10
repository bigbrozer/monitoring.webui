/*
** Javascript for Downtime web app
** Author: Vincent BESANCON <besancon.vincent@gmail.com>
*/

$(document).ready(function() {
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
