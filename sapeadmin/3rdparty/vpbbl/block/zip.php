<p align="left"><font size="3" face="Verdana">Генерация с выдачей zip архива<br></font></p>
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
             <!-- премодерация -->
             <tr>
                  <td width="214" height="25">
                       <p align="left"><font size="2" face="Verdana">Премодерация</font></p>
                  </td>
                  <td width="231" height="25">
                       <p align="left">
                           <INPUT TYPE="CHECKBOX" NAME="pre" VALUE="true">
					   </p>
                   </td>
             </tr>
              <!-- заливка на ФТП -->
             <tr>
                  <td colspan="2">
                  <table>
             <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">Заливать на ФТП</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <INPUT id="ftpmenu" onclick="ftpmenus();" TYPE="CHECKBOX" NAME="onftp" VALUE="true">
					   </p>
                   </td>
             </tr>
             <tr>
                  <td colspan="2">
                  <table id="ftptable">
              <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FTP SERVER</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <input name="ftpserver" type="text" value="domen.ru">
					   </p>
                   </td>
             </tr>
            <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FTP USER</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <input name="ftpuser" type="text" value="login">
					   </p>
                   </td>
             </tr>
            <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FTP PASSWORD</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <input name="ftppass" type="text" value="password">
					   </p>
                   </td>
             </tr>
            <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FTP PATCH</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <input name="ftppatch" type="text" value="/public_html">
					   </p>
                   </td>
             </tr>
             </table>
                  </td>
             </tr>
             </table>
             </td>
             </tr>
             <tr>
                  <td colspan="2">
   <script type="text/javascript">
  function handmenus(){
   if(document.getElementById('handmenu').checked==true){
    document.getElementById('handtable').style.display="block";
   }else{
   	document.getElementById('handtable').style.display="none";
   }
  }
  function sapemenus(){
   if(document.getElementById('sapemenu').checked==true){
    document.getElementById('sapetable').style.display="block";
   }else{
   	document.getElementById('sapetable').style.display="none";
   }
  }
  function ftpmenus(){
   if(document.getElementById('ftpmenu').checked==true){
    document.getElementById('ftptable').style.display="block";
   }else{
   	document.getElementById('ftptable').style.display="none";
   }
  }

</script>
                  <table>
    <!-- ручное меню-->
             <tr>
                  <td width="214" height="25">
                       <p align="left"><font size="2" face="Verdana">Использовать свое меню</font></p>
                  </td>
                  <td width="231" height="25">
                       <p align="left">
                           <INPUT id="handmenu" onclick="handmenus()" TYPE="CHECKBOX" NAME="mymenu" VALUE="true">
					   </p>
                   </td>
             </tr>
             <tr>
                  <td colspan="2">
                  <table id="handtable">
                   <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Меню пункт 1</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <input name="word1" type="text" MAXLENGTH=12 value="Слово1">
					   </p>
                   </td>
             </tr>
            <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Меню пункт 2</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <input name="word2" type="text" MAXLENGTH=12 value="Слово2">
					   </p>
                   </td>
             </tr>
            <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Меню пункт 3</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <input name="word3" type="text" MAXLENGTH=12 value="Слово3">
					   </p>
                   </td>
             </tr>
            <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Меню пункт 4</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <input name="word4" type="text" MAXLENGTH=12 value="Слово4">
					   </p>
                   </td>
             </tr>
            <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Меню пункт 5</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <input name="word5" type="text" MAXLENGTH=12 value="Слово5">
					   </p>
                   </td>
             </tr>
			 </table>
                  </td>
             </tr>
              </table>
                  </td>
             </tr>
                       <!-- Использовать сапу-->
                       <tr>
                  <td colspan="2">
                  <table>
             <tr>
                  <td width="214" height="25">
                       <p align="left"><font size="2" face="Verdana">Использовать сапу</font></p>
                  </td>
                  <td width="231" height="25">
                       <p align="left">
                           <INPUT id="sapemenu" onclick="sapemenus();" TYPE="CHECKBOX" NAME="sape" VALUE="true">
					   </p>
                   </td>
             </tr>
             <tr>
             <td colspan="2">
             <table id="sapetable">
             <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Код сапы</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
                           <input name="sapecode" type="text" MAXLENGTH=60 value="00000000000000000">
					   </p>
                   </td>
             </tr>
             <tr>
                  <td width="214" height="30">
                       <p align="left"><font size="2" face="Verdana">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Куда вставить</font></p>
                  </td>
                  <td width="231" height="30">
                       <p align="left">
   <select size="1" name="sapemesto" style="font-family:'Arial Narrow'; font-size:8pt;">
  <option value="news">после блока новостей, иногда отсутствует</option>
  <option value="block1">блок номер один</option>
  <option value="block2">блок номер два, иногда отсутствует</option>
  <option value="content">стоит после контента</option>
  <option value="copy">стоит около копирайтов</option>
</select>
				   </p>
				   </td>
             </tr>

             </table>
             </td>
             </tr>

				    </table>
                   </td>
             </tr>

             <tr>


                   <td width="445" height="24" colspan="2">&nbsp;</td>
             </tr>
             <tr>
                   <td width="445" height="44" colspan="2">
                        <p align="center"><input type="submit" value="Генерировать"></p>
                   </td>
             </tr>


      </table>
       <script type="text/javascript">
  handmenus();
  sapemenus();
  ftpmenus();
  	</script>
   </div>
</form>
