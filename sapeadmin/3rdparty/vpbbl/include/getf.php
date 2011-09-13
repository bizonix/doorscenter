<?
ini_set("user_agent","Yandex/1.01.001 (compatible; Win16; P)");
//если запрошен с параметром для получения страниц то получаем и записываем страницу!
if($_GET['cmd']=="getpic"){

ini_set("default_socket_timeout","120");
       $sql="SELECT *
FROM `pic`
WHERE `id` LIKE '".$_GET['url']."'";
  $result1 = $db->sql_query($sql);
  $arr=$db->sql_fetchrow($result1);
$page=file_get_contents3($arr['url']);
       $sql="UPDATE `pic` SET `pic` = '".mysql_escape_string($page)."' WHERE `id` =".$_GET['url']." LIMIT 1 ;
";
  $result1 = $db->sql_query($sql);
       $sql="UPDATE `pic` SET `pars` = '1' WHERE `id` =".$_GET['url']." LIMIT 1 ;
";
  $result1 = $db->sql_query($sql);

	exit();
}


//если запрошен с параметром для получения страниц то получаем и записываем страницу!
if($_GET['cmd']=="getpage"){
	include("page.function.php");
ini_set("default_socket_timeout","120");
       $sql="SELECT *
FROM `text`
WHERE `id` LIKE '".$_GET['url']."'";
  $result1 = $db->sql_query($sql);
  $arr=$db->sql_fetchrow($result1);
$page=file_get_contents2($arr['url']);
if(strlen($page)>100){
       $sql="UPDATE `text` SET `text` = '".mysql_escape_string(charset_x_win(getcontent($page)))."' WHERE `id` =".$_GET['url']." LIMIT 1 ;
";
  $result1 = $db->sql_query($sql);
       $sql="UPDATE `text` SET `pars` = '1' WHERE `id` =".$_GET['url']." LIMIT 1 ;
";
  $result1 = $db->sql_query($sql);
}
	exit();

}

?>