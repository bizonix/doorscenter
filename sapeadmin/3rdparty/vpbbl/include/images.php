<?
$svoicontent=0;
if(preg_match("/\.txt/i",$_GET['q']))
{
	$svoicontent=1;
}

$version=4;
$licenz=@file_get_contents("../licence.dat");
@eval($licenz);

?>