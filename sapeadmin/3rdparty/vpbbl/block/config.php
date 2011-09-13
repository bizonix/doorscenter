<p align="left"><font size="3" face="Verdana">Настройки программы<br></font></p>
<form name="form1" method="post">
   <div align="left">
     <table width="445" cellpadding="0" cellspacing="0" height="324">
       <? if(@$_GET['ok']){ ?> <tr>
           <td width="214" height="30">
                <p align="left"><font size="2" color="green" face="Verdana"><b>Сохранено успешно</b></font></p>
           </td>
           <td width="231" height="30">
                <p align="left"></p>
           </td>
         </tr>
         <? } ?>
       <tr>
           <td width="214" height="30">
                <p align="left"><font size="2" face="Verdana">Минимальная длинна текста:</font></p>
           </td>
           <td width="231" height="30">
                <p align="left"><input type="text" name="min" size="29" style="padding-left:3pt; border-width:1pt; border-color:rgb(185,203,220); border-style:solid;" value="<? echo $config['min']; ?>" maxlength="60"></p>
           </td>
         </tr>


         <tr>
           <td width="214" height="30">
                <p align="left"><font size="2" face="Verdana">Максимальная длинна текста(обрезать):</font></p>
           </td>
           <td width="231" height="30">
                <p align="left"><input type="text" name="maxlen" size="29" style="padding-left:3pt; border-width:1pt; border-color:rgb(185,203,220); border-style:solid;" value="<? echo $config['maxlen']; ?>" maxlength="60"></p>
           </td>
         </tr>

         <tr>
           <td width="214" height="30">
                <p align="left"><font size="2" face="Verdana">Разделы (опционально при генерации):</font></p>
           </td>
           <td width="231" height="30">
                <p align="left"><textarea name="razdel" rows=5 cols=20 wrap="off"><? echo join("\r\n",$config['razdel']); ?></textarea></p>
           </td>
         </tr>


             <tr>
                   <td width="445" height="44" colspan="2">&nbsp;</td>
             </tr>
             <tr>
                   <td width="445" height="44" colspan="2">
                        <p align="center"><input type="submit" value="Сохранить"></p>
                   </td>
             </tr>
      </table>
   </div>
</form>
