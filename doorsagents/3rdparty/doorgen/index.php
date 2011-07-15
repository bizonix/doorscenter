<?
$mode = $_POST["mode"];

if ($_POST["action"] == "save"){

echo "<style>p {text-align:center}</style>";
	switch ($mode) {
	   case "settings":
			echo "<p><a href='index.php'>Назад</a></p>";
			$settings_text = stripslashes($_POST["settings_text"]);
			$file_out = fopen("settings.xml", "w");
			fwrite($file_out, $settings_text);
			fclose($file_out);
			echo "<p>Настройки сохранены</p>";
			exit;
			
		case "jobs":
			echo "<p><a href='index.php'>Назад</a></p>";
			$jobs_file = $_POST["jobs_file"];
			$jobs_text = stripslashes($_POST["jobs_text"]);
			$file_out = fopen($jobs_file, "w");
			fwrite($file_out, $jobs_text);
			fclose($file_out);
			echo "<p>Задание сохранено</p>";
			exit;

		case "templates":
			echo "<p><a href='index.php'>Назад</a></p>";
			$templ_folder = $_POST["templ_folder"];
			$templ_index_text = stripslashes($_POST["templ_index_text"]);
			$templ_page_text = stripslashes($_POST["templ_page_text"]);
			$templ_map_text = stripslashes($_POST["templ_map_text"]);
			if(!is_dir($templ_folder))
				mkdir($templ_folder);
			$file_out = fopen($templ_folder."/index.txt", "w");
			fwrite($file_out, $templ_index_text);
			fclose($file_out);
			$file_out = fopen($templ_folder."/page.txt", "w");
			fwrite($file_out, $templ_page_text);
			fclose($file_out);
			$file_out = fopen($templ_folder."/map.txt", "w");
			fwrite($file_out, $templ_map_text);
			fclose($file_out);
			echo "<p>Шаблон сохранен</p>";
			exit;

		case "keys":
			echo "<p><a href='index.php'>Назад</a></p>";
			$keys_file = $_POST["keys_file"];
			$keys_text = stripslashes($_POST["keys_text"]);
			$file_out = fopen($keys_file, "w");
			fwrite($file_out, $keys_text);
			fclose($file_out);
			echo "<p>Ключи сохранены</p>";
			exit;

		case "macros":
			echo "<p><a href='index.php'>Назад</a></p>";
			$macros_file = $_POST["macros_file"];
			$macros_text = stripslashes($_POST["macros_text"]);
			$file_out = fopen($macros_file, "w");
			fwrite($file_out, $macros_text);
			fclose($file_out);
			echo "<p>Макросы сохранены</p>";
			exit;

		case "text":
			echo "<p><a href='index.php'>Назад</a></p>";
			$text_file = $_POST["text_file"];
			$text_text = stripslashes($_POST["text_text"]);
			$file_out = fopen($text_file, "w");
			fwrite($file_out, $text_text);
			fclose($file_out);
			echo "<p>Текстовки сохранены</p>";
			exit;

		default:
			echo "<p>Ошибка, вернитесь <a href='index.php'>Назад</a></p>";
			exit;
	}
}

echo "<style>p {text-align:center} h2 {text-align:center} h3 {text-align:center}</style>";
echo "<h2>Настройки генератора</h2>";
echo "<p><a href='readme.html' target='_blank'>Помощь</a></p>";

