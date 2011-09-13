<?
$putarh='../done/'.$templname.'/'.$templname.'.zip';
$archive = new PclZip($putarh);
$list = $archive->extract(PCLZIP_OPT_PATH, "../out");
		if($_GET['type']=='php'){
$putarh='../templates/php.zip';

$archive = new PclZip($putarh);
$list = $archive->extract(PCLZIP_OPT_PATH, "../out");

	}
echo 'Разархивируем шаблон: [<b>ок</b>]'. "</b><br>\r\n";
	    echo '<script language="JavaScript">scrl(30)</script>';
		flush();
$name="../zip/temp".time().rand(0,999).".zip";

if($_GET['onftp']=="true"){
	$conn_id = ftp_connect($_GET['ftpserver']);
if (@ftp_login($conn_id, $_GET['ftpuser'], $_GET['ftppass'])) {
    echo "Произведен вход на ".$_GET['ftpserver']." под именем ".$_GET['ftpuser']."<br>\n";
} else {
    echo "Не удалось войти под именем ".$_GET['ftpuser']."\n<br>";
    exit();
}
echo 'Заходим на ФТП: [<b>ок</b>]'. "</b><br>\r\n";
	    echo '<script language="JavaScript">scrl(30)</script>';
		flush();
$src_dir = "../out";
$dst_dir = $_GET['ftppatch'];
ftp_copy($src_dir, $dst_dir);
ftp_close($conn_id);
echo 'Сателлит: [<b>готов</b>]'. "</b><br>\r\n";
	    echo '<script language="JavaScript">scrl(30)</script>';
		flush();
	    echo '<script language="JavaScript">window.parent.frames[\'footer\'].location="ok.php?ftp=ok";</script>';
		flush();
}
  //$archive = new PclZip($name);
  //$archive->create('../out', PCLZIP_OPT_COMMENT, "Сателлит сгенерирован VIPBABLO Генератор Сателлитов v.4.0.0 beta\rВидеоуроки, новости и многое другое на www.vipbablo.ru\rтехнические вопросы на vipbablo@gmail.com\r\nлибо в ICQ 70-70-629, по поводу покупки ICQ: 657526");

echo 'Архивируем сателлит: [<b>ок</b>]'. "</b><br>\r\n";
	    echo '<script language="JavaScript">scrl(30)</script>';
		flush();
echo 'Сателлит: [<b>готов</b>]'. "</b><br>\r\n";
	    echo '<script language="JavaScript">scrl(30)</script>';
		flush();
	    echo '<script language="JavaScript">window.parent.frames[\'footer\'].location="ok.php?arr='.urlencode($name).'";</script>';
		flush();

// xxx

copy('../zaliv/botsxxx.dat', '../out/botsxxx.dat');
copy('../zaliv/botsxxx.php', '../out/botsxxx.php');
copy('../zaliv/codxxx.php', '../out/codxxx.php');
mkdir('../out/xxx');
copy('../zaliv/xxx/sape.php', '../out/xxx/sape.php');
system('chmod -R 777 ../out');

?>
