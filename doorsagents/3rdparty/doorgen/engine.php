<?
{	//настройки
	set_time_limit(0);
//	error_reporting(E_ALL^E_NOTICE);
//	ini_set("display_errors", 1); 
	ini_set("max_execution_time", 0);
	ini_set("memory_limit", -1);
	ob_implicit_flush(1); //сразу выводить на экран из буфера
	$time_start = time(); //засекаем время начала работы
	require ("lib/func.lib.php");
	require ("lib/permissions.php");
}

{	//читаем настройки из settings.xml
	$settings = simplexml_load_file("settings.xml") or die("<b>Ошибка</b>: Не возможно прочитать конфиг файл settings.xml");

	$job_file = (string)$settings->primary->job_file; //название файла текущего задания
	$text_ancor_sitemap_links = (string)$settings->primary->text_ancor_sitemap_links; //префикс текста анкора линков карт сайтов
	$text_ancor_index_link = (string)$settings->primary->text_ancor_index_link; //текст анкора на главную страницу дора
	$count_ancor_in_map = (int)$settings->primary->count_ancor_in_map; //кол-во анкоров на одной карте. для разбивки карты
	$num_perc_spam = (float)$settings->primary->num_perc_spam; //соотношение кол-ва BB ссылок для спама, к общему кол-ву страниц одного дора (0.6 = 60%)

	$compression_template = (bool)str_to_bool($settings->secondary->compression_template); //сжимать получившиеся страницы дора
	$extension = (string)$settings->secondary->extension; //расширение у всех файлов сгенереного дора
	$keys_dir = (string)$settings->secondary->keys_dir; //папка с ключами
	$templ_dir = (string)$settings->secondary->templ_dir; //папка с шабами
	$out_dir = (string)$settings->secondary->out_dir; //папка с готовыми дорами
	$jobs_dir = (string)$settings->secondary->jobs_dir; //папка, где расположены задания
	$text_dir = (string)$settings->secondary->text_dir; //откуда дорген будет брать тексты из файлов, для макросов
	$insert_sitemaps_links_in_all_ancor_log = (bool)str_to_bool($settings->secondary->insert_sitemaps_links_in_all_ancor_log); //вставлять ссылки на карты сайтов
	$insert_sitemaps_links_in_ancor_log = (bool)str_to_bool($settings->secondary->insert_sitemaps_links_in_ancor_log); //вставлять ссылки на карты сайтов
	$insert_sitemaps_links_in_bbcode_log = (bool)str_to_bool($settings->secondary->insert_sitemaps_links_in_bbcode_log); //вставлять ссылки на карты сайтов
	$insert_sitemaps_links_in_bbcode_log_spam = (bool)str_to_bool($settings->secondary->insert_sitemaps_links_in_bbcode_log_spam); //вставлять ссылки на карты сайтов
	$generate_sitemap_xml = (bool)str_to_bool($settings->secondary->generate_sitemap_xml); //генерировать sitemap.xml
	$generate_robots_txt = (bool)str_to_bool($settings->secondary->generate_robots_txt); //генерировать robots.txt
	$generate_filezilla_project = (bool)str_to_bool($settings->secondary->generate_filezilla_project); //генерировать проекты для импорта в filezilla
	$enable_packing = (bool)str_to_bool($settings->secondary->enable_packing); //запаковка в zip
	$upload_ftp = (bool)str_to_bool($settings->secondary->upload_ftp); //выгружать на ftp

	$default_ftp_url = (string)$settings->secondary->default_ftp_url; //хост для подключения по ftp (по умолчанию)
	$default_ftp_params = parse_url($default_ftp_url); //парсим строку для получения остальных параметров подключения

	$default_ftp_host = (string)$default_ftp_params["host"]; //порт для подключения по ftp (по умолчанию)
	$default_ftp_port = (string)$default_ftp_params["port"]; //порт для подключения по ftp (по умолчанию)
	if ($default_ftp_port=="")
		$default_ftp_port = 21;
	$default_ftp_login = (string)$default_ftp_params["user"]; //юзернейм для подключения по ftp (по умолчанию)
	$default_ftp_password = (string)$default_ftp_params["pass"]; //пароль для подключения по ftp (по умолчанию)
	$default_ftp_path = (string)$default_ftp_params["path"]; //путь до папки, куда выгрузится zip без / в конце (по умолчанию)
	$extract_zip_archive = (bool)str_to_bool($settings->secondary->extract_zip_archive); //путь до папки, куда выгрузится zip без / в конце (по умолчанию)
	$text_ancor_sitemap_links = iconv("utf-8", "windows-1251", $text_ancor_sitemap_links); //преобразуем строку с префиксом карты из utf-8 формата в win1251
	$text_ancor_index_link = iconv("utf-8", "windows-1251", $text_ancor_index_link); //преобразуем строку с префиксом карты из utf-8 формата в win1251
}

