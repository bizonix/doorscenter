<?
error_reporting  (0);
ini_set("max_execution_time",3000);
ini_set("allow_url_fopen",true);
include("../confbd.php");
include("../include/bd.php");
include("../config.php");            //подключаем функции
include("function.php");            //подключаем функции
include("Snoopy.class.php");            //подключаем функции
include("Smarty.class.php");            //подключаем функции
require_once('pclzip.lib.php');

//загружаем страницы или картинки
include("getf.php");
//парсим поисковик
    echo '
    <style  type=text/css>body
{
font-family:Verdana;
font-size:8pt;
}

</style>

    <script language="JavaScript">
<!--
tr=0
function scrl(x) {self.scrollTo(0, tr+x)
tr=tr+x
}
// -->
</script>';

//парсим картинки
if(($_GET['step']!=2)and($_GET['pre']=="true")){
	include("images.php"); //подгатавливается массив изображений $images
	echo "\r\n<br><a TARGET='_blank' href=\"pre.php\">Премодерация</a>";
	echo '<form method="get">';
	echo '<input name="step" type="hidden" value="2">
	';
	foreach($_GET as $key=>$value){
	if($key!="step")	echo '<input name="'.$key.'" type="hidden" value="'.$value.'">
	';	}

	echo '
<input type="submit" value="Продолжить">
</form>';
	exit();
}elseif($_GET['pre']!="true"){	include("images.php"); //подгатавливается массив изображений $images}else{	       $sql="SELECT *
FROM `text`";
  $result1 = $db->sql_query($sql);
  $num=$db->sql_numrows($result1);
  for ($i=0; $i<$num; $i++) {
$arr=$db->sql_fetchrow($result1);
$outtitle[]=$arr['title'];
$outurl[]=$arr['url'];
$outcontent[]=$arr['text'];
  }
	       $sql="SELECT `url`
FROM `pic`";
  $result1 = $db->sql_query($sql);
  $num=$db->sql_numrows($result1);
  for ($i=0; $i<$num; $i++) {
$arr=$db->sql_fetchrow($result1);
$images[]=$arr['url'];
  }
  switch ($_GET['picture']) {
  case "po12":
   $countpicture=ceil(count($outtitle)*1.5);
    break;
  case "po02":
   $countpicture=count($outtitle);
    break;
  case "po03":
   $countpicture=ceil(count($outtitle)*1.5);
    break;
  case "all":
    $countpicture=ceil(count($outtitle));
    break;
  case "on2":
   $countpicture=ceil(count($outtitle)*0.5);
    break;
  case "on3":
   $countpicture=ceil(count($outtitle)*0.35);
    break;
  case "po2":
   $countpicture=ceil(count($outtitle)*2);
    break;
  case "no":
   $countpicture=0;
    break;
}
}
//обрабатываем синонимайзером
    include("sinonim.php");  //на выход имееем массив $array
//обрабатываем переводчиком
    include("translate.php");  //на выход имееем массив $array
//готовим данные для сателлита
    include("dataform.php");  //на выход имееем массив $array
//если нужно синонимизируем
//если нужно уникализируем

//вставляем в шаблон
    include("inwrite.php");
    //записываем
    include("inzip.php");
//делаем редирект на шаблон вместо прогресс бара
?>