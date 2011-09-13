<?
include("../confbd.php");
include("bd.php");

function update($id,$title,$text){
global $db;$sql="UPDATE `text` SET `title` = '".mysql_escape_string($title)."',  `text` = '".mysql_escape_string($text)."' WHERE `id` =".mysql_escape_string($id)." LIMIT 1 ;";
  $result1 = $db->sql_query($sql);}
function del($id){
global $db;
	   $sql="DELETE FROM `text` WHERE `id` = ".mysql_escape_string($id)." LIMIT 1;";
  $result1 = $db->sql_query($sql);
}

if(count($_POST)>2){
foreach($_POST as $key=>$line){	if(substr($key,0,3)=="use"){		list(,$id)=explode("use",$key);
		$arrid[$id]='1';	}}
$sql="SELECT *
FROM `text`  WHERE `pars` = 1";
  $result1 = $db->sql_query($sql);
  $num=$db->sql_numrows($result1);
  for ($i=0; $i<$num; $i++) {
$arr=$db->sql_fetchrow($result1);
if(!isset($arrid[$arr['id']])) {	del($arr['id']);}else{	if(isset($_POST['edit'.$arr['id']]))
	{		update($arr['id'],$_POST['title'.$arr['id']],$_POST['text'.$arr['id']]);	}}
}
 echo '<br><br><br><h2>Изминения сохранены.</h2><br><br><br>';
}

	       $sql="SELECT *
FROM `text`  WHERE `pars` = 1";
  $result1 = $db->sql_query($sql);
  $num=$db->sql_numrows($result1);
  echo '
  <script type=\'text/javascript\'><!--
    function view(id){if(document.getElementById(\'div\'+id).style.display=="none"){	document.getElementById(\'div\'+id).style.display="inline";}else{	document.getElementById(\'div\'+id).style.display="none";}
    	}
    	function edityes(id){    	document.getElementById(\'iedit\'+id).checked="true";
    	}

   -->
  </script>
  <form method="post">
  <table width="953" cellpadding="0" cellspacing="0">
    <tr>
        <td width="21" bgcolor="#DCE9F7">
            <p align="center"><font size="1" face="Arial">№</font></p>
        </td>
        <td width="38" bgcolor="#DCE9F7" style="border-right-width:1pt; border-left-width:1pt; border-right-color:black; border-left-color:black; border-right-style:solid; border-left-style:solid;"><font size="1" face="Arial">Использовать</font></td>
        <td width="42" bgcolor="#DCE9F7" style="border-right-width:1pt; border-right-color:black; border-right-style:solid;"><font size="1" face="Arial">Редактировать</font></td>
        <td width="824" bgcolor="#DCE9F7">
            <p align="center"><font size="3" face="Arial"><b>Заголовок</b></font></p>
        </td>
    </tr>';
  for ($i=0; $i<$num; $i++) {
$arr=$db->sql_fetchrow($result1);
$outtitle[]=$arr['title'];
$outurl[]=$arr['url'];
$outcontent[]=$arr['text'];
/*echo "\r\n<br>".'<hr><h2>'.$arr['id'].'</h2>
<a href="pre.php?cmd=del&id='.$arr['id'].'">Удалить</a> <br>
<form method="post">
<input name="id" type="hidden" value="'.$arr['id'].'">
<input name="cmd" type="hidden" value="edit">
<input name="title" SIZE=75 type="text" value="'.$arr['title'].'"><br>
<input name="url" SIZE=75 type="text" value="'.$arr['url'].'"><br>
<textarea name="text" rows=7 cols=60 wrap="off">'.$arr['text'].'</textarea><br>
<input type="submit" value="Редактировать">
</form>

';    */
echo '

    <tr>
        <td width="21" style="border-bottom-width:1pt; border-bottom-color:rgb(153,153,153); border-bottom-style:solid;">'.($i+1).'</td>
        <td width="38" style="border-right-width:1pt; border-bottom-width:1pt; border-left-width:1pt; border-right-color:black; border-bottom-color:rgb(153,153,153); border-left-color:black; border-right-style:solid; border-bottom-style:solid; border-left-style:solid;">
            <p align="center"><input type="checkbox" checked name="use'.$arr['id'].'" value="1"></p>
        </td>
        <td width="42" style="border-right-width:1pt; border-bottom-width:1pt; border-right-color:black; border-bottom-color:rgb(153,153,153); border-right-style:solid; border-bottom-style:solid;">
            <p align="center"><input type="checkbox" id="iedit'.$arr['id'].'" name="edit'.$arr['id'].'" value="1"></p>
        </td>
        <td width="824" style="border-bottom-width:1pt; border-bottom-color:rgb(153,153,153); border-bottom-style:solid;"><font size="2" face="Arial">&nbsp;<a href="javascript:view(\''.$arr['id'].'\');">[edit]</a> </font><input onkeypress="edityes(\''.$arr['id'].'\')" type="text" name="title'.$arr['id'].'" size="84" value="'.strip_tags($arr['title']).'" style="border-width:1pt; border-color:white; border-style:solid;"><font size="2" face="Arial"> Текст: '.strlen($arr['text']).' символов</font>
        <div id="div'.$arr['id'].'" style="display:none;">
        <textarea onkeypress="edityes(\''.$arr['id'].'\')" WRAP="virtual" name="text'.$arr['id'].'" rows=8 cols=90 wrap="off">'.htmlspecialchars($arr['text']).'</textarea>
        </div>
        </td>
    </tr>

';
  }
  echo '</table>
  <br><br>
<input type="submit" value="Сохранить"></form>
  ';
?>