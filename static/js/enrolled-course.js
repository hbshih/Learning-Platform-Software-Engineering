$('.table-list .content .module-list').on('click', function(e) {
	var target = $(this).next();
	var caret = $(this).find("h3 small i").first();
	if (target.css('display') == 'none') {
		caret.removeClass('fa-caret-right');
		caret.addClass('fa-caret-down');
		target.slideDown();
	} else {
		caret.removeClass('fa-caret-down');
		caret.addClass('fa-caret-right');
		target.slideUp();
	}
});
