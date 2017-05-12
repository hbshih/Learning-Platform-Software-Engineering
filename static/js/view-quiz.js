var locked = false;

$('form').on('submit', function(e) {
	e.preventDefault();
	if (locked === true) {
		return;
	}
	locked = true;
	var data = {}, answers = [];
	var input = $('input[name="answer"]');
	input.each(function(e) {
		answers.push($(this).val());
	});
	data.answers = JSON.stringify(answers);
	$.ajax({
		method: 'post',
		data: data,
		complete: function(rs) {
			var data = rs.responseText;
			try {
				data = JSON.parse(data);
			} catch (e) {
				locked = false;
				return;
			}
			input.each(function(i, val) {
				if (data[i].correct === true) {
					$(this).addClass('bg-success');
				} else {
					$(this).addClass('bg-danger');
				}
				$(this).after('<div style="margin-top:5px"><label>Answer:</label> ' + data[i].answer + '</div>');
			});
			$('input[type="submit"]').remove();
			console.log(data);
			locked = false;
		}
	});
});
