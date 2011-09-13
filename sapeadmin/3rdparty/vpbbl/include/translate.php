<?
if($_GET['trans']=="yes"){
	foreach($outcontent as $key=>$value){
	$outcontent[$key]=translate($value,"ru","en");
	echo "Перевод статьи номер ".($key+1)." выполнен.<br>\r\n";
	    echo '<script language="JavaScript">scrl(30)</script>';
		flush();
	}
}
?>