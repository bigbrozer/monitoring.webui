/*
** Javascript for Downtime web app
** Author: Vincent BESANCON <besancon.vincent@gmail.com>
*/

function toggleRecurrent() {
	$("#recurrent_options").toggle();
	$('#recurrent_options input[type=checkbox]').attr('checked', false);
	$('#recurrent_options #id_start_time').attr('value', "");
	$('#recurrent_options #id_end_time').attr('value', "");
	
	// Disable Start and End period input if recurrent
	$("#period_box").toggle();
	$('#id_start_period').attr('value', "");
	$('#id_end_period').attr('value', "");
}

$(document).ready(function() {
    /* --- Init --- */
    // Init date and time pickers
    $('#id_start_period').datetimepicker();
    $('#id_end_period').datetimepicker();
    $('#id_start_time').timepicker({});
    $('#id_end_time').timepicker({});
    
    // State of recurrent options
    if ( $("#id_is_recurrent").attr('checked') ) {
    	$("#recurrent_options").toggle();
    	$("#period_box").toggle();    	
    }
    
    /* --- Handle events --- */
    // Recurrent check box
	$("#id_is_recurrent").click(toggleRecurrent);
	
	// Autocomplete host name
	$(function() {
		var availableHosts = [
			"WWFCSUNIA007",
			"DEDE1APP0005",
			"FRFR1PXY0000",
			"JIT_Beaulieu",
			"HACMP_EAS_SAP_PRINT"
		];
		$( "#id_search_host" ).autocomplete({
			source: availableHosts
		});
	});
});
