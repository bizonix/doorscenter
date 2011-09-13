<?php
session_start();
if(!empty($_POST)) header("Location:$PHP_SELF");
$b_data = "botsxxx.dat";
$b_msgp = 500;
$data = file($b_data);
$maxmsg = count($data);
rsort ($data);
if($logon) {
if ($password == $b_psswd) {
session_register("psswd");
$psswd = $password;
}
}
if ($delete) {
$fp = fopen($b_data,"w");
ftruncate ($fp,0); 
fclose($fp);
}
?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1251">
<style type="text/css">
body, td {margin-top:0px; margin-bottom:0px; font-weight:normal; font-size:11px; color:#000000; font-family:tahoma; text-decoration:none}
input {font-weight:normal; font-size:11px; color:black; font-family:tahoma; text-decoration:none; border-right:#808080 1px solid; border-top:#808080 1px solid; border-left:#808080 1px solid; border-bottom:#808080 1px solid; background-color:#dFdFdF}
a {color:#000000}
a:hover {text-decoration:underline; color:#ce0000}
</style>
</head>
<body bgcolor="#ffffff"><br>
<center>
<?php
print("<b>$maxmsg</b> <br><br>");
if ($maxmsg) {
?>
<table style="border-collapse:collapse" width="60%" border="1" cellspacing="0" cellpadding="5" align="center" bordercolor="#808080" bordercolordark="#808080" bordercolorlight="#808080">
<?php
$frstmsg = $p * $b_msgp;
$lastmsg = $p * $b_msgp + $b_msgp;
if ($lastmsg > $maxmsg) {
$lastmsg=$maxmsg;
}
for ($u=$frstmsg; $u<$lastmsg; $u++) {
$entry = explode("|",$data[$u]);
print ("<tr><td>$entry[1]</td><td>$entry[2]</td><td>$entry[3]</td><td width=\"100%\"><a target=\"_blank\" href=\"http://$entry[5]\">$entry[5]</a></td></tr>"); 
}
?>
</table>
<br>
<?php
$t_links=($maxmsg-0.1)/$b_msgp;
if ($t_links>1) {
print("<table width=\"60%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" align=\"center\"><tr><td align=\"center\">");
for($j=0;$j<=$t_links;$j++) {
$n=$j+1;
if ($j!=$p)print("[<a href=\"$PHP_SELF?p=$j\">$n</a>] ");
else print("[$n] ");
}
print("</td></tr></table><br>");
}
}
?>
<table style="border-collapse:collapse" width="60%" border="1" cellspacing="0" cellpadding="5" align="center" bordercolor="#808080" bordercolordark="#808080" bordercolorlight="#808080">
</center>
</body>
</html>