switch ($mode) {
   case "settings":
		echo "<h3>РЕДАКТИРУЕМ НАСТРОЙКИ</h3>";
		$settings_text = file_get_contents("settings.xml");
		echo "<form action='index.php' method='post'>
		<p><a href='index.php'>Назад</a></p>
		<p>Настройки:</p>
		<p><textarea rows='35' cols='150' name='settings_text'>$settings_text</textarea></p>
		<input name='mode' type='hidden' value='$mode'>
		<input name='action' type='hidden' value='save'>
		<p><input type='submit' value='Сохранить'></p>
		<p><a href='index.php'>Назад</a></p>
		</form>";
		exit;

	case "jobs":
		echo "<h3>РЕДАКТИРУЕМ ЗАДАНИЕ</h3>";
		$jobs_file = $_POST["jobs_file"];
		$jobs_text = @file_get_contents($jobs_file);
		echo "<form action='index.php' method='post'>
		<p><a href='index.php'>Назад</a></p>
		<p>Файл задания: <b>$jobs_file</b></p>
		<p>Задания из файла:</p>
		<p><textarea rows='20' cols='100' name='jobs_text'>$jobs_text</textarea></p>
		<input name='jobs_file' type='hidden' size='40' value='$jobs_file'>
		<input name='mode' type='hidden' value='$mode'>
		<input name='action' type='hidden' value='save'>
		<p><input type='submit' value='Сохранить'></p>
		<p><a href='index.php'>Назад</a></p>
		</form>";
		exit;

	case "templates":
		echo "<h3>РЕДАКТИРУЕМ ШАБЛОН</h3>";
		$templ_folder = $_POST["templ_folder"];
		$templ_index_text = @file_get_contents($templ_folder."/index.txt");
		$templ_page_text = @file_get_contents($templ_folder."/page.txt");
		$templ_map_text = @file_get_contents($templ_folder."/map.txt");
		echo "<form action='index.php' method='post'>
		<p><a href='index.php'>Назад</a></p>
		<p>Папка с шаблонами: <b>$templ_folder</b></p>
		<p>index.txt:</p>
		<p><textarea rows='20' cols='150' name='templ_index_text'>$templ_index_text</textarea></p>
		<p>page.txt:</p>
		<p><textarea rows='20' cols='150' name='templ_page_text'>$templ_page_text</textarea></p>
		<p>map.txt:</p>
		<p><textarea rows='20' cols='150' name='templ_map_text'>$templ_map_text</textarea></p>
		<input name='templ_folder' type='hidden' size='40' value='$templ_folder'>
		<input name='mode' type='hidden' value='$mode'>
		<input name='action' type='hidden' value='save'>
		<p><input type='submit' value='Сохранить'></p>
		<p><a href='index.php'>Назад</a></p>
		</form>";
		exit;

	case "keys":
		echo "<h3>РЕДАКТИРУЕМ КЛЮЧИ</h3>";
		$keys_file = $_POST["keys_file"];
		$keys_text = @file_get_contents($keys_file);
		echo "<form action='index.php' method='post'>
		<p><a href='index.php'>Назад</a></p>
		<p>Файл ключей: <b>$keys_file</b></p>
		<p>Ключи из файла:</p>
		<p><textarea rows='30' cols='100' name='keys_text'>$keys_text</textarea></p>
		<input name='keys_file' type='hidden' size='40' value='$keys_file'>
		<input name='mode' type='hidden' value='$mode'>
		<input name='action' type='hidden' value='save'>
		<p><input type='submit' value='Сохранить'></p>
		<p><a href='index.php'>Назад</a></p>
		</form>";
		exit;

	case "macros":
		echo "<h3>РЕДАКТИРУЕМ МАКРОСЫ</h3>";
		$macros_file = $_POST["macros_file"];
		$macros_text = @file_get_contents($macros_file);
		echo "<form action='index.php' method='post'>
		<p><a href='index.php'>Назад</a></p>
		<p>Файл макросов: <b>$macros_file</b></p>
		<p>Макросы из файла:</p>
		<p><textarea rows='30' cols='150' name='macros_text'>$macros_text</textarea></p>
		<input name='macros_file' type='hidden' size='40' value='$macros_file'>
		<input name='mode' type='hidden' value='$mode'>
		<input name='action' type='hidden' value='save'>
		<p><input type='submit' value='Сохранить'></p>
		<p><a href='index.php'>Назад</a></p>
		</form>";
		exit;

   case "text":
		echo "<h3>РЕДАКТИРУЕМ ТЕКСТОВКИ</h3>";
		$text_file = $_POST["text_file"];
		$text_text = @file_get_contents($text_file);
		echo "<form action='index.php' method='post'>
		<p><a href='index.php'>Назад</a></p>
		<p>Файл текстовки: <b>$text_file</b></p>
		<p>Текст из файла:</p>
		<p><textarea rows='30' cols='150' name='text_text'>$text_text</textarea></p>
		<input name='text_file' type='hidden' size='40' value='$text_file'>
		<input name='mode' type='hidden' value='$mode'>
		<input name='action' type='hidden' value='save'>
		<p><a href='index.php'>Назад</a> <input type='submit' value='Сохранить'></p>
		</form>";
		exit;

	case "delete":
		$delete_file = $_POST["delete_file"];
		echo "<p>Удаление файла: <b>$delete_file</b></p>";
		if (@unlink($delete_file))
			echo "<p>Файл удален</p>
		<p><a href='index.php'>Назад</a></p>";
		else
			echo "<p>Файл НЕ удален</p>
		<p><a href='index.php'>Назад</a></p>";
		exit;

	default:
		$settings_text = file_get_contents("settings.xml");
		$settings = simplexml_load_string($settings_text);
		$editor_def_jobs_file = (string)$settings->editor->editor_def_jobs_file;
		$editor_def_templ_folder = (string)$settings->editor->editor_def_templ_folder;
		$editor_def_keys_file = (string)$settings->editor->editor_def_keys_file;
		$editor_def_macros_file = (string)$settings->editor->editor_def_macros_file;
		$editor_def_text_file = (string)$settings->editor->editor_def_text_file;
		$editor_def_delete_file = (string)$settings->editor->editor_def_delete_file;
		echo "<style>table {border:0px} td {padding:10px; margin:0px; vertical-align:middle; height:50px} #pn {background-color:#DFDFDF} #pn2 {background-color:#EFEFEF}</style>";
		echo "<table align='center' cellpadding='0' cellspacing='0'>";
		echo "<form action='index.php' method='post'><tbody id='pn'><tr><td>Редактировать настройки <b>settings.xml</b></td><td><input name='mode' type='hidden' value='settings'></td><td><input type='submit' value='Править'></tr></tbody></form>";
		echo "<form action='index.php' method='post'><tbody id='pn2'><tr><td>Редактировать задание</td><td><input name='jobs_file' type='text' size='40' value='$editor_def_jobs_file'><input name='mode' type='hidden' value='jobs'></td><td><input type='submit' value='Править'></tr></tbody></form>";
		echo "<form action='index.php' method='post'><tbody id='pn'><tr><td>Редактировать шаблон</td><td><input name='templ_folder' type='text' size='40' value='$editor_def_templ_folder'><input name='mode' type='hidden' value='templates'></td><td><input type='submit' value='Править'></tr></form>";
		echo "<form action='index.php' method='post'><tbody id='pn2'><tr><td>Редактировать ключи</td><td><input name='keys_file' type='text' size='40' value='$editor_def_keys_file'><input name='mode' type='hidden' value='keys'></td><td><input type='submit' value='Править'></tr></form>";
		echo "<form action='index.php' method='post'><tbody id='pn'><tr><td>Редактировать макросы</td><td><input name='macros_file' type='text' size='40' value='$editor_def_macros_file'><input name='mode' type='hidden' value='macros'></td><td><input type='submit' value='Править'></tr></tbody></form>";
		echo "<form action='index.php' method='post'><tbody id='pn2'><tr><td>Редактировать текстовки</td><td><input name='text_file' type='text' size='40' value='$editor_def_text_file'><input name='mode' type='hidden' value='text'></td><td><input type='submit' value='Править'></tr></tbody></form>";
		echo "<form action='index.php' method='post'><tbody id='pn'><tr><td>Удалить файл</td><td><input name='delete_file' type='text' size='40' value='$editor_def_delete_file'><input name='mode' type='hidden' value='delete'></td><td><input type='submit' value='Удалить'></tr></form>";
		echo "</table>";
		echo "<p align='center' size='5'><a href='engine.php' target='_blank'>Генерация</a></p>";
		exit;
}
?>
</body>
</html>