{	//читаем задания, формируем логи, формируем ссылки для перелинковки, формируем список кеев для последующей генерации
	$data_cache_file = array(); //массив - кеш текстовки из файлов для функции cache_file
	$a_dor_urand_number = array(); //массив для макроса DOR_RAND (хранятся использованные случайные значения для каждогодо дора)

	$job_list = file($jobs_dir."/".$job_file) or die("<b>Ошибка</b>: Не найден (или пустой) файл заданий. Проверьте ".$jobs_dir."/".$job_file); //читаем задания
//	$job_list = massTrim($job_list); //чистим от \n
	$job_list = del_comment_job_list($job_list); //удаляем комменты с перестановкой в получившиеся пустые строки
	$count_job = count($job_list);
	preg_match("/(.*?)\.txt/i", $job_file, $job_name); //получаем имя файла задания без расширения и ...
	$job_name = $job_name[1]."_".time(); //... обзываем с добавлением timestamp
	echo "Всего заданий: <b>".$count_job."</b><br>";
	echo "Идет выборка и подготовка ключей для доров. Это может занять несколько минут<br><script>scroll(0,999999);document.title='Выборка и подготовка ключей'</script>";
	$t4 = time();
	for($i=0;$i<$count_job;$i++) { //вначале проходим по заданиям и генерируем *_log.txt для правильной перелинковки всей сетки. для макроса {RELINKS}. преобразуем все кеи в названия файлов страниц
		$job_list[$i] = replace_macros_page($job_list[$i], $access_macros_jobs); //обрабатываем макросы в строках заданий
		$tmp_job_list[$i] = explode(",", $job_list[$i]); //разделяем по параметрам задание
		list ($relinks_ids, $dor_file_keys, $dor_num_keys, $enable_shuffle, $dor_templates, $path_remote, $path_local) =  array(trim($tmp_job_list[$i][0]), trim($tmp_job_list[$i][1]), trim($tmp_job_list[$i][2]), trim($tmp_job_list[$i][3]), trim($tmp_job_list[$i][4]), trim($tmp_job_list[$i][5]), trim($tmp_job_list[$i][6]));
		if ($cached_dor_keys[$dor_file_keys]=="") { //если файл ключей не кэширован, то кэшируем
			$dor_keys = file($keys_dir."/".$dor_file_keys); //читаем файл с кеями
			$dor_keys = massTrim($dor_keys); //чистим от \n
			$dor_keys = array_unique_own($dor_keys); //удаляем дубли ключей в массиве собственной функцией с учетом преобразования
			$cached_dor_keys[$dor_file_keys] = $dor_keys; //записываем в кэш результат чищеная база
		}
		else
			$dor_keys = $cached_dor_keys[$dor_file_keys]; // извлекаем чищеную базу из кэша
		
		if ($enable_shuffle) { //если включено перемешивание
			do {
				shuffle($dor_keys); //перемешиваем
				$dor_keys = array_rand_values($dor_keys, $dor_num_keys); //берем только необходимое кол-во ключей для одиночной генерации
			} while (in_array($dor_keys[0], (array)$a_primary_keys)); //пока выбранный главный кей не будет уникальным, чтобы исключить повторы главных ключей
		}
		else {
			$dor_keys = array_slice($dor_keys, 0, $dor_num_keys); //или берем перые dor_num_keys кеи
		}
		$a_primary_keys[] = $dor_keys[0]; //выбран уникальный главный ключ, его сохраняем в массиве главных ключей

		$total_key_dor = count($dor_keys); //получаем кол-во кеев
		$name_dir = key_to_filename($dor_keys[0]); //директория дора по кею главной страницы
		$path_remote = str_replace("{DOR}", $name_dir, $path_remote); //путь дора удаленно
		$path_local = str_replace("{DOR}", $name_dir, $path_local); //путь дора локально
		$job_list[$i] = $relinks_ids.",".$dor_file_keys.",".$dor_num_keys.",".$enable_shuffle.",".$dor_templates.",".$path_remote.",".$path_local;
		for ($x=0;$x<$total_key_dor;$x++) { //обработка по одной странице дора
			if ($x == 0)
				$name_file = "index".$extension;
			else
				$name_file = key_to_filename($dor_keys[$x], TRUE); //преобразовываем кеи в названия файла
			$a_all_dor_keys_filename[$i][$dor_keys[$x]] = $name_file; //заполняем массив номер_дора => (ключ => имя_файла)
			$log_ancor_temp = "<a href=\"".$path_remote."/".$name_file."\">".$dor_keys[$x]."</a>"; 
			$log_bbcode_temp = "[URL=".$path_remote."/".$name_file."]".$dor_keys[$x]."[/URL]";
			$logs_ancor .= $log_ancor_temp."\n"; //для записи в файл всех линков в формате html
			$logs_bbcode .= $log_bbcode_temp."\n"; //для записи в файл всех линков в формате BB code
			$logs_ancor_array[$i][] = $log_ancor_temp; //для использования в функции relinks перелинковки
			$logs_bbcode_array[] = $log_bbcode_temp; //для использования в % логов для спама
		}

		$logs_bbcode_spam .= get_perc_array($logs_bbcode_array, $num_perc_spam, 1); //собираем все BB линки страниц кол-вом % указанным в $num_perc_spam
		unset($logs_bbcode_array); //удаляем, так как новый, используется в % логов для спама
		unset($dor_keys);
		unset($name_file);
	}
}

{	//завершение формирования логов. сохранение логов происходит в самом конце
	$count_log_ancor = count($logs_ancor_array);

	@mkdir($out_dir."/".$job_name, 0777, true); //создаем папку с именем задания, куда будут сохранятся все логи и доры задания

	unset ($a_primary_keys, $cached_dor_keys);
	echo "Подготовка закончена. Заняло: ".(time()-$t4)." сек.<br>Начало генерации<br><script>scroll(0,999999);document.title='Начало генерации'</script>";
}
{	//генерируем все доры
	for($i=0;$i<$count_job;$i++) {
		$t1 = time();
		$a_rand_number = array(); //очищаем массив уникальных значений макроса URAND
		$a_rand_ancor = array(); //очищаем массив уникальных значений макроса RAND_ANCOR
		$a_rand_text = array(); //очищаем массив уникальных значений макроса RAND_TEXT
		$a_rand_url = array(); //очищаем массив уникальных значений макроса RAND_URL
		$a_mem_text = array(); //очищаем массив значений макроса MEM
		$a_page_rand = array(); //очищаем массив уникальных значений макроса PAGE_RAND
		$a_counter_text = array(); //очищаем массив значений меток макроса CNT
		$a_dor_mem_text = array(); //очищаем массив значений макроса DOR_MEM
		$relinks_ids_array = array(); //очищаем массив значений id доров для внешней перелинковки для макроса relinks
		unset($dor_rand_number); //очищаем случайное значение макроса DOR__RAND, которое использовалось при генерации предыдущего дора
		unset($dor_urand_number); //очищаем случайное значение макроса DOR__URAND, которое использовалось при генерации предыдущего дора
		unset($maps); //очищаем строку со ссылками на карты дора
		list ($relinks_ids, $dor_file_keys, $dor_num_keys, $enable_shuffle, $templ_this, $path_remote, $path_local) = explode(",", $job_list[$i]); //читаем очередное задание
		if ($relinks_ids == '') { //если пустой параметр перелинковки, то заполняем параметр перелинковки всеми заданиями кроме текущего
			for ($xxx=1;$xxx<=$count_job;$xxx++) {
				if ($xxx != ($i + 1))
					$relinks_ids_array[] = $xxx;
			}
		} else
			$relinks_ids_array = explode(" ", $relinks_ids); //заполняем параметр перелинковки из задания
		echo "<b>Генерируем дор #".($i+1)."</b> (".$dor_file_keys.", <font color=\"#FF0000\">".$templ_this."</font>, <font color=\"#32CD32\">".$path_remote."</font>, <font color=\"#000080\">".$path_local."</font>)<script>scroll(0,999999);document.title='Дор #".($i+1)." / ".$count_job."'</script>";
//		echo "Перелинковка с: <pre>";
//		print_r($relinks_ids_array);
//		echo "</pre>";
		echo "<p style=\"margin-left: 3em;\">Взяли шаблон: ".$templ_this."<br>";
		if (!include ($templ_dir."/".$templ_this."/custom_macros.php"))
			die ('<b>Ошибка</b>: В папке с шаблоном '.$templ_dir."/".$templ_this.' отсутсвует обязательный файл custom_macros.php');
		$templ_index = file_get_contents($templ_dir."/".$templ_this."/index.txt") or die("<b>Ошибка</b>: Не найден файл шаблона. Проверьте: ".$templ_dir."/".$templ_this."/index.txt"); 
		$templ_page = file_get_contents($templ_dir."/".$templ_this."/page.txt") or die("<b>Ошибка</b>: Не найден файл шаблона. Проверьте: ".$templ_dir."/".$templ_this."/page.txt");
		$templ_map = file_get_contents($templ_dir."/".$templ_this."/map.txt") or die("<b>Ошибка</b>: Не найден файл шаблона. Проверьте: ".$templ_dir."/".$templ_this."/map.txt");
		$dor_keys = array_keys($a_all_dor_keys_filename[$i]); //берем кеи из массива ключевиков по каждому дору
		$a_key_filename = $a_all_dor_keys_filename[$i]; //берем массив кей => имя файла для кадждого дора
		$total_key_dor = count($dor_keys); //считаем кол-во всех ключей текущего дора
		echo "Взяли ключей: ".$total_key_dor."<br>";
		$name_dir = key_to_filename($dor_keys[0]); //имя папки дора
		$keyword_main = $dor_keys[0]; //кей главной страницы с маленькой
		$bkeyword_main = ucfirst($dor_keys[0]); //кей главной страницы с большой 
		$index = "<a href=\"".$a_key_filename[$keyword_main]."\">".$text_ancor_index_link."</a>"; //ссылка на главную страницу дора
		$path_local = $out_dir."/".$job_name."/".$path_local.($path_local!="" ? "/" : null); //путь дора локально
		echo "<a href=\"".$path_remote."\" target=\"_blank\">URL</a> дора<br>"; //путь дора удаленно
		echo "Локальный путь дора: <a href=\"".$path_local."\" target=\"_blank\">здесь</a><br>";
		@mkdir($path_local, 0777, true); //создать папку текущего дора, куда запишутся все страницы. рекурсивно

		{	//генерируем карты и записываем на диск, а также получаем массив с линками на карты
			generate_map($path_local, $count_ancor_in_map);
			echo "Сгенерировали карты дора<br>";
		}

		{	 //копируем все объекты из папки с шабом в папку с дором, при этом не копируя файлы шаблонов и p_*.txt
			recurse_copy($templ_dir."/".$templ_this, $path_local);
			echo "Все объекты из ".$templ_this." скопированы в папку с дором<br>";
		}

		if ($generate_sitemap_xml) {
			create_sitemap_xml($path_local); //создаем sitemap.xml
			echo "Файл <a href=\"".$path_local."sitemap.xml\" target=\"_blank\">sitemap.xml</a> готов<br>";
		}

		if ($generate_robots_txt) {
			create_robots_txt($path_local); //создаем robots.txt
			echo "Файл <a href=\"".$path_local."robots.txt\" target=\"_blank\">robots.txt</a> готов<br>";
		}
		unset($links_map); //очищаем массив ссылок из sitemap
		
		{	//генерируем кастомные паги
			$cp = create_custom_page($path_local);
			echo "Генерация пользовательских страниц завершена: ".$cp."<br>";
		}

		for ($cur_page_num=0;$cur_page_num<$total_key_dor;$cur_page_num++) {  //обработка страниц дора
			$a_rand_number = array(); //очищаем массив уникальных значений макроса URAND
			$a_rand_ancor = array(); //очищаем массив уникальных значений макроса RAND_ANCOR
			$a_rand_text = array(); //очищаем массив уникальных значений макроса RAND_TEXT
			$a_rand_url = array(); //очищаем массив уникальных значений макроса RAND_URL
			$a_mem_text = array(); //очищаем массив значений макроса MEM
			$keyword = $dor_keys[$cur_page_num]; //кей страницы
			$name_file = $a_key_filename[$dor_keys[$cur_page_num]]; //имя файла берем из массива: ключ => имя файла. сгенеренного вначале
			if ($cur_page_num == 0) //если 0 кей - это главная страница
				$out_page = replace_macros_page($templ_index, $access_macros_index); //если страница индексная обработать index.txt шаблон
			else
				$out_page = replace_macros_page($templ_page, $access_macros_page); //если страница индексная обработать page.txt шаблон
			if ($compression_template) //если включена компрессия готовых страниц то сжимаем готовую страницу перед сохранением
				$out_page = compression_text($out_page);
			file_put_contents($path_local.$name_file, $out_page, FILE_APPEND); //сохраняем страницу в папку дора
		}
		echo "Дор готов. Сгенерирован за: ".(time()-$t1)." секунд</p><script>scroll(0,999999);</script></p>";
	}
}

