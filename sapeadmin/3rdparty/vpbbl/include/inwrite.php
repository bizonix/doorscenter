<?
  //формируем меню новостей
	$news=makenews($array,$key);
	$templname=$_GET['tpl'];
//основной цикл записи
$map='<br><br>

';
$i = 1;
foreach ($array as $key=>$line){

	//формируем перелинковку
	$blockul=blockul($array);
	$blockol=blockol($array);
	//форумируем основное меню указывая не текущая ли страница открыта
	$menu=makemenu($array,$key);

	//формируем и записываем страницу
	//
	$smarty = new Smarty;

	$smarty->compile_check = true;
	$smarty->debugging = true;
	//$smarty->caching = true;
	$smarty->template_dir = "../templates";
	$smarty->compile_dir = "../compile";
	$smarty->cache_dir = "../cache";
	$smarty->config_dir = "../done/".$templname;
	$smarty->assign("name",$_GET['nn']);
	$smarty->assign("title",$array[$key]['title']);
	$smarty->assign("keywords",$array[$key]['keywords']);
	$smarty->assign("description",$array[$key]['description']);
	$smarty->assign("domen","#");
	$smarty->assign("slogan",$_GET['q']);
	$smarty->assign("m",$menu);
	$smarty->assign("content",$array[$key]['text']);
			if($_GET['type']=='html'){
	$smarty->assign("content",$array[$key]['text']);
	}else{
	$smarty->assign("content",$array[$key]['text'].'<? echo $content; ?>');
	}
	$smarty->assign("blockul",$blockul);
	$smarty->assign("blockol",$blockol);
	$smarty->assign("news",$news);
	$smarty->assign("year",date("Y",time()));
		if($_GET['type']=='html'){
	$smarty->assign("type","html");
	}else{
	$smarty->assign("type","php");
	}
	$content= $smarty->fetch('../done/'.$templname.'/index.html');
	if($_GET['type']=='html'){
	$fp = fopen ("../out/".$array[$key]['name'].".php", "w+");
	}else{
	$fp = fopen ("../out/".$array[$key]['name'].".php", "w+");
	}
	$map.="\r\n".'<a href="'.$array[$key]['name'].".php".'">'.$i.', </a>';
	$i++;
	fwrite ($fp, $content);
	fclose ($fp);
	echo 'Записываем во временную папку страницу №: [<b>'.($key+1).'</b>]'. "</b><br>\r\n";
	    echo '<script language="JavaScript">scrl(30)</script>';
		flush();

}
	$fp = fopen ("../out/map.php", "w+");
	fwrite ($fp, $map.'');
	fclose ($fp);
	if($_GET['type']=="php"){
if($_GET['sape']==true){
$news='\'\'';      //стоит после блока новостей
$block1='\'\'';    //блок номер один
$block2='\'\'';    //блок номер два, иногда отсутствует
$content= '\'\'';   //стоит после контента
$footer= '\'\'';
switch ($_GET['sapemesto']) {
  case "news":
$news='$sape->return_links()';
    break;
  case "block1":
$block1='$sape->return_links()';
    break;
  case "block2":
$block2='$sape->return_links()';
    break;
  case "content":
$content='$sape->return_links()';
    break;
  case "copy":
$footer='$sape->return_links()';
    break;
}
$inc='<?
//переменные которые доступны на сателлите
$news='.$news.';      //стоит после блока новостей
$block1='.$block1.';    //блок номер один
$block2='.$block2.';    //блок номер два, иногда отсутствует
$content= '.$content.';   //стоит после контента
$footer='.$footer.';    //стоит около копирайтов
?>';
}else{
$inc='<?
//переменные которые доступны на сателлите
$news=\'\';      //стоит после блока новостей
$block1=\'\';    //блок номер один
$block2=\'\';    //блок номер два, иногда отсутствует
$content= \'\';   //стоит после контента
$footer=\'\';    //стоит около копирайтов
?>';
}
			$fp = fopen ("../out/inc.php", "w+");
	fwrite ($fp, $inc);
	fclose ($fp);
	$index='';
	if($_GET['sape']==true){
		$index='<?php
if (!defined(\'_SAPE_USER\')){
define(\'_SAPE_USER\', \''.$_GET['sapecode'].'\');
}
require_once($_SERVER[\'DOCUMENT_ROOT\'].\'/\'._SAPE_USER.\'/sape.php\');
$sape = new SAPE_client();
?><?php
if (!defined(\'_SAPE_USER\')){
define(\'_SAPE_USER\', \''.$_GET['sapecode'].'\');
}
require_once($_SERVER[\'DOCUMENT_ROOT\'].\'/\'._SAPE_USER.\'/sape.php\');
$sape_context = new SAPE_context();
ob_start(array(&$sape_context,\'replace_in_page\'));
?>';
	}
	$index.='<?
include("inc.php");
if(strlen($_GET[\'q\'])<1){
$_GET[\'q\']="index";
}
$_GET[\'q\']=str_replace("http://","xxx",$_GET[\'q\']);
include($_GET[\'q\'].".txt");
?>';
	$fp = fopen ("../out/index.php", "w+");
	fwrite ($fp, $index);
	fclose ($fp);
	}
?>