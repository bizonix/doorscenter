<script language="JavaScript">
<!--
function change(name){ openWin = window.opener;
 openWin.changetpl(name);
 self.opener=self;self.close();}
// -->
</script>
<?
	echo '<table width="272" cellpadding="0" cellspacing="0">
    ';
$dh = opendir("../done");
while ($file = readdir($dh)){
	if((is_dir("../done/".$file))and($file!="..")and($file!=".")){		if($chet==0){echo '<tr>';}
		if(is_file("../done/".$file."/".$file.".gif")){
echo '
        <td width="136" style="cursor:pointer;" onclick="change(\''.$file.'\');"><img src="../done/'.$file.'/'.$file.'.gif" border="0"><br><br></td>
';
}else{echo '
        <td width="136" HEIGHT="105" style="cursor:pointer;" onclick="change(\''.$file.'\');"><br><center><b>'.$file.'</b></center></td>
';}
$chet++;
if($chet==2){echo '</tr>'; $chet=0;}
  }
  }
echo '
</table>';
?>