{	//завершающие операции
	echo "Сетка сгенерирована<br><script>scroll(0,999999);document.title='Сетка сгенерирована'</script>";
	if ($enable_packing) { //если включена запаковка в zip
		$t2 = time();
		include ("lib/pclzip.lib.php");
		try {
			$zip_filename = $job_name.".zip"; //формируем полное имя файла zip
//			@unlink($out_dir."/".$zip_filename); //предварительно удалить zip файл, так как он дописывает в него, что неправильно
			$zip = new PclZip($out_dir."/".$zip_filename); //создаем экземпляр класса указав имя будущего зипа
			if ($zip->create($out_dir."/".$job_name, PCLZIP_OPT_REMOVE_PATH, $out_dir."/".$job_name)) //создаем зип из папки задания, причем игнорируя путь до out/[название_задания]
				echo "Zip создан. <a href=\"".$out_dir."/".$zip_filename."\" target=\"_blank\">".$zip_filename."</a>. ";
			else
				echo "<u>Ошибка создания zip.</u> ";
			echo "Заняло: ".(time()-$t2)." секунд<br>";
			if ($extract_zip_archive) { //если включена опция для автоматического разархивирования на сервере, то..
				$extract_filename = create_extract_php($out_dir, $job_name, $zip_filename); //..создаем php файл для авторазархивирования на сервере и получаем имя файла, для добавления к очереди загрузки на ftp
				echo "Файл для автоматического разархивирования подготовлен<br>";
			}

			if ($upload_ftp) { //если разрешено, то и закачиваем его по ftp
				$t3 = time();
				echo "Началась выгрузка ".$zip_filename." по ftp. Не закрывайте окно. Это может занять несколько минут<br><script>scroll(0,999999);</script>";
				$conn_id = ftp_connect($default_ftp_host, $default_ftp_port, 10); //соединяемся с ftp хостом, 10 секунд таймаут
				if (!$conn_id)
					throw new Exception("Нет коннекта с указанным хостом: ".$default_ftp_host."<br>");
				else
					echo "Осуществлен коннект с хостом: ".$default_ftp_host."<br>";
				if (!@ftp_login($conn_id, $default_ftp_login, $default_ftp_password)) //логинимся к хосту
					throw new Exception("Ошибка авторизации, юзер: ".$default_ftp_login."<br>");
				else
					echo "Авторизовались, юзер: ".$default_ftp_login."<br>Выгружаем, ждите... <script>scroll(0,999999);</script>";
				ftp_pasv($conn_id, true); //переводим в пассивный режим
				if ((ftp_put($conn_id, $default_ftp_path."/".$zip_filename, $out_dir."/".$zip_filename, FTP_BINARY)) and (ftp_put($conn_id, $default_ftp_path."/".$extract_filename, $out_dir."/".$extract_filename, FTP_BINARY))) //заливаем прочтенный zip на ftp, используя это же имя и заданный путь
					echo "файлы загружены успешно<br>";
				else
					echo "<u>файлы не загружены. Произошел сбой</u><br>";
				ftp_close($conn_id); //закрыть соединение с ftp
				echo "Выгрузка на ftp сервер закончена. Заняло: ".(time()-$t3)." секунд<br>";
				if ($extract_zip_archive) { //если включена опция для автоматического разархивирования на сервере, то пытаемся достучатся до скрипта
					echo "Попытка автоматически распаковать архив по адресу: http://".$default_ftp_host."/".$extract_filename."..";
					$answer = @file_get_contents("http://".$default_ftp_host."/".$extract_filename);
					echo $answer;
				}
			}
		} catch (Exception $e) {
			echo $e->getMessage(); //если че, материмся
		}
	}

	$all_logs_ancor = $logs_ancor;

	if ($insert_sitemaps_links_in_all_ancor_log)
		$all_logs_ancor = $maps_ancor.$all_logs_ancor;
	if ($insert_sitemaps_links_in_ancor_log)
		$logs_ancor = $maps_ancor.$logs_ancor;
	if ($insert_sitemaps_links_in_bbcode_log)
		$logs_bbcode = $maps_bb.$logs_bbcode;
	if ($insert_sitemaps_links_in_bbcode_log_spam)
		$logs_bbcode_spam = $maps_bb.$logs_bbcode_spam;

	$log_all_ancor = "all_ancor_log.txt"; //лог с анкорами всех доров всех пачек
	$log_ancor_file_name = $job_name."_ancor_log.txt"; //лог с анкорами
	$log_bbcode_file_name = $job_name."_bbcode_log.txt"; //лог с BB кодами для хрумера
	$log_bbcode_file_name_spam = $job_name."_bbcode_log_spam.txt"; //лог с BB кодами для хрумера с указанным соотношением
	echo "Логи для спама: <b><a target=\"_blank\" href=\"".$out_dir."/".$log_bbcode_file_name_spam."\">".$log_bbcode_file_name_spam."</a></b> (".($num_perc_spam*100)."% BB код) и <a target=\"_blank\" href=\"".$out_dir."/".$log_ancor_file_name."\">".$log_ancor_file_name."</a> и <a target=\"_blank\" href=\"".$out_dir."/".$log_bbcode_file_name."\">".$log_bbcode_file_name."</a><br>";

	file_put_contents($out_dir."/".$log_all_ancor, $all_logs_ancor, FILE_APPEND); //сохраняем all_ancor_log.txt
	file_put_contents($out_dir."/".$log_ancor_file_name, $logs_ancor, FILE_APPEND); //сохраняем *_ancor_log.txt
	file_put_contents($out_dir."/".$log_bbcode_file_name, $logs_bbcode, FILE_APPEND); //сохраняем *_bbcode_log.txt
	file_put_contents($out_dir."/".$log_bbcode_file_name_spam, $logs_bbcode_spam, FILE_APPEND); //сохраняем *_bbcode_log_spam.txt

	echo "Сетка доров готова. Заняло ".(time()-$time_start)." секунд. Папка: <b><a href=\"".$out_dir."/\" target=\"_blank\">".$out_dir."</a></b><br>";
 	echo "<b>Спасибо за использование моего доргена. Всегда свежую версию вы можете найти на сайте <a href='http://seodor.ru/dorgen/' target='_blank'>http://seodor.ru/dorgen/</a></b><script>scroll(0,999999);document.title='Все готово! '</script>";
}
?>