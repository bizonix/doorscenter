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
                <p align="left"><font size="2" face="Verdana">Использовать Proxy:</font></p>
           </td>
           <td width="231" height="30">
                <p align="left"><input type="CHECKBOX" name="proxy" <? if($config['proxy']){echo ' CHECKED=TRUE';} ?> size="29" style="padding-left:3pt; border-width:1pt; border-color:rgb(185,203,220); border-style:solid;" value="true" maxlength="60"></p>
           </td>
         </tr>


         <tr>
           <td width="214" height="30">
                <p align="left"><font size="2" face="Verdana">Proxy host:</font></p>
           </td>
           <td width="231" height="30">
                <p align="left"><input type="text" name="host" size="29" style="padding-left:3pt; border-width:1pt; border-color:rgb(185,203,220); border-style:solid;" value="<? echo $config['proxyhost']; ?>" maxlength="60"></p>
           </td>
         </tr>


         <tr>
           <td width="214" height="30">
                <p align="left"><font size="2" face="Verdana">Proxy port:</font></p>
           </td>
           <td width="231" height="30">
                <p align="left"><input type="text" name="port" size="29" style="padding-left:3pt; border-width:1pt; border-color:rgb(185,203,220); border-style:solid;" value="<? echo $config['proxyport']; ?>" maxlength="60"></p>
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
