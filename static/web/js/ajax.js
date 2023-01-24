$("#submit_phone").click(function (e) {
	e.preventDefault();

	fname = $("#login_name").val();
	phone = $("#signup_sec #login-phone").val();
    
    console.log(phone)

	var filter = /^\d*(?:\.\d{1,2})?$/;
	filter_test = filter.test(phone);
	console.log(filter_test);

	$("#required_text_name").css({
		display: "none",
	});
    $("#required_text_phone").css({
		display: "none",
	});

    if (fname.length === 0) {
		$("#required_text_name").css({
			display: "block",
		});
    } else if (phone.length == 0) {
		$("#required_text_phone").css({
			display: "block",
		});
	} else if (filter_test == false) {
		$("#required_text_phone").css({
			display: "block",
		});
		$("#required_text_phone").html("enter correct phone number");
	} else if (phone.length > 10) {
		$("#required_text_phone").css({
			display: "block",
		});
		$("#required_text_phone").html(
			"Enter a valid number, seen like you entered phone number greater than 10"
		);
	} else if (phone.length < 10) {
		$("#required_text_phone").css({
			display: "block",
		});
		$("#required_text_phone").html(
			"Enter a valid number, seen like you entered phone number less than 10"
		);
	} else {
		url = $(this).attr("data-url");

		console.log(phone);
		console.log(fname);

		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			data: {
				phone: phone,
			},

			success: function (data) {
				if (data["status"] == "true") {
					
					$(".signup-phone").css("display", "none");
                    $(".verify-otp").css({display: "block",});

					$(".sub-text #number").html(phone);
					$("#user_name").attr("value",fname);
				}

				if (data["status"] == "6001") {
					if (data["condition_status"] == "phone_already_exists") {
						$("#required_text_phone").css({
							display: "block",
						});
						$("#required_text_phone").html(data["message"]);
					}
				}
			},

			error: function (data) {},
		});
	}
});


$("#phone_login").click(function (e) {
	e.preventDefault();

	phone = $("#signin_sec #login-phone").val();
    
    console.log(phone)

	var filter = /^\d*(?:\.\d{1,2})?$/;
	filter_test = filter.test(phone);
	console.log(filter_test);

	
    $("#required_text_phone").css({
		display: "none",
	});

    if (phone.length == 0) {
		$("#required_text_phone").css({
			display: "block",
		});
	} else if (filter_test == false) {
		$("#required_text_phone").css({
			display: "block",
		});
		$("#required_text_phone").html("enter correct phone number");
	} else if (phone.length > 10) {
		$("#required_text_phone").css({
			display: "block",
		});
		$("#required_text_phone").html(
			"Enter a valid number, seen like you entered phone number greater than 10"
		);
	} else if (phone.length < 10) {
		$("#required_text_phone").css({
			display: "block",
		});
		$("#required_text_phone").html(
			"Enter a valid number, seen like you entered phone number less than 10"
		);
	} else {
		url = $(this).attr("data-url");

		console.log(phone);
		console.log(url);

		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			data: {
				phone: phone,
			},

			success: function (data) {
				if (data["status"] == "true") {
					
					$("#signin_sec").css("display", "none");
                    $(".verify-otp").css({display: "block",});

					$(".sub-text #number").html(phone);
				}

				if (data["status"] == "6001") {
					if (data["condition_status"] == "phone_already_exists") {
						$("#required_text_phone").css({
							display: "block",
						});
						$("#required_text_phone").html(data["message"]);
					}
				}
			},

			error: function (data) {},
		});
	}
});



$("#otp_validation").click(function (e) {
	e.preventDefault();
	$("#required_text_otp").css({
		display: "none",
	});

	if (
		$("#otp_one").val().length === 0 &&
		$("#otp_two").val().length === 0 &&
		$("#otp_three").val().length === 0 &&
		$("#otp_four").val().length === 0
	) {
		$("#required_text_otp").css({
			display: "block",
		});
	} else {
		fname = $("#user_name").val();
		phone = $(".sub-text #number").html();
		otp_one = $("#otp_one").val();
		otp_two = $("#otp_two").val();
		otp_three = $("#otp_three").val();
		otp_four = $("#otp_four").val();

		url = $(this).attr("data-url");

		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			data: {
				fname: fname,
				phone: phone,
				otp_one: otp_one,
				otp_two: otp_two,
				otp_three: otp_three,
				otp_four: otp_four,
			},

			success: function (data) {
				if (data["status"] == "true") {
					window.location.reload();
				}

				if (data["status"] == "false") {
					if (data["condition_status"] == "not_match") {
						$("#required_text_otp").css({
							display: "block",
						});
						$("#required_text_otp").html(data["message"]);
					}
				}
			},

			error: function (data) {
				//    console.log("errrorrrr")
			},
		});
	}
});


$("#addAddressBtn").click(function (e) {
	e.preventDefault();
	$(".add-address-modal").css({
		display: "block",
	});
});


function change_address(id) {
	// console.log(id);
	url = $("#"+id).attr("data-url");
	// console.log(url);

	$.ajax({
		type: "GET",
		url: url,
		dataType: "json",

		success: function (data) {
			if (data["status"] == "true") {
				window.location.reload();
			}
		},

		error: function (data) {
			//    console.log("errrorrrr")
		},
	});
}

// edit address
function edit_address(id) {
	// console.log(id);
	url = $("#btn"+id).attr("data-url");
	update_url = $("#btn"+id).attr("data-update_url");
	// console.log(url);

	$.ajax({
		type: "GET",
		url: url,
		dataType: "json",

		success: function (data) {
			if (data["status"] == "true") {
				// console.log(data["data"])
				fname = data.data.name
				phone = data.data.phone
				pincode = data.data.pincode
				street = data.data.street
				city = data.data.city
				landmark = data.data.landmark
				state = data.data.state
				address_line1 = data.data.address_line1
				address_type = data.data.address_type
				console.log(update_url);

				$(".add-address-modal #address_form").attr("action",update_url)

				$(".add-address-modal #id_name").attr("value",fname)
				$(".add-address-modal #id_phone").attr("value",phone)
				$(".add-address-modal #id_pincode").attr("value",pincode)
				$(".add-address-modal #id_street").attr("value",street)
				$(".add-address-modal #id_city").attr("value",city)
				$(".add-address-modal #id_landmark").attr("value",landmark)
				$(".add-address-modal #id_state").attr("value",state)
				$(".add-address-modal #id_address_line1").val(address_line1)

				if (address_type == "home") {
					$(".add-address-modal #at_home").prop("checked", true)
				}
				if (address_type == "office") {
					$(".add-address-modal #at_office").prop("checked", true)
				}

				$(".add-address-modal").css({
					display: "block",
				});
			}
		},

		error: function (data) {
			//    console.log("errrorrrr")
		},
	});
}
