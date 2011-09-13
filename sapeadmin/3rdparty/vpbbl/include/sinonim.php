<?
if($_GET['sin']=="yes"){
	foreach($outcontent as $key=>$value){	$outcontent[$key]=sinonim($value);	echo "Синонимизация статьи номер ".($key+1)." выполнена.<br>\r\n";
	    echo '<script language="JavaScript">scrl(30)</script>';
		flush();
	}
}
function sinonim($stext){
 global $db;
$rere=str_replace(array(".",",","!","?","\r","\t","\n","(",")","'","\\",":","'","\"",";","$","0","1","2","3","4","5","6","7","8","9","\"","q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m","Q","W","E","R","T","Y","U","I","O","P","A","S","D","F","G","H","J","K","L","Z","X","C","V","B","N","M"), '', $stext );
$stext=str_replace(array("."), ' $^1^$', $stext );
$stext=str_replace(array(","), ' $^2^$', $stext );
$stext=str_replace(array("!"), ' $^3^$', $stext );
$stext=str_replace(array("?"), ' $^4^$', $stext );
$arr=explode(" ",$rere);
$re=0;
$rt=0;
for ($i=0; $i<count($arr); $i++) {
$re++;
	$arr2=array("й","ц","у","к","е","н","г","ш","щ","з","х","ъ","ф","ы","в","а","п","р","о","л","д","ж","э","я","ч","с","м","и","т","ь","б","ю");
	$arr1=array("Й","Ц","У","К","Е","Н","Г","Ш","Щ","З","Х","Ъ","Ф","Ы","В","А","П","Р","О","Л","Д","Ж","Э","Я","Ч","С","М","И","Т","Ь","Б","Ю");
	$arr[$i] = trim(str_replace($arr2,$arr1,$arr[$i]));
	if($re>30){$re=0; $rt++;}
	if(strlen($arr[$i])>1){
$words[$arr[$i]]=$i;
$words2[$rt][]=$arr[$i];
}
}


    for ($ei=0; $ei<count($words2); $ei++) {

$tr=implode("' or `word` LIKE '",$words2[$ei]);
$sql="SELECT *  FROM `sin` WHERE `word` LIKE '".$tr."'";
	$result1 = $db->sql_query($sql);
		$num=$db->sql_numrows($result1);
		for ($i=0; $i<$num; $i++) {
			$ttt=$db->sql_fetchrow($result1);
			$array[$ttt['word']][]=$ttt['sinonim'];
		}
}
foreach($array as $key=>$value){
	$tempp=str_replace($arr1,$arr2,trim($value[rand(0,count($value)-1)]));
	$aa[]=str_replace($arr1,$arr2,$key);
	$stext=str_ireplace(" ".str_replace($arr1,$arr2,$key)." "," ".$tempp." ",$stext);
}
if(($ch>0)and($secret==2)) {
$mmm1=array("е","у","р");
$mmm2=array("e","y","p");
$mmm3=array("<u>e</u>","<u>o</u>","<u>a</u>","<u>y</u>","<u>p</u>","<u>c</u>");

for ($i=0; $i<count($arr); $i++) {
	if(!array_search(str_replace($arr1,$arr2,$arr[$i]),$aa)){
	$rnd=rand(0,$ch);
	if($rnd==1){
	$old=str_replace($arr1,$arr2,$arr[$i]);
		$arr[$i]=str_replace($mmm1,$mmm2,str_replace($arr1,$arr2,$arr[$i]));
		$stext=str_replace($old,$arr[$i],$stext);
	}
	}
}
}
$stext=str_replace(' $^1^$', ".", $stext );
$stext=str_replace(' $^2^$', ",", $stext );
$stext=str_replace(' $^3^$', "!", $stext );
$stext=str_replace(' $^4^$', "?", $stext );
return $stext;
}
?>