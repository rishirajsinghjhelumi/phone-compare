jQuery(document).ready(function(){
	jQuery('.skillbar').each(function(){
		jQuery(this).find('.skillbar-bar').animate({
			width:jQuery(this).attr('data-percent')
		},6000);
	});

	// Increase the count of the compare bucket
	$( "#add_to_compare" ).click(function() {
		$phoneID = $("div.PhoneObjectID").eq(0).text();
		$url = "../cart/add/" + $phoneID;
		$.ajax({url:$url ,
		dataType: 'json',
		success: function(data, status){
            if (data.status == 200) {
            	$( "span.badge" ).empty();
            	$( "span.badge" ).append(data.count);
            }

            else if (data.status == 512) {
            	// $("id.form-add_to_cart").append( 
            	// 	<div class="alert alert-success alert-dismissable" style="display: none;">
             //          <button class="close" data-dismiss="alert" type="button">×</button>
             //          <h3>Sorry!</h3>
             //           We can accomodate only 4 mobiles to be compared. Please remove one to add more.
             //        </div> 
             //        );
            	$("div.alert").css("display", "");
            }

        }});
	})


});
