<?
set_time_limit(0);
include("C:/Work/snippets/parser/httpdata.php");
//---------------------------------------------------------------//
$http = new httpdata;

$num = 2; //Глубина парсинга
$file = "C:/Work/snippets/parser/text.txt"; //Файл куда будет скидыватся текст
//$lang = "ru"; //Язык парсинга i.e(ru, en, ua. Нужно для парсинга русского текста, чтоб гугл отдавал его в читаемом виде.)
$lang = file_get_contents("C:/Work/snippets/parser/language.txt");
$fkeys = "C:/Work/snippets/parser/keywords.txt";

//-------Прокси--------//
//$http->setProxy("139.19.142.3:3128");

$googlesuka = "Приносим свои извинения..."; //Гугл сука, банит нас


//-------------------------Файлы---------------------------------------//
$fp = fopen($file, "w+");
$keys = file($fkeys);


$ch = $http->CurlInit(); //Инициализируем cUrl

//-------------------------Главный цикл---------------------------------------//
for($n=0;$n<count($keys);$n++)
{
	$key = trim($keys[$n]);
	$start = 0;
	echo "Parsing: ".$key."\r\n";
	for($i=0;$i<$num;$i++)
	{
        $url = "http://www.google.com/search?hl=$lang&q=".urlencode($key)."&start=".$start;  // исправлено
        $start += 10; // исправлено

        $res = $http->GetData($ch, $url);
        sleep($pause); // подождать немного

		if(!$http->CheckData($googlesuka, $res)){
			preg_match_all("#<div class=\"s\">(.+)<br>#sU", $res, $text);
			
			foreach($text[1] as $t)
			{
				$t = strip_tags($t);
				$t = str_replace("...", "", $t);
				$t = str_replace("&nbsp;", " ", $t);
				$t = str_replace("&gt;", "", $t);
				$t = str_replace("&quot;", "", $t);
				$t = str_replace(" &middot;", ".", $t);
				$t = str_replace("&#39;", "'", $t);
				$t = iconv('utf-8', 'cp1251', $t);
				fwrite($fp, $t."\r\n");
			}
		}else{
			echo "Гугл сука забанил";
			die();
		}

	}	
}
fclose($fp);
$http->CurlClose($ch);
unset($ch);
unset($http);


?>
