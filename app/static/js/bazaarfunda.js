jQuery(document).ready(function(){



	jQuery('.skillbar').each(function(){
		jQuery(this).find('.skillbar-bar').animate({
			width:jQuery(this).attr('data-percent')
		},6000);
	});

	// Increase the count of the compare bucket
	$( "#add_to_compare" ).click(function() {
		$phoneID = $("div.PhoneObjectID").eq(0).text();
		$comarePath = "../cart/add/" + $phoneID;
    $currentURL = window.location.href
    $path = window.location.pathname
    
    $url = $currentURL.replace($path, "/cart/add/" + $phoneID); 
    $compareURL = $currentURL.replace($path, "/compare");
		$.ajax({url:$url ,
		dataType: 'json',
		success: function(data, status){
            if (data.status == 200) {
            	$( "span.badge" ).empty();
            	$( "span.badge" ).append(data.phoneId.length);
              window.open($compareURL);
            }

            else if (data.status == 256) {
              $( "span.badge" ).empty();
              $( "span.badge" ).append(data.phoneId.length);
              window.open($compareURL);
            }

            else if (data.status == 512) {
            	$("div.alert").css("display", "");
            }

        },
        
      });
    

	})

  $(".dropdown .title").click(function () {
  $(this).parent().toggleClass("closed");
});

$(".dropdown li").click(function () {
  $(this).parent().parent().toggleClass("closed").find(".title").text($(this).text());
});


});

function removeDiv(divId) {
   $("#"+divId).remove();
}

function removeByClass(className) {
   $("."+className).remove();
}

function click1(theLink, id) {
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
      $("."+res).show();
      $currentURL = window.location.href
      $path = window.location.pathname

      $removeURL = $currentURL.replace($path, "/cart/remove/" + id);
      $.ajax({url:$removeURL ,
      dataType: 'json',
      success: function(data, status){
              if (data.status == 200) {
                $( "span.badge" ).empty();
                $( "span.badge" ).append(data.phoneId.length);
                
              }

              else if (data.status == 512) {
                $("div.alert").css("display", "");
              }

          },
          
        });

}

 $(document).ready(function() {
            BindControls();

        });

        function BindControls() {
            var brand = ['Nokia', 
                'Apple', 
                'ASUS', 
                'HTC', 
                'Blackberry',
                'BQ', 
                'Samsung', 
                'Micromax', 
                'Karbonn', 
                'Spice', 
                'Xolo'];
                  
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

        function loadModelForBrand($brand) {
          console.log($(this).text());
          $currentURL = window.location.href
          $path = window.location.pathname

          $getModelURL = $currentURL.replace($path, "/phone/brand/" + $brand);

          $.ajax({url:$getModelURL ,
          dataType: 'json',
          success: function(data, status){
                  if (status == 200) {
                    console.log(data);
                    
                  }

                  
              },
              
            });
        }


            
            
