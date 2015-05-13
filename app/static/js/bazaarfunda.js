var modelModelIDMap = {};
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
    

	});

  $('#choosePhone').click(function(){
    var brand  = document.getElementById("thebrand").value;
    var model =  document.getElementById("themodel").value;
    $phoneID = modelModelIDMap[model]["$oid"];
    console.log($phoneID);

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
              location.reload(); 
              window.open($compareURL, "_self");
            }

            else if (data.status == 256) {
              $( "span.badge" ).empty();
              $( "span.badge" ).append(data.phoneId.length);
              location.reload(); 
              window.open($compareURL, "_self");
            }

            else { 
              location.reload(); 
            }

            

        },
        
      });
      window.open($compareURL, "_self");

  }); 
          


       
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
      $currentURL = window.location.href;
      $currentURL = $currentURL.replace("#","");
      $currentURL = $currentURL + "/";
      $path = window.location.pathname + "/";

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
                  
                  var model = [];
                        
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
          // $('#themodel').html("Select Model...");
          console.log($brand);
          $currentURL = window.location.href
          $path = window.location.pathname
          $path = $path + "#";

          $getModelURL = $currentURL.replace($path, "/phone/brand/" + $brand);
          $getModelURL = $getModelURL.replace("#openModal", "");
          var data = httpGet($getModelURL);
          
          var key = "Model Name";
          var modelList = [];
          var jsonData = JSON.parse(data);
          for (var i = 0; i < jsonData.length; i++) {
              var modelName = jsonData[i][key];
              var modelID = jsonData[i]["_id"]
              modelList.push($brand + " " + modelName);
              modelModelIDMap[$brand + " " + modelName] = modelID;
          }
          console.log(modelModelIDMap);
          modelList.sort();

          $('#themodel').autocomplete({
                source: modelList,
                minLength: 0,
                scroll: true

            }).focus(function() {
                $(this).autocomplete("search", "");
            });
          
        }

        function httpGet(theUrl)
        {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", theUrl, false );
            xmlHttp.send( null );
            return xmlHttp.responseText;
        }

        


            
            
