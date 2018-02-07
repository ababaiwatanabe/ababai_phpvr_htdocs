<?php
if(isset($_GET["x"]) && isset($_GET["y"])) {
//	require_once './Jsphon/Decoder.php';
//	$getCont = file_get_contents("http://express.heartrails.com/api/json?method=getStations&x=".$_GET["x"].'&y='.$_GET["y"]);
//$json = new Jsphon_Decoder();
//$result = $json->decode($getCont);
	$retInfoArr = json_decode(file_get_contents("http://express.heartrails.com/api/json?method=getStations&x=".$_GET["x"].'&y='.$_GET["y"]),true);
	$retInfoArr = $retInfoArr['response']['station'];
	$retStr = '';

  foreach ($retInfoArr as $info){
    $retStr .= $info[line].' ';
    $retStr .= $info[name].' [';
    $retStr .= $info[distance]."]\n";
  }
  print ($getCont);

}
?>