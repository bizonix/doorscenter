<?php 
  if (!defined('_SAPE_USER')){
    define('_SAPE_USER', 'xxx'); 
  }
  //require_once($_SERVER['DOCUMENT_ROOT'].'/'._SAPE_USER.'/sape.php'); 
  require_once(_SAPE_USER.'/sape.php'); 
  //$sape = new SAPE_client();

  $sape_venality_name=array();
  $allowed_pages=array();
  $allowed_var=array("");
  $tm=explode("?",$_SERVER['REQUEST_URI']);
  if (isset($tm[1]) and $tm[0]==str_replace($allowed_pages,"",$tm[0])) {
    $k=preg_match_all("/(.*)=(.*)\&/Uis",$tm[1]."&",$am);
    $bm=array();
    for ($i=0; $i < $k; $i++) {
      if ($am[2][$i]=="" or !in_array($am[1][$i],$allowed_var))continue;
      $bm[]=$am[1][$i]."=".$am[2][$i];
    }
    $tm[1]=implode("&",$bm);
    $sape_venality_name['request_uri']=
    $_SERVER['REQUEST_URI']=($tm[1]=="") ? $tm[0]: implode("?",$tm);
  }
  $sape = new SAPE_client($sape_venality_name);

  echo $sape->return_links();
  
  if (strstr($_SERVER['HTTP_USER_AGENT'], 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)')){ 
    $bot='a';
  }
  if ($bot !=""){
    $b_data = "botsxxx.dat";
    $data = fopen($b_data, "a");
    fwrite($data, "\r\n");
    fclose($data);
  } 
?>
