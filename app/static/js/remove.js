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
	$("."+res).show();
}