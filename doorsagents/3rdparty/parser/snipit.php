<?
set_time_limit(0);
include("C:/Work/snippets/parser/httpdata.php");
//---------------------------------------------------------------//
$http = new httpdata;

$pause = 5; // новый параметр. Время между запросами к гуглу в секундах
$num = 1; //Глубина парсинга
$file = "C:/Work/snippets/parser/text.txt"; //Файл куда будет скидыватся текст
$lang = file_get_contents("C:/Work/snippets/parser/language.txt");
$fkeys = "C:/Work/snippets/parser/keywords.txt";
$proxies = "C:/Work/snippets/parser/proxy.txt";
$proxiesArray = file($proxies);
$googlesuka = "Приносим свои извинения..."; //Гугл сука, банит нас

//-------------------------Файлы---------------------------------------//
$fp = fopen($file, "w+");
$keys = file($fkeys);

//-------------------------Главный цикл---------------------------------------//
$ch = $http->CurlInit(); //Инициализируем cUrl
for($n=0;$n<count($keys);$n++)
{
  $key = trim($keys[$n]);
  echo "\r\n" . date('d.m.Y H:i:s') . " - parsing: " . $key;
  for($i=0;$i<$num;$i++)
  {
    $url = "http://www.google.com/search?as_q=".urlencode($key)."&tbs=qdr:z&num=100&hl=$lang&output=ie&filter=0";
    $res = $http->GetData($ch, $url);

    if(!$http->CheckData($googlesuka, $res)){
      preg_match_all("#<div class=\"s\">(.+)<br>#sU", $res, $text);
      
      $nn = 0;
      foreach($text[1] as $t) {
        $t = strip_tags($t);
        $t = str_replace("...", "", $t);
        $t = str_replace("&nbsp;", " ", $t);
        $t = str_replace("&gt;", "", $t);
        $t = str_replace("&quot;", "", $t);
        $t = str_replace(" &middot;", ".", $t);
        $t = str_replace("&#39;", "'", $t);
        $t = iconv('utf-8', 'cp1251', $t);
        fwrite($fp, $t."\r\n");
        $nn++;
      }
      echo ", " . $nn;
    } else {
      echo "Гугл сука забанил";
      die();
    }

  }  
}
$http->CurlClose($ch);
unset($ch);
fclose($fp);
unset($http);
?>