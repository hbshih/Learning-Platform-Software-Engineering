$('button').on('click', function(e) {
	e.preventDefault();
});

$('#deleteModal').on('show.bs.modal', function(e) {
	var button = $(e.relatedTarget);
	var id = button.data('id');
	var name = button.data('name');
	$('#deleteModal .modal-body font').html(name);
	$('#deleteModal .modal-footer a').attr('href', './delete/' + id);
});
