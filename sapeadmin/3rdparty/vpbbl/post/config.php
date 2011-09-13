<?
if(!isset($config)){	include("config.php");}
$fp = fopen ("config.php", "w+");
$cc='<?
$config[\'min\']='.$_POST['min'].';
$config[\'maxlen\']='.$_POST['maxlen'].';
$config[\'proxy\']=\''.$config['proxy'].'\';
$config[\'proxyhost\']=\''.$config['proxyhost'].'\';
$config[\'proxyport\']=\''.$config['proxyport'].'\';
' ;
$tarrt=explode("\r\n",$_POST['razdel']);
for ($i=0; $i<count($tarrt); $i++) {
$cc.='$config[\'razdel\'][]="'.$tarrt[$i].'";
' ;
}
$cc.='
?>' ;
fwrite ($fp, $cc);
fclose ($fp);
header("Location: index.php?module=config&ok=1");
?>