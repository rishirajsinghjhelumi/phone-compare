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

	$("#myModal").on("show", function () {
      $("body").addClass("modal-open");
    }).on("hidden", function () {
      $("body").removeClass("modal-open")
    });

    $("#recmodal").on("show", function () {
      $("body").addClass("modal-open");
    }).on("hidden", function () {
      $("body").removeClass("modal-open")
    });

    $("#compare_price").on("show", function () {
      $("body").addClass("modal-open");
    }).on("hidden", function () {
      $("body").removeClass("modal-open")
    });
    $("#compare_price0").on("show", function () {
      $("body").addClass("modal-open");
    }).on("hidden", function () {
      $("body").removeClass("modal-open")
    });


  $('#choosePhone').click(function(){
    var brand  = document.getElementById("thebrand").value;
    var model =  document.getElementById("themodel").value;
    $phoneID = modelModelIDMap[model]["$oid"];
    console.log($phoneID);

    $currentURL = window.location.href
    $path = window.location.pathname
    $path = $path + "#";
    
    $url = $currentURL.replace($path, "/cart/add/" + $phoneID); 
    httpGet($url);
    location.reload();
    $compareURL = $currentURL.replace($path, "/compare");
    // $.ajax({url:$url ,
    // dataType: 'json',
    // success: function(data, status){
    //         if (data.status == 200) {
    //           $( "span.badge" ).empty();
    //           $( "span.badge" ).append(data.phoneId.length);
    //           location.reload(); 
    //           window.open($compareURL, "_self");
    //         }

    //         else if (data.status == 256) {
    //           $( "span.badge" ).empty();
    //           $( "span.badge" ).append(data.phoneId.length);
    //           location.reload(); 
    //           window.open($compareURL, "_self");
    //         }

           

            

    //     },
        
    //   });
      // window.open($compareURL, "_self");

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

function filterOptions(leftColumn) {
  var brands = document.getElementsByName("brand");
  var newBrandList = []
  for (var i =0; i<brands.length; i++) {
    if (brands[i].checked) {
      newBrandList.push(brands[i].id)
    }
  }
  var keywords = document.getElementsByName("keyword");
  var newKeywordList = []
  for (var i =0; i<keywords.length; i++) {
    if (keywords[i].checked) {
      newKeywordList.push(keywords[i].id)
    }
  }
  var newpriceRange = []
  var prices = document.getElementsByClassName("infoBox");
  for (var i =0; i<prices.length; i++) {
      newpriceRange.push(prices[i].innerHTML)
    
  }
  $domain = location.host
  $url =  "http://" + $domain + "/search?pricerange=";
  for (var i =0; i<newpriceRange.length; i++) { 
    $url = $url + newpriceRange[i].replace('₹','') + ",";
  }
  $url = $url.slice(0,-1)
  $url = $url + "&keywords="
  for (var i =0; i<newKeywordList.length; i++) { 
    $url = $url + newKeywordList[i] + ",";
  }
  $url = $url.slice(0,-1)
  $url = $url + "&brands="
  for (var i =0; i<newBrandList.length; i++) { 
    $url = $url + newBrandList[i] + ",";
  }
  $url = $url.slice(0,-1)
  window.location = $url
  console.log($url)
  console.log(newBrandList)
  console.log(newpriceRange)
  console.log(newKeywordList)

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
            populateAutoComplete()

        });

        function populateAutoComplete() {
          $domain = location.host
            $url =  "http://" + $domain + "/phone/autocomplete";
            // data = httpGet($url).results;
            // var jsonData = JSON.parse(data);
            // phoneList = jsonData.results
            // console.log(phoneList)
            // $('#search-query').autocomplete({
            //     source: phoneList,
            //     minLength: 0,
            //     scroll: true
            // }).focus(function() {
            //     $(this).autocomplete("search", "");
            // });

            $.ajax({
                url: $url
                }).done(function (data) {
                    $('#main-search-query').autocomplete({
                        source: data.results,
                        minLength: 2
                    }).focus(function() {
                $(this).autocomplete("search", "");
            });
                });
            };


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

        function addToCompareFromListing(phoneID) {

            $domain = location.host


            $url =  "http://" + $domain + "/cart/add/" + phoneID;
            $compareURL = "http://" +  $domain +  "/compare";
            console.log($url)
            console.log($compareURL)

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

            console.log(phoneID)
        }

        function searchForItems() {
            queryString = document.getElementById("main-search-query").value;
            console.log(queryString);
            domain = location.host
            searchUrl =  "http://" + (domain + "/query?queryText=" + queryString);
            setTimeout(10000)
            window.location = searchUrl
            // window.open(searchUrl, "_self");
//            query?queryText="Apple Iphone 6"
//            setTimeout(continueExecution, 10000);
        }

        <!-- Initialize the Filter Plugin: -->
 $(function() {
        $('#filter_search_1').fastLiveFilter('#filter_brand');
    $('#filter_search_2').fastLiveFilter('#filter_keyword');
    $('#filter_search_3').fastLiveFilter('#filter_model');
    
    });

        


            
            
