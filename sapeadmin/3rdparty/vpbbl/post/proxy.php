<?
$fp = fopen ("config.php", "w+");
$cc='<?
$config[\'min\']='.$config['min'].';
$config[\'maxlen\']='.$config['maxlen'].';
$config[\'proxy\']=\''.$_POST['proxy'].'\';
$config[\'proxyhost\']=\''.$_POST['host'].'\';
$config[\'proxyport\']=\''.$_POST['port'].'\';
' ;
$tarrt=$config['razdel'];
for ($i=0; $i<count($tarrt); $i++) {
$cc.='$config[\'razdel\'][]=\''.trim($tarrt[$i]).'\';
' ;
}
$cc.='
?>' ;
fwrite ($fp, $cc);
fclose ($fp);
header("Location: index.php?module=proxy&ok=1");
?>