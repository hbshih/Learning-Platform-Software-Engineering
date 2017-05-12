$('#add').on('click', function(e) {
	function buildInput(string) {
		return '<div class="row form-group">' +
			'<div class="col-xs-12 col-sm-2">' +
			string.charAt(0).toUpperCase() + string.slice(1) + ':' +
			'</div>' +
			'<div class="col-xs-12 col-sm-10">' +
			'<input class="form-control" name="' + string + '">' +
			'</div>' +
			'</div>';
	}

	function buildQuestionAndAnswer(index) {
		return '<div class="form-group" data-index="' + index + '" style="display:none;">' +
			'<label>Q.' + (index + 1) + '</label>' +
			buildInput('question') +
			buildInput('answer') +
			'</div>';
	}

	var last = $('.form-box').children().last().prev().prev().prev();
	var index = last.data('index') + 1;
	var content = buildQuestionAndAnswer(index);
	last.after(content);
	last.next().slideDown();
	if ($('#remove').css('display') == 'none') {
		$('#remove').show();
	}
});

$('#remove').on('click', function(e) {
	var last = $('.form-box').children().last().prev().prev().prev();
	var index = last.data('index');
	if (index == 1) {
		$('#remove').hide();
	}
	last.slideUp(function(e) {
		last.remove();
	});
});

$('form').on('submit', function(e) {
	e.preventDefault();
	var data = {}, questions = [], answers = [];
	$('input[name="question"]').each(function(e) {
		questions.push($(this).val());
	});
	$('input[name="answer"]').each(function(e) {
		answers.push($(this).val());
	});
	data.questions = JSON.stringify(questions);
	data.answers = JSON.stringify(answers);
	$.ajax({
		method: 'post',
		data: data,
		complete: function(rs) {
			window.location = rs.responseText;
		}
	});
});
