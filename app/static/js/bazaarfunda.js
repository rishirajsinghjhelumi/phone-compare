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

function removeDiv(divId) {
   $("#"+divId).remove();
}

function removeByClass(className) {
   $("."+className).remove();
}

function click1(theLink) {
    var data=theLink.className.split(' ')[0];
    //var data = ev.dataTransfer.getData("text");
    //ev.target.appendChild(document.getElementById(data));
      //document.getElementById("demo").innerHTML = res;
      removeByClass(data);
      var last = data.slice(-1);
      var str ="hide";
      var res = str.concat(last);
      //var elem = document.getElementByClassName(res);
      //elem.style.display='block';
	console.log(res);
      $("."+res).show();
}

 $(document).ready(function() {
            BindControls();
        });

        function BindControls() {
            var brand = ['ARGENTINA', 
                'AUSTRALIA', 
                'BRAZIL', 
                'BELARUS', 
                'BHUTAN',
                'CHILE', 
                'CAMBODIA', 
                'CANADA', 
                'CHILE', 
                'DENMARK', 
                'DOMINICA'];
                  
                  var model = ['MI3', 
                'MI4', 
                'XT1033', 
                'REDMI1S', 
                'MOTO-G',
                'MOTO-G2', 
                'CAMBODIA', 
                'CANADA', 
                'CHILE', 
                'DENMARK', 
                'DOMINICA'];
                        
                   $('#themodel').autocomplete({
                source: model,
                minLength: 0,
                scroll: true
            }).focus(function() {
                $(this).autocomplete("search", "");
            });
                  

            $('#thebrand').autocomplete({
                source: brand,
                minLength: 0,
                scroll: true
            }).focus(function() {
                $(this).autocomplete("search", "");
            });
                  
                  $(window).resize(function() {
                  $(".ui-autocomplete").css('display', 'none');
                  
                  });
        }
            
            
