<p align="left"><font size="3" face="Verdana">Генерация с заливкой на FTP<br></font></p>
<form name="form1" method="post">
   <div align="left">
     <table width="445" cellpadding="0" cellspacing="0" height="324">
        <tr>
           <td width="214" height="30">
                <p align="left"><font size="2" face="Verdana">Введите ключевую фразу:</font></p>
           </td>
           <td width="231" height="30">
                <p align="left"><input type="text" name="q" size="29" style="padding-left:3pt; border-width:1pt; border-color:rgb(185,203,220); border-style:solid;" value="Сладкая выпечка" maxlength="60"></p>
           </td>
         </tr>
         <tr>
            <td width="214" height="30">
                <p align="left"><font size="2" face="Verdana">Введите ключ для&nbsp;картинок:</font></p>
            </td>
            <td width="231" height="30">
                <p align="left"><input type="text" name="nn" size="29" style="padding-left:3pt; border-width:1pt; border-color:rgb(185,203,220); border-style:solid;" value="выпечка" maxlength="60"></p>
            </td>
          </tr>
          <tr>
             <td width="214" height="30">
                 <p align="left"><font size="2" face="Verdana">Введите количество страниц:</font></p>
             </td>
             <td width="231" height="30">
                 <p align="left"><input type="text" name="count" size="3" style="padding-left:3pt; border-width:1pt; border-color:rgb(185,203,220); border-style:solid;" value="20" maxlength="3"></p>
             </td>
           </tr>
           <tr>
              <td width="214" height="30">
                  <p align="left"><font size="2" face="Verdana">Использовать синонимайзер:</font></p>
              </td>
              <td width="231" height="30">
                  <p align="left"><font size="2" face="Verdana"><input type="radio" name="sin" value="yes">да &nbsp;&nbsp;&nbsp;&nbsp;<input type="radio" name="sin" value="no" checked>нет</font></p>
              </td>
           </tr>
           <tr>
               <td width="214" height="40">
                  <p align="left"><font size="2" face="Verdana">Использовать перевод <br> (ru-&gt;eng, eng-&gt;ru)</font></p>
               </td>
               <td width="231" height="40">
                  <p align="left"><font size="2" face="Verdana"><input type="radio" name="trans" value="yes">да &nbsp;&nbsp;&nbsp;&nbsp;<input type="radio" name="trans" value="no" checked>нет</font></p>
               </td>
           </tr>
           <tr>
                <td width="214" height="30">
                   <p align="left"><font size="2" face="Verdana">Установка картинок:</font></p>
                </td>
                <td width="231" height="30">
                   <p align="left">
		                <select name="picture" size="1">
		                   <option value="po12">по 1-2 (случайно) на каждую</option>
		                   <option value="po02">по 0-2 (случайно) на каждую</option>
		                   <option value="po03">po 0-3 (случайно) на каждую</option>
		                   <option selected value="all">-На каждую-</option>
		                   <option value="on2">на каждую 2-ю страницу</option>
		                   <option value="on3">на каждую 3-ю страницу</option>
		                   <option value="po2">по 2 на каждую</option>
		                   <option value="no">-без картинок-</option>
						</select>
				   </p>
                </td>
           </tr>
           <tr>
                 <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">Имена файлов:</font></p>
                 </td>
                 <td width="231" height="30">
                        <p align="left">
                              <select name="names" size="1">
                                 <option selected value="own">одно слово в транслите</option>
                                 <option value="title">заголовок в транслите</option>
                                 <option value="num">порядковый номер</option>
                                 <option value="rand">случайная цифра (0-9999999)</option>
                                 <option value="randrazdel">случайный раздел + цифра (0-99)</option>
							  </select>
						</p>
                   </td>
           </tr>
           <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">Тип сохранения:</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left"><input type="radio" name="type" value="php"><font size="2" face="Verdana">PHP &nbsp;&nbsp;&nbsp;&nbsp;<input type="radio" name="type" value="html" checked>HTML</font></p>
                  </td>
            </tr>
            <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">Шаблон для экспорта</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                            <? ddmenu(); ?> <span onclick="na_open_window('Template', 'include/changetpl.php', 200, 50, 350, 650, 0, 0, 0, 1, 0);" style="cursor:pointer;"><font color="#7DA8D3">выбрать</font></span>
					   </p>
                   </td>
             </tr>
            <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">FTP SERVER</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <input name="ftpserver" type="text" value="domen.ru">
					   </p>
                   </td>
             </tr>
            <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">FTP USER</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <input name="ftpuser" type="text" value="login">
					   </p>
                   </td>
             </tr>
            <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">FTP PASSWORD</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <input name="ftppass" type="text" value="password">
					   </p>
                   </td>
             </tr>
            <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">FTP PATCH</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <input name="ftppatch" type="text" value="/public_html">
					   </p>
                   </td>
             </tr>

             <tr>
                   <td width="445" height="44" colspan="2">&nbsp;</td>
             </tr>
             <tr>
                   <td width="445" height="44" colspan="2">
                        <p align="center"><input type="submit" value="Генерировать"></p>
                   </td>
             </tr>
      </table>
   </div>
</form>
