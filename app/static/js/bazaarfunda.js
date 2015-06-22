var modelModelIDMap = {};
var prefQueue = [];

jQuery(document).ready(function(){



	jQuery('.skillbar').each(function(){
		jQuery(this).find('.skillbar-bar').animate({
			width:jQuery(this).attr('data-percent')
		},6000);
	});


	// Increase the count of the compare bucket
	jQuery("#add_to_compare").click(function() {
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

function filterOptions(leftColumn,price1,price2) {
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
  console.log(price1)
  if (price1 ) {
    newpriceRange.push(price1);
    newpriceRange.push(price2);
    
  }
  else {
      $currentURL = window.location.href;
      $priceRangeList = $currentURL.match(/pricerange=(.+)\&keyword/);
      if (!$priceRangeList){
        $priceRangeList = $currentURL.match(/pricerange=(.+)\&brands/); 
      } 
      if (!$priceRangeList){
        $currentURL = $currentURL + "&keyword";
        $priceRangeList = $currentURL.match(/pricerange=(.+)\&keyword/); 
      }
      if (!$priceRangeList){
        $currentURL = $currentURL + "&keyword";
        $priceRangeList = $currentURL.match(/pricerange=(.+)\#&keyword/); 
      }
      if (!$priceRangeList){
        $priceRangeList = $currentURL.match(/pricerange=(.+)\#&brands/); 
      } 
      if ($priceRangeList.length > 1) {
        $priceRange =  $priceRangeList[1]
        $priceRangeList = $priceRange.split(',');
        console.log($priceRangeList)
        var newPrice1 = $priceRangeList[0].replace("#","")
        var newPrice2 = $priceRangeList[1].replace("#","")
        newpriceRange.push(newPrice1.toString());
        newpriceRange.push(newPrice2.toString());
        }
      
      else {
        var newPrice1 = 200
        var newPrice2 = 60000
        newpriceRange.push(newPrice1.toString());
        newpriceRange.push(newPrice2.toString());
      }
  }
  console.log(newpriceRange)
  $domain = location.host
  $url =  "http://" + $domain + "/search?pricerange=";
  for (var i =0; i<newpriceRange.length; i++) { 
    $url = $url + newpriceRange[i] + ",";
  }
  
  if (newKeywordList.length != 0){
    $url = $url.slice(0,-1)
    $url = $url + "&keywords="
    for (var i =0; i<newKeywordList.length; i++) { 
      $url = $url + newKeywordList[i] + ",";
    }
  }
  if (newBrandList.length != 0) {
    $url = $url.slice(0,-1)
    $url = $url + "&brands="
    for (var i =0; i<newBrandList.length; i++) { 
      $url = $url + newBrandList[i] + ",";
    }
  }
  $url = $url.slice(0,-1)
  window.location = $url
  // console.log($url)
  // console.log(newBrandList)
  // console.log(newpriceRange)
  // console.log(newKeywordList)

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

        function searchForItemsMain() {
            queryString = document.getElementById("main-search-query").value;
            console.log(queryString);
            domain = location.host
            searchUrl =  "http://" + (domain + "/search/query?queryText=" + queryString);
            setTimeout(10000)
            window.location = searchUrl
            // window.open(searchUrl, "_self");
//            query?queryText="Apple Iphone 6"
//            setTimeout(continueExecution, 10000);
        }

        function searchForItemsSpy() {
            queryString = document.getElementById("search-query-spy").value;
            console.log(queryString);
            domain = location.host
            searchUrl =  "http://" + (domain + "/search/query?queryText=" + queryString);
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


function enable_buttons(theLink) {
  
  var str ="show_button";
  $("."+str).css("display","inline");
  
  var child=theLink.className;
  prefQueue.push(child)
  $("."+child).hide();
  //$("#"+name).parent().children().prop("disabled",true);
  //var last = parent.slice(-1);
  //$("#"+parent).prop("disabled",true);
  var name=theLink.id; //Taking ID
  console.log(prefQueue)
  console.log(name)
  var parent=$("#"+name).parent().attr("id"); //Taking Parent ID
  var lb_val=$("#"+name).val()//Taking value of radio
  $("#"+parent).hide().animate({right: '1000px'});  //Animate Parent ID
  var last = parent.slice(-1);//last char
  var lab="pref_l";
  var lb_id=lab.concat(last);//concat
  console.log(lb_id)
  $("#"+lb_id).html(lb_val);//setting label text
  //alert(lb_val);
  var last=Number(last)+1;
  //alert(last);
  var parent="pref-"
  var res = parent.concat(last);
  $("#"+res).show().animate({right: '0px'});
  
}

function enable_brand(theLink) {
  // console.log(theLink);
  // theLink.setAttribute("checked", "checked"); 
  var str ="choose_brand";
  
  $("#"+str).show().animate({right: '0px'});
}

function disable_brand(theLink) {
  // console.log(theLink);
  // theLink.setAttribute("checked", "checked"); 
  var str ="choose_brand";
  $("#"+str).hide().animate({right: '1000px'});
}



function reset_1() {
  prefQueue = []
  var child="Camera";
  $("."+child).parent().children().prop("disabled",false);
  $("."+child).parent().children().prop("checked", false);
  $("."+child).parent().children().show();
  //var str=$("#pref_l3").html();
  //alert(str);
  $("#pref-1").hide().animate({right: '1000px'});
  $("#pref-2").hide().animate({right: '1000px'});
  $("#pref-3").hide().animate({right: '1000px'});
  $("#pref-4").hide().animate({right: '1000px'});
  $("#pref-5").hide().animate({right: '1000px'});
  $("#pref-1").show().animate({right: '0px'});
  $("#pref_l1").html("");
  $("#pref_l2").html("");
  $("#pref_l3").html("");
  $("#pref_l4").html("");
  $("#pref_l5").html("");
  //var str=$("#pref_l1").html();
  //alert(str);
}

<!-- Initialize the multiselect plugin: -->

    $(document).ready(function() {
        $('#brand-list').multiselect();
    });

function enable_pref() {
  $("#pref-1").show().animate({right: '0px'});
}

<!-- Initialize the Filter Plugin: -->
 $(function() {
        $('#filter_search_1').fastLiveFilter('#filter_brand');
    $('#filter_search_2').fastLiveFilter('#filter_keyword');
    $('#filter_search_3').fastLiveFilter('#filter_model');
    
    });

 function reccomendMe() {
    var chooseBrand = document.getElementById("choose_brand");
    var display = chooseBrand.style.display
    brandList = []
    if (display == "block") {
      brandList = document.getElementsByClassName("multiselect dropdown-toggle btn btn-default");
      var brandText = brandList[0].title;
      var brandList = brandText.split(",");
      if (!brandList) {
        brandList = [brandText]
      }
    }
    var newpriceRange = []
    var prices = document.getElementsByClassName("infoBox");
    for (var i =0; i<prices.length; i++) {
        priceWithSign = prices[i].innerHTML
        newpriceRange.push(priceWithSign.replace("₹",""))
    }
    console.log(brandList)
    console.log(prefQueue)
    console.log(newpriceRange)

    $domain = location.host
    $url =  "http://" + $domain + "/search?pricerange=";
    for (var i =0; i<newpriceRange.length; i++) { 
      $url = $url + newpriceRange[i].replace('₹','') + ",";
    }
    weights = [];
    highest = 5;
    console.log(prefQueue)
    if (prefQueue.length != 0){
      $url = $url.slice(0,-1)
      $url = $url + "&keywords="
      for (var i =0; i<prefQueue.length; i++) { 
        weights.push(highest)
        highest --;
        $url = $url + prefQueue[i] + ",";
      }
    }
    if (brandList.length != 0) {
      $url = $url.slice(0,-1)
      $url = $url + "&brands="
      for (var i =0; i<brandList.length; i++) { 
        brand = brandList[i]
        brand = brand.trim()
        $url = $url + brand + ",";
      }
    }

    if (weights.length != 0){
      $url = $url.slice(0,-1)
      $url = $url + "&weights="
      for (var i =0; i<weights.length; i++) { 
        
        $url = $url + weights[i] + ",";
      }
    }
    $url = $url.slice(0,-1)
    window.location = $url
    console.log($url)

 }

 


  
        


            
            
