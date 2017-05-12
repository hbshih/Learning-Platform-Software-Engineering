function checkPassword(password, confirmPassword) {
	if (password.val().length === 0 || confirmPassword.val().length === 0) {
		return -1;
	}
	if (password.val() != confirmPassword.val()) {
		return -2;
	}
	return 0;
}

function checkUsername(username) {
	if (username.val().length === 0) {
		return -1;
	}
	if (username.val().length != 8) {
		return -2;
	}
	if (!/^[a-zA-Z0-9_-]+$/.test(username.val())) {
		return -3;
	}
	return 0;
}

$('input[name="username"]').on("keyup", function(e) {
	var username = $(this);
	username.removeClass("bg-success");
	username.removeClass("bg-danger");
	var result = checkUsername(username);
	if (result === 0) {
		username.addClass("bg-success");
	} else if (result != -1) {
		username.addClass("bg-danger");
	}
});

$('input[name="password"], [name="confirm-password"]').on("keyup", function(e) {
	var password = $('input[name="password"]');
	var confirmPassword = $('input[name="confirm-password"]');
	password.removeClass("bg-success");
	password.removeClass("bg-danger");
	confirmPassword.removeClass("bg-success");
	confirmPassword.removeClass("bg-danger");
	var result = checkPassword(password, confirmPassword);
	if (result === 0) {
		password.addClass("bg-success");
		confirmPassword.addClass("bg-success");
	} else if (result == -2) {
		password.addClass("bg-danger");
		confirmPassword.addClass("bg-danger");
	}
});

$('input[name="name"]').on("keyup", function(e) {
	var name = $('input[name="name"]');
	if (name.val().length !== 0) {
		name.removeClass("bg-danger");
	}
});

$('form').on("submit", function(e) {
	var username = $('input[name="username"]');
	var password = $('input[name="password"]');
	var confirmPassword = $('input[name="confirm-password"]');
	var name = $('input[name="name"]');
	if (checkUsername(username) !== 0) {
		username.addClass("bg-danger");
		return false;
	}
	if (checkPassword(password, confirmPassword) !== 0) {
		return false;
	}
	if (name.val().length === 0) {
		name.addClass("bg-danger");
		return false;
	}
});
