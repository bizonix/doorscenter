<html>

<head>
<title>VIP Bablo - генератор сателлитов</title>
<meta http-equiv="content-type" content="text/html; charset=windows-1251"></head>

<body bgcolor="#EFEFDE" text="black" link="blue" vlink="purple" alink="red">
<table width="731" height="79" cellpadding="0" cellspacing="0" align="center">
    <tr>
        <td width="731" height="44">
            <table width="691" height="40" cellpadding="0" cellspacing="0">
                <tr>
                    <td width="576" height="34"><b><font size="4" face="Verdana" color="#A8A2A2">Генератор Сателлитов</font></b></td>
                    <td width="53" height="34">
                        <p align="center"><b><font size="5">VIP</font></b></p>
                    </td>
                    <td width="62" height="34">
                        <p align="left"><b><font size="4" color="red">Bablo</font></b></p>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td width="731">
        <table width="698" cellpadding="0" cellspacing="0" style="padding:4pt; border-width:1pt; border-color:rgb(189,193,190); border-style:solid;" height="149">
                <tr>
                    <td width="696" height="147">
                        <div align="right">
                            <table width="692" cellpadding="0" cellspacing="0" height="100%">
                                <tr>
                                    <td width="468">
                                        <table width="453" cellpadding="0" cellspacing="0" bgcolor="white" style="padding:4pt; border-width:1pt; border-color:rgb(185,203,220); border-style:solid;" height="100%">
                                            <tr>
                                                <td width="451" height="468" valign="top">
<center><iframe name="top" src="include/parse.php?view=zip&q=<? echo urlencode($_POST['q']); ?>&nn=<? echo urlencode($_POST['nn']); ?>&count=<? echo urlencode($_POST['count']); ?>&sin=<? echo urlencode($_POST['sin']); ?>&trans=<? echo urlencode($_POST['trans']); ?>&picture=<? echo urlencode($_POST['picture']); ?>&names=<? echo urlencode($_POST['names']); ?>&type=<? echo urlencode($_POST['type']); ?>&tpl=<? echo urlencode($_POST['tpl']); ?>&pre=<? echo urlencode(@$_POST['pre']); ?>&onftp=<? echo urlencode(@$_POST['onftp']); ?>&mymenu=<? echo urlencode(@$_POST['mymenu']); ?><?
if(@$_POST['sape']=="true"){	?>
&sape=true&sapecode=<? echo urlencode($_POST['sapecode']); ?>&sapemesto=<? echo urlencode($_POST['sapemesto']); ?>
<?
}
?><?
if(@$_POST['onftp']=="true"){
	?>
&ftpuser=<? echo urlencode($_POST['ftpuser']); ?>&ftppass=<? echo urlencode($_POST['ftppass']); ?>&ftpserver=<? echo urlencode($_POST['ftpserver']); ?>&ftppatch=<? echo urlencode($_POST['ftppatch']); ?>
<?
}
?><?

if(@$_POST['mymenu']=="true"){
	?>
&word1=<? echo urlencode($_POST['word1']); ?>&word2=<? echo urlencode($_POST['word2']); ?>&word3=<? echo urlencode($_POST['word3']); ?>&word4=<? echo urlencode($_POST['word4']); ?>&word5=<? echo urlencode($_POST['word5']); ?>
<?
}
?>" frameborder="0" width="372" height="236"></iframe></center><br>
<center><iframe name="footer" src="include/progressbar.php" frameborder="0" width="372" scrolling="no" height="26"></iframe></center>
               </td>
                                            </tr>
                                        </table>
                                    </td>
                                    <td width="224" valign="top">
                                        <? include('menu.php'); ?>
                                    </td>
                                </tr>
                            </table>
                        </div>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
<p>&nbsp;</p>
</body>

</html>