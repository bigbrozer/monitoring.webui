/*
** Javascript for Downtime web app
** Author: Vincent BESANCON <besancon.vincent@gmail.com>
*/

/*
================================================================================
 _____                 _   _                 
|  ___|   _ _ __   ___| |_(_) ___  _ __  ___ 
| |_ | | | | '_ \ / __| __| |/ _ \| '_ \/ __|
|  _|| |_| | | | | (__| |_| | (_) | | | \__ \
|_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

================================================================================
*/
function toggleRecurrent() {
	$("#recurrent_options").toggle();
	$('#recurrent_options input[type=checkbox]').attr('checked', false);
	$('#id_start_time').attr('value', "");
	$('#id_end_time').attr('value', "");
	
	// Disable Start and End period input if recurrent
	$("#period_box").toggle();
	$('#id_start_period').attr('value', "");
	$('#id_end_period').attr('value', "");
}

/*
================================================================================
 __  __       _       
|  \/  | __ _(_)_ __  
| |\/| |/ _` | | '_ \ 
| |  | | (_| | | | | |
|_|  |_|\__,_|_|_| |_|

================================================================================
*/
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
		function split( val ) {
			return val.split( /,\s*/ );
		}
		function extractLast( term ) {
			return split( term ).pop();
		}

		$( "#id_host_list" )
			// don't navigate away from the field on tab when selecting an item
			.bind( "keydown", function( event ) {
				if ( event.keyCode === $.ui.keyCode.TAB &&
						$( this ).data( "autocomplete" ).menu.active ) {
					event.preventDefault();
				}
			})
			.autocomplete({
				source: function( request, response ) {
					$.getJSON( "/optools/nagios/hosts/search", {
						term: extractLast( request.term )
					}, response );
				},
				search: function() {
					// custom minLength
					var term = extractLast( this.value );
					if ( term.length < 2 ) {
						return false;
					}
				},
				focus: function() {
					// prevent value inserted on focus
					return false;
				},
				select: function( event, ui ) {
					var terms = split( this.value );
					// remove the current input
					terms.pop();
					// add the selected item
					terms.push( ui.item.value );
					// add placeholder to get the comma-and-space at the end
					terms.push( "" );
					this.value = terms.join( ", " );
					this.value = terms;
					return false;
				}
			});
	});
});
