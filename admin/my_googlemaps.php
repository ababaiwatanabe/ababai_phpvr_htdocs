<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja" dir="ltr"><!-- InstanceBegin template="/Templates/index.dwt" codeOutsideHTMLIsLocked="false" -->
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="Content-Script-Type" content="text/javascript" />
<style type="text/css">
	html{width:800px;height: 400px;font-size:12px;}
	body{height: 400px; margin: 0px; padding: 0px;font-size:12px; }
	#map{width: 550px;height:400px;float:left;}
	#control{padding-left:20px;width:230px;float:left;}
</style>
<script type="text/javascript" src="./scripts/jquery-1.7.2.min.js"></script>
<script src="http://maps.google.com/maps/api/js?v=3&sensor=false" type="text/javascript" charset="UTF-8"></script>

<script type="text/javascript">
//<![CDATA[
var map;
$(document).ready(function(){
	var cord = $("#<?php echo $_GET['id']?>",parent.document).val().split(",");
	if (cord[0] == ''){
		$('#lat').val(35.226063);
		$('#lng').val(137.098233);
	}else{
		$('#lat').val(cord[0]);
		$('#lng').val(cord[1]);
	}
	


	var latlng = new google.maps.LatLng($("#lat").val(), $("#lng").val());
	var opts = {
		zoom: 16,
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		center: latlng
	};
	map = new google.maps.Map(document.getElementById("map"), opts);
	geo = new google.maps.Geocoder();

	var markerOpts = {
		position: new google.maps.LatLng($("#lat").val(), $("#lng").val()),
		map: map,
		draggable: true
	};
	var marker = new google.maps.Marker(markerOpts);
	
	google.maps.event.addListener(map, 'click', myMapClickEventFunc);
	google.maps.event.addListener(marker, 'dragend', myMarkerDragendEventFunc);

	function myMapClickEventFunc(event){//mapクリック
		map.panTo(event.latLng);
	}
	function myMarkerDragendEventFunc(event){//マーカードラッグ終了
		var p = marker.position;
		$('#lat').val(p.lat()); 
		$('#lng').val(p.lng());
	}

	$("#getLatLngByAddress").click(function(){
		var req = {
			address: $("#address").val(),
		};
		geo.geocode(req, geoResultCallback);
	});
	
	$('#setcord').click(function(){
		$("#<?php echo $_GET['id']; ?>",parent.document).val($('#lat').val()+','+$('#lng').val());
		parent.$.fancybox.close();
	});

	function geoResultCallback(result, status) {
		if (status != google.maps.GeocoderStatus.OK) {
			alert(status);
			return;
		}
		var latlng = result[0].geometry.location;
		map.setCenter(latlng);
		marker.position = latlng;
		marker.setMap(map);

		$('#lat').val(latlng.lat()); 
		$('#lng').val(latlng.lng());
	}

});

//]]>
</script>
</head>
<body>

<div id="map"></div>
<div id="control">
	<p><input type="text" value="" id="address" style="width:220px;"></p>
	<p><input type="button" value="住所から検索" id="getLatLngByAddress"></p>
<br />
	<p>緯度：<input type="text" value="" id="lat"></p>
	<p>経度：<input type="text" value="" id="lng"></p>
	<p><input type="button" value="確定" id="setcord"></p>
	<p style="font-size:12px;">
	住所を入力して「住所から検索」ボタンを押すと、その場所に移動します。<br />
	場所が見つからない場合は丁目、番地等を消して検索してみて下さい。<br />
	マーカーアイコンをドラッグ＆ドロップで微調整できます。<br />
	場所が決まったら「確定」ボタンをクリックして完了です。
	</p>
</div>
</body>
</html>
