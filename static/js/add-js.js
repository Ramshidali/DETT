$('.btn-gst').click(function (e) {
			e.preventDefault();

			current_button = $(this).attr('data-type')
			console.log(current_button);
			url = $(this).attr('data-url');

			input_type_value = $('#code_type')

			if(current_button === 'hsn'){
				$('.btn-asc').css({
			    'background':'#2196f3',
			    'box-shadow': 'none',
			})
			    $(this).css({
			        'background':'red',
			        'box-shadow':' 0px 0px 15px 0px red',

			    });

			    input_type_value.attr('value','hsn');
			    getHsnSuggestions(url);

			}else{

			input_type_value.attr('value','asc');

			$('.btn-hsn').css({
			    'background':'#2196f3',
			    'box-shadow': 'none'
			});
			    $(this).css({
			        'background':'red',
			         'box-shadow':' 0px 0px 15px 0px red',
			    });
			}

			getAscSuggestions(url);

			$('.forms-gst').css({
			    'display':'block'
			});

});


function getHsnSuggestions(url) {


   $("#id_code").keyup(function(event) {

     var code = $("#id_code").val();
     $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        data: {
            code:code,
        },

        success: function (data) {

                $('#gst_suggestions').text("Loading");
                var value = data['code']
                var isData = data['data']

                igst = $('#id_igst');
                cgst = $('#id_cgst');
                sgst = $('#id_sgst');

                console.log(isData);

                $('#gst_suggestions').text("Suggestions are :-"+value);
                if(isData =='yes'){
                    igst.val(data['igst']);
                    cgst.val(data['cgst']);
                    sgst.val(data['sgst']);
                } else {
                    igst.val('0');
                    cgst.val('0');
                    sgst.val('0');
                }
        },

        error: function (data) {
            var title = "An error occurred";
            var message = "An error occurred. Please try again later.";
            swal(title, message, "error");
            console.log(data)
        }
    });
});

}


function getAscSuggestions(url) {

    console.log(url);
   $("#id_code").keyup(function(event) {

     var code = $("#id_code").val();
     $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        data: {
            type:"asc",
            code:code,
        },

        success: function (data) {

                $('#gst_suggestions').text("Loading");
                var value = data['code']
                var isData = data['data']

                igst = $('#id_igst');
                cgst = $('#id_cgst');
                sgst = $('#id_sgst');

                console.log(isData);

                $('#gst_suggestions').text("Suggestions are :-"+value);
                if(isData =='yes'){
                    igst.val(data['igst']);
                    cgst.val(data['cgst']);
                    sgst.val(data['sgst']);
                } else {
                    igst.val('0');
                    cgst.val('0');
                    sgst.val('0');
                }
        },

        error: function (data) {
            var title = "An error occurred";
            var message = "An error occurred. Please try again later.";
            swal(title, message, "error");
            console.log(data)
        }
    });
});

}
