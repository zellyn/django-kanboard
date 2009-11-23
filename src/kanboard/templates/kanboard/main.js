/*
    // Clean version
    $(function() {
      $('.sortable').sortable({connectWith: '.sortable'}).disableSelection();
    });
//*/
//*
function resize_board() {
	var height = $(window).height() - $('#top').outerHeight() - $('#bottom').outerHeight();
	height = height > 200 ? height : 200;
	var width = $('#board').width();
	var columns = $('#board .column').length;
	var col_width = parseInt(width / columns);
	var last_width = width - (col_width * (columns - 1)) - 18;
	$('#board .column').each(function(i) {
		var head_height = $('h2', this).outerHeight();
		$('ul', this).height(height - head_height - 2);  // -2 for the 2px of vertical padding on the ul
		$(this).width(i == columns - 1 ? last_width : col_width);
	});
}

$(function() {
	var debug = function(msg) {
		$('#messages').append('<li>' + msg + '</li>');
	};
	$('.sortable').sortable({
		connectWith: '.sortable',
		stop: function(e, ui) {
		var sender = ui.sender ? ui.sender[0].id : "(none)";
		var item = ui.item[0].id;
		var target = e.target.id;
		debug('ui.sender=' + sender + ', item=' + item + ', target=' + target);
		var data = {};
		$('ul.phase').each(function() {
			data[this.id] = $.map($(this).find('li.card'), function(y) { return y.id})
		});
		// TODO:zjh - add error function to display debug info
		$.post('update/', data);
	}
	}).disableSelection();
	resize_board();
	$(window).bind('resize', resize_board);
});
//*/

