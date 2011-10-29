<?
	//--Описание макросов-------------
	function replace_macros_page ($text	/* исходный текст*/, $access_macros /* массив разрешенных/запрещенных максросов */ = array (
		/* 0  */	TRUE /* custom_macros */,
		/* 1  */	TRUE /* FOR /FOR */,
		/* 2  */	TRUE /* [[|]] */,
		/* 3  */	TRUE /* URAND */,
		/* 4  */	TRUE /* RAND */,
		/* 5  */	TRUE /* DOR_URAND */,
		/* 6  */	TRUE /* DOR_RAND */,
		/* 7  */	TRUE /* RAND_TEXT, BRAND_TEXT, BBRAND_TEXT */,
		/* 8  */	TRUE /* DOR_TEXT */,
		/* 9  */	TRUE /* LINE_FILE */,
		/* 10 */	TRUE /* LINKS, BLINKS, BBLINKS */,
		/* 11 */	TRUE /* RELINKS */,
		/* 12 */	TRUE /* RAND_KEY */,
		/* 13 */	TRUE /* RAND_URL */,
		/* 14 */	TRUE /* RAND_ANCOR */,
		/* 15 */	TRUE /* MAPS */,
		/* 16 */	TRUE /* PREV_PAGE */,
		/* 17 */	TRUE /* NEXT_PAGE */,
		/* 18 */	TRUE /* MKEYWORD, BMKEYWORD, BBMKEYWORD */,
		/* 19 */	TRUE /* KEYWORD, BKEYWORD, BBKEYWORD */,
		/* 20 */	TRUE /* INDEX */,
		/* 21 */	TRUE /* MAP_LINKS */,
		/* 22 */	TRUE /* MIX_TEXT */,
		/* 23 */	TRUE /* CURR_PAGE */,
		/* 24 */	TRUE /* DOR_URL */,
		/* 25 */	TRUE /* DOR_HOST */,
		/* 26 */	TRUE /* MEM /MEM, INS */,
		/* 27 */	TRUE /* PAGE_RAND */,
		/* 28 */	TRUE /* CNT /CNT */,
		/* 29 */	TRUE /* DOR_MEM /DOR_MEM, DOR_INS */,
		/* 30 */	TRUE /* JOB_RAND */,
		/* 31 */	TRUE /* SNIPPET */
	)) {
		$all_macros = array();

		if ($access_macros[0]) { //реализация пользовательских макросов
			global $custom_macros;
			if (isset($custom_macros)) {
				$custom_macros_values = array_keys($custom_macros);
				$custom_macros_replace_values = array_values($custom_macros);
				for ($x=0;$x<count($custom_macros_values);$x++)
					$all_macros[] = $custom_macros_values[$x] = "/".$custom_macros_values[$x]."/U";
				$text = preg_replace($custom_macros_values, $custom_macros_replace_values, $text);
			}
		}

		if ($access_macros[1]) {
			//$macros = "/{FOR_(\d*)_(\d*)}(.*){\/FOR}/Us";
			$macros1 = "/{FOR\((\d*),(\d*)\)}(.*){ENDFOR}/Us";
			$macros2 = "/{FOR\((\d*),{RAND\((\d*),(\d*)\)}\)}(.*){ENDFOR}/Us";
			$macros3 = "/{FORX\((\d*),(\d*)\)}(.*){ENDFORX}/Us";
			$macros4 = "/{FORX\((\d*),{RAND\((\d*),(\d*)\)}\)}(.*){ENDFORX}/Us";
			$text = preg_replace_callback($macros1, "for_endfor", $text);
			$text = preg_replace_callback($macros2, "for_endfor", $text);
			$text = preg_replace_callback($macros3, "for_endfor", $text);
			$text = preg_replace_callback($macros4, "for_endfor", $text);
			$all_macros[] = $macros1;
			$all_macros[] = $macros2;
			$all_macros[] = $macros3;
			$all_macros[] = $macros4;
		}

		$text = add_page_key($text);

		if ($access_macros[2]) {
			$macros = "/\[\[([^(\[\[)(\]\])]*)\]\]/U";
			$text = preg_replace_callback($macros, "select", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[23]) {
			$macros = "/{CURR_PAGE}/";
			$text = preg_replace_callback($macros, "curr_page", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[24]) {
			$macros = "/{DOR_URL}/";
			$text = preg_replace_callback($macros, "dor_url", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[25]) {
			$macros = "/{DOR_HOST}/";
			$text = preg_replace_callback($macros, "dor_host", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[27]) {
			$macros = "/{PAGE_RAND_(.*)_(\d*)_(\d*)}/U";
			$text = preg_replace_callback($macros, "page_rand", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[3]) {
			$macros = "/{URAND_(\d*)_(\d*)}/U";
			$text = preg_replace_callback($macros, "urand_number", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[4]) {
			//$macros = "/{RAND_(\d*)_(\d*)}/U";
			$macros = "/({(RAND)\((\d*),(\d*)\)}|{(COUNTRAND)})/U";
			$text = preg_replace_callback($macros, "rand_number", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[30]) {
			$macros = "/{JOB_RAND_(.*)_(\d*)_(\d*)}/U";
			$text = preg_replace_callback($macros, "job_rand_number", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[5]) {
			$macros = "/{DOR_URAND_(.*)_(\d*)_(\d*)}/U";
			$text = preg_replace_callback($macros, "dor_urand_number", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[6]) {
			$macros = "/{DOR_RAND_(.*)_(\d*)_(\d*)}/U";
			$text = preg_replace_callback($macros, "dor_rand_number", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[28]) {
			$macros = "/{CNT_(.*)_(\d*)_(\d*)}(.*){\/CNT}/Us";
			$text = preg_replace_callback($macros, "counter", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[10]) {
			$macros = "/{(B?B?)LINKS_(\d*)_(\d*)_(.*)}/U";
			$text = preg_replace_callback($macros, "links", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[11]) {
			$macros =  "/{RELINKS_(\d*)_(\d*)_(.*)}/U";
			$text = preg_replace_callback($macros, "relinks", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[12]) {
			$macros = "/{(B?B?)RAND_KEY_(\d*)_(\d*)_(.*)}/U";
			$macros2 = "/{(B?B?)RAND_KEY}/U";
			$text = preg_replace_callback($macros, "rand_key", $text);
			$text = preg_replace_callback($macros2, "rand_key", $text);
			$all_macros[] = $macros;
			$all_macros[] = $macros2;
		}

		if ($access_macros[13]) {
			$macros = "/{RAND_URL}/";
			$text = preg_replace_callback($macros, "rand_url", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[14]) {
			$macros = "/{(B?B?)RAND_ANCOR}/U";
			$text = preg_replace_callback($macros, "rand_ancor", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[15]) {
			$macros = "/{MAPS_(.*)}/U";
			$text = preg_replace_callback($macros, "maps", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[16]) {
			$macros = "/{PREV_PAGE_(\d*)_(.*)}/U";
			$text = preg_replace_callback($macros, "prev_page", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[17]) {
			$macros = "/{NEXT_PAGE_(\d*)_(.*)}/U";
			$text = preg_replace_callback($macros, "next_page", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[18]) {
			$macros = "/{(B?B?)MKEYWORD}/";
			$text = preg_replace_callback($macros, "mkeyword", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[19]) {
			$macros = "/{(B?B?)KEYWORD}/";
			$text = preg_replace_callback($macros, "keyword", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[20]) {
			$macros = "/{INDEX(?:_(\d*))?}/U";
			$text = preg_replace_callback($macros, "index_link", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[21]) {
			$macros = "/{MAP_LINKS_(.*)}/U";
			$text = preg_replace_callback($macros, "map_links", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[7]) {
			$macros = "/{(B?B?)RAND_TEXT_(.*)_(\d*)_(\d*)_(.*)_(.*)}/U";
			//$macros2 = "/{(B?B?)RAND_TEXT_(.*)}/U";
			$macros2 = "/{(B?B?)RANDTEXTLINE\((.*)\)}/U";
			$text = preg_replace_callback($macros, "rand_text", $text);
			$text = preg_replace_callback($macros2, "rand_text", $text);
			$all_macros[] = $macros;
			$all_macros[] = $macros2;
		}
		
		if ($access_macros[8]) {
			$macros = "/{DOR_TEXT_(.*)}/U";
			$text = preg_replace_callback($macros, "dor_text", $text);
			$all_macros[] = $macros;
		}
		
		if ($access_macros[9]) {
			$macros = "/{LINE_FILE_(.*)_(\d*)}/U";
			$text = preg_replace_callback($macros, "line_file", $text);
			$all_macros[] = $macros;
		}

		if ($access_macros[22]) {
			$macros = "/{MIX_TEXT_(.*)_(.*)_(.*)}/U";
			$text = preg_replace_callback($macros, "mix_text", $text);
			$all_macros[] = $macros;
		}

 		if ($access_macros[26]) {
			$macros = "/{MEM_(.*)}(.*){\/MEM}/U";
			$text = preg_replace_callback($macros, "mem", $text);
			$macros2 = "/{INS_(.*)}/U";
			$text = preg_replace_callback($macros2, "ins", $text);
			$all_macros[] = $macros;
			$all_macros[] = $macros2;
		}

 		if ($access_macros[29]) {
			$macros = "/{DOR_MEM_(.*)}(.*){\/DOR_MEM}/U";
			$text = preg_replace_callback($macros, "dor_mem", $text);
			$macros2 = "/{DOR_INS_(.*)}/U";
			$text = preg_replace_callback($macros2, "dor_ins", $text);
			$all_macros[] = $macros;
			$all_macros[] = $macros2;
		}

		if ($access_macros[31]) {
			$macros = "/{(B?B?)SNIPPET\((.*)\)}/U";
			$text = preg_replace_callback($macros, "snippet", $text);
			$all_macros[] = $macros;
		}
		
		foreach ($all_macros as $macros) {
			if (preg_match($macros, $text)) {
				$text = replace_macros_page($text, $access_macros);
//				break;
			}
		}
		return $text;
	}
	//--------------------------------

	//--Описание генератора карты-----
	function generate_map($path_local, $count_ancor_in_map) {
		global $links_map, $maps, $dor_keys, $extension, $a_key_filename, $dor_num_pages, $text_ancor_sitemap_links, $templ_map, $a_rand_number, $a_rand_ancor, $a_rand_text, $a_rand_url, $insert_sitemaps_links_in_all_ancor_log, $insert_sitemaps_links_in_ancor_log, $insert_sitemaps_links_in_bbcode_log, $insert_sitemaps_links_in_bbcode_log_spam, $path_remote, $maps_bb, $maps_ancor, $a_mem_text, $access_macros_text_ancor_sitemap_links, $access_macros_sitemap;
		$count_map_files = ceil($dor_num_pages/$count_ancor_in_map);
		$curr_text_ancor_sitemap_links = replace_macros_page($text_ancor_sitemap_links,	$access_macros_text_ancor_sitemap_links);

		for ($x=1;$x<=$count_map_files;$x++) {
			$num_sitemap = ($x==1 ? null : $x);
			$maps[] = "<a href=\"sitemap".$num_sitemap.$extension."\">".$curr_text_ancor_sitemap_links.$num_sitemap."</a>";
		}

		for ($x=1;$x<=$count_map_files;$x++) {
			$a_rand_number = array(); //очищаем массив уникальных значений макроса URAND
			$a_rand_ancor = array(); //очищаем массив уникальных значений макроса RAND_ANCOR
			$a_rand_text = array(); //очищаем массив уникальных значений макроса RAND_TEXT
			$a_rand_url = array(); //очищаем массив уникальных значений макроса RAND_URL
			$a_mem_text = array(); //очищаем массив значений макроса MEM
			$links_map = array(); //очищаем массив ссылок на страницы
			for ($v=($x-1)*$count_ancor_in_map;(($v<$x*$count_ancor_in_map) and ($v<$dor_num_pages));$v++) {
				$ancor = $a_key_filename[$dor_keys[$v]];
				$links_map[] = "<a href=\"".$ancor."\">".$dor_keys[$v]."</a>";
			}
	
			$num_sitemap = ($x==1 ? null : $x);

			$maps_bb .= "[URL=".$path_remote."/sitemap".$num_sitemap.$extension."]".$curr_text_ancor_sitemap_links.$num_sitemap."[/URL]\n";
			$maps_ancor .= "<a href=\"".$path_remote."/sitemap".$num_sitemap.$extension."\">".$curr_text_ancor_sitemap_links.$num_sitemap."</a>\n";

			$copy_text[$x] = $templ_map;
			$copy_text[$x] = preg_replace('/\{NUM_SITEMAP\}/', $x, $copy_text[$x]);
			$copy_text[$x] = replace_macros_page($copy_text[$x], $access_macros_sitemap);
			if ($compression_template)
				$copy_text[$x] = compression_text($copy_text[$x]);
			file_put_contents($path_local."sitemap".$num_sitemap.$extension, $copy_text[$x], FILE_APPEND);
		}
	}


	//--Генерация пользовательских страниц-----
	function create_custom_page($path_local) {
		global $templ_dir, $templ_this, $a_rand_number, $a_rand_ancor, $a_rand_text, $a_rand_url, $a_mem_text, $access_macros_custom_page, $compression_template;
		$i = 0;
		$custom_template_files = get_all_files_in_dir($templ_dir."/".$templ_this);
		if (count($custom_template_files) > 0) {
			foreach ($custom_template_files as $custom_template_file) {
				$a_rand_number = array(); //очищаем массив уникальных значений макроса URAND
				$a_rand_ancor = array(); //очищаем массив уникальных значений макроса RAND_ANCOR
				$a_rand_text = array(); //очищаем массив уникальных значений макроса RAND_TEXT
				$a_rand_url = array(); //очищаем массив уникальных значений макроса RAND_URL
				$a_mem_text = array(); //очищаем массив значений макроса MEM
				$custom_template = file_get_contents($custom_template_file);
				$custom_template = replace_macros_page($custom_template, $access_macros_custom_page);
				$custom_template_file = substr ($custom_template_file, (strlen($templ_dir."/".$templ_this)+1));
				$custom_template_file = preg_replace("/t_/", "", $custom_template_file);
				if ($compression_template)
					$custom_template = compression_text($custom_template);
				file_put_contents($path_local."/".$custom_template_file, $custom_template);
				$i++;
			}
		}
		return $i;
	}
	//--------------------------------

	//-----------------------
	//Начало описания макросов

	function page_rand($matches) { //"/{PAGE_RAND_(.*)_(\d*)_(\d*)}/U"
		global $a_page_rand, $cur_page_num;
		if (!isset($a_page_rand[$matches[1]])) {
			$end = $matches[3]-$matches[2];
			for ($x=1;$x<=$end;$x++) {
				do {
					$z = mt_rand($matches[2], $matches[3]);
				} while (in_array($z, (array)$a_page_rand[$matches[1]]));
				$a_page_rand[$matches[1]][$x] = $z;
			}
		}
		$res = $a_page_rand[$matches[1]][$cur_page_num];
		return $res;
	}

	function urand_number($matches) {
		global $a_rand_number;
		do {
			$z = mt_rand($matches[1], $matches[2]); //сгенерировать случайное значение из указанных границ
		} while (in_array($z, $a_rand_number)); //повторять генерацию, пока будут совпадения сгенерированного числа с массивом использованных ранее значений
		$a_rand_number[] = $z; //сгенерировалось уникальное значение, записать в массив использованных значений
		return $z;
	}

	$rand_number_mem = 0;
	function rand_number($matches) {
		global $rand_number_mem;
		if ($matches[2] == 'RAND') {
			$z = mt_rand($matches[3], $matches[4]); //сгенерировать случайное значение из указанных границ
			$rand_number_mem = $z;
		}
		else
			$z = $rand_number_mem;
		return $z;
	}

	function job_rand_number($matches) {
		global $JOB_RAND_number;
		if (isset($JOB_RAND_number[$matches[1]]))
			$z = $JOB_RAND_number[$matches[1]];
		else {
			$z = mt_rand($matches[2], $matches[3]); //сгенерировать случайное значение из указанных границ
			$JOB_RAND_number[$matches[1]] = $z; //сгенерировалось уникальное значение, записать в массив использованных значений
		}
		return $z;
	}

	function dor_rand_number($matches) {
		global $dor_rand_number;
		if (isset($dor_rand_number[$matches[1]]))
			$z = $dor_rand_number[$matches[1]];
		else {
			$z = mt_rand($matches[2], $matches[3]); //сгенерировать случайное значение из указанных границ
			$dor_rand_number[$matches[1]] = $z; //сгенерировалось уникальное значение, записать в массив использованных значений
		}
		return $z;
	}

	function dor_urand_number($matches) {
		global $dor_urand_number, $a_dor_urand_number;
		if (isset($dor_urand_number[$matches[1]]))
			$z = $dor_urand_number[$matches[1]];
		else {
			do {
				$z = mt_rand($matches[2], $matches[3]); //сгенерировать случайное значение из указанных границ
			} while (in_array($z, (array)$a_dor_urand_number[$matches[1]]));
			$a_dor_urand_number[$matches[1]][] = $dor_urand_number[$matches[1]] = $z; //сгенерировалось уникальное значение, записать в массив использованных значений
		}
		return $z;
	}

	function rand_key($matches) {
		global $dor_keys, $keyword, $total_key_dor;
		if (!isset($matches[2]) and !isset($matches[3]))
			$matches[2] = $matches[3] = 1;
		$cp = mt_rand($matches[2], $matches[3]);
		for ($x=1;$x<=$cp;$x++) {
			do {
				$z = $dor_keys[mt_rand(0, ($total_key_dor-1))];
			} while ($z == $keyword);
			switch ($matches[1]) {
				case "B": $res = ucfirst($z); break;
				case "BB": $res = ucwords($z); break;
				default: $res = $z;
			}
			$result .= $res.($x==$cp ? null : $matches[4]);
		}
		return $result;
	}

	function rand_url($matches) {
		global $dor_keys, $keyword, $a_key_filename, $a_rand_url, $dor_num_pages;
		//do {
			$z = mt_rand(0, ($dor_num_pages-1));
		//} while (($dor_keys[$z] == $keyword) or (in_array($z, $a_rand_url)));
		$a_rand_url[] = $z;
		return $a_key_filename[$dor_keys[$z]];
	}

	function rand_ancor($matches) {
		global $dor_keys, $keyword, $a_key_filename, $a_rand_ancor, $dor_num_pages;
		//do {
			$z = mt_rand(1, ($dor_num_pages-1));
		//} while (($dor_keys[$z] == $keyword) or (in_array($z, $a_rand_ancor)));
		$z1 = $a_key_filename[$dor_keys[$z]];
		$a_rand_ancor[] = $z;
		switch ($matches[1]) {
			case "B": $res = ucfirst($dor_keys[$z]); break;
			case "BB": $res = ucwords($dor_keys[$z]); break;
			default: $res = $dor_keys[$z];
		}
		return "<a href=\"".$z1."\">".$res."</a>";
	}

	function rand_text($matches) { //{(B?B?)RAND_TEXT_(.*)_(\d*)_(\d*)_(.*)_(.*)}
		global $text_dir, $a_rand_text;
		$text = cache_file($text_dir."/".$matches[2]);
		if (!isset($matches[3]) and !isset($matches[4]))
			$matches[3] = $matches[4] = 1;
		if (!isset($matches[5]) or $matches[5]=='\n')
			$a_text = explode ("\n", $text);
		else
			$a_text = explode ($matches[5], $text);
		$num_lines = count($a_text);
		$cp = mt_rand($matches[3], $matches[4]);
		for ($x=1;$x<=$cp;$x++) {
			do {
				$z = mt_rand(0, (count($a_text)-1));
			} while (in_array($z, (array)$a_rand_text[$matches[2]]) and ($num_lines > $cp) and ($num_lines > count((array)$a_rand_text[$matches[2]])));
			$a_rand_text[$matches[1]][] = $z;
			switch ($matches[1]) {
				case "B": $txt = ucfirst(trim($a_text[$z])); break;
				case "BB": $txt = ucwords(trim($a_text[$z])); break;
				default: $txt = trim($a_text[$z]);
			}
			$result .= $txt.$matches[6];
		}
		return $result;
	}

	function snippet($matches) { //{(B?B?)RAND_TEXT_(.*)_(\d*)_(\d*)_(.*)_(.*)}
		global $snippet_dir, $a_rand_text;
		$text = cache_file($snippet_dir."/".$matches[2]);
		if (!isset($matches[3]) and !isset($matches[4]))
			$matches[3] = $matches[4] = 1;
		if (!isset($matches[5]) or $matches[5]=='\n')
			$a_text = explode ("\n", $text);
		else
			$a_text = explode ($matches[5], $text);
		$num_lines = count($a_text);
		$cp = mt_rand($matches[3], $matches[4]);
		for ($x=1;$x<=$cp;$x++) {
			do {
				$z = mt_rand(0, (count($a_text)-1));
			} while (in_array($z, (array)$a_rand_text[$matches[2]]) and ($num_lines > $cp) and ($num_lines > count((array)$a_rand_text[$matches[2]])));
			$a_rand_text[$matches[1]][] = $z;
			switch ($matches[1]) {
				case "B": $txt = ucfirst(trim($a_text[$z])); break;
				case "BB": $txt = ucwords(trim($a_text[$z])); break;
				default: $txt = trim($a_text[$z]);
			}
			$result .= $txt.$matches[6];
		}
		return $result;
	}

	function relinks($matches) {
		global $logs_ancor_array, $count_job, $relinks_ids_array;
		if (($count_job > 1) and ($relinks_ids_array[0] != 0)) {
			$cp = mt_rand($matches[1], $matches[2]);
			for ($x=1;$x<=$cp;$x++) {
				$xx = $relinks_ids_array[(mt_rand(1, count($relinks_ids_array)) - 1)];
				$res = $logs_ancor_array[($xx-1)][mt_rand(0, (count($logs_ancor_array[($xx-1)])-1))];
				$result .= $res.($x==$cp ? null : $matches[3]);
			}
		}
		return $result;
	}

	function select($matches) {
		$arr = explode("|", $matches[1]);
		$result = $arr[mt_rand(0, (count($arr)-1))];
		return $result;
	}

	function dor_text($matches) {
		global $text_dir, $i;
		$text = cache_file($text_dir."/".$matches[1]);
		$a_text = explode ("\n", $text);
		return trim($a_text[$i]);
	}

	function line_file($matches) {
		global $text_dir;
		$text = cache_file($text_dir."/".$matches[1]);
		$a_text = explode ("\n", $text);
		return trim($a_text[($matches[2]-1)]);
	}

	function links($matches) {
		global $dor_keys, $keyword, $a_key_filename, $a_rand_ancor, $dor_num_pages;
		$cp = mt_rand($matches[2], $matches[3]);
		for ($x=1;$x<=$cp;$x++) {
			do {
				$z = mt_rand(1, ($dor_num_pages-1));
			} while (($dor_keys[$z] == $keyword) or (in_array($z, $a_rand_ancor)));
			$z1 = $a_key_filename[$dor_keys[$z]];
			$a_rand_ancor[] = $z;
			switch ($matches[1]) {
				case "B": $ancor = ucfirst($dor_keys[$z]); break;
				case "BB": $ancor = ucwords($dor_keys[$z]); break;
				default: $ancor = $dor_keys[$z];
			}
			$result .= "<a href=\"".$z1."\">".$ancor."</a>".($x==$cp ? null : $matches[4]);
		}
		return $result;
	}

	function maps($matches) {
		global $maps;
		$count_map_links = count($maps);
		for ($x=0;$x<$count_map_links;$x++) {	
			$links_sitemap .= $maps[$x].($x==($count_map_links-1) ? null : $matches[1]);
		}
		return $links_sitemap;
	}

	function prev_page($matches) {
		global $dor_keys, $a_key_filename, $cur_page_num;
		for ($x=1;$x<=(int)$matches[1];$x++) {
			$xx = $cur_page_num - $x;
			if ($xx>1)
				$result = $matches[2]."<a href=\"".$a_key_filename[$dor_keys[$xx]]."\">".$xx."</a>".$result;
		}
		if ($cur_page_num>1)
			$result = "<a href=\"".$a_key_filename[$dor_keys[1]]."\">First</a>".$result;
		return $result;
	}

	function next_page($matches) {
		global $dor_num_pages, $dor_keys, $a_key_filename, $cur_page_num;
		for ($x=1;$x<=(int)$matches[1];$x++) {
			$xx = $cur_page_num + $x;
			if ($xx<($dor_num_pages-1))
				$result = $result."<a href=\"".$a_key_filename[$dor_keys[$xx]]."\">".$xx."</a>".$matches[2];
		}
		if ($cur_page_num<($dor_num_pages-1))
			$result = $result."<a href=\"".$a_key_filename[$dor_keys[($dor_num_pages-1)]]."\">Last</a>";
		return $result;
	}

	function for_endfor($matches) {
		if (!isset($matches[4])) {
			for ($x=$matches[1];$x<=$matches[2];$x++) {
			$tmp = $matches[3];
				$tmp = preg_replace('/{FOR_NUM}/', $x, $tmp);
				$res .= $tmp;
			}
		}
		else {
	 		for ($x=$matches[1];$x<=mt_rand($matches[2], $matches[3]);$x++) {
			$tmp = $matches[4];
				$tmp = preg_replace('/{FOR_NUM}/', $x, $tmp);
				$res .= $tmp;
			}
		}
		return $res;
	}

	function mkeyword($matches) {
		global $keyword_main;
		switch ($matches[1]) {
			case "B": $res = ucfirst($keyword_main); break;
			case "BB": $res = ucwords($keyword_main); break;
			default: $res = $keyword_main;
		}
		return $res;
	}

	function keyword($matches) {
		global $keyword;
		switch ($matches[1]) {
			case "B": $res = ucfirst($keyword); break;
			case "BB": $res = ucwords($keyword); break;
			default: $res = $keyword;
		}
		return $res;
	}

	function index_link($matches) {
		global $logs_ancor_array, $i;
		if ($matches[1] == '')
			$dor = $i ;
		else
			$dor = ($matches[1] - 1);
		return $logs_ancor_array[$dor][0];
	}

	function map_links($matches) {
		global $links_map;
		$num_links = count($links_map);
		for ($x=0;$x<$num_links;$x++)
			$res .= $links_map[$x].($x==($num_links-1) ? null : $matches[1]);
		return $res;
	}

	function mix_text($matches) {
		global $text_dir;
		$text = cache_file($text_dir."/".$matches[1]);
		if (!isset($matches[2]) or $matches[2]=='\n')
			$a_text = explode ("\n", $text);
		else
			$a_text = explode ($matches[2], $text);
		shuffle($a_text);
		foreach ($a_text as $line)
			$result .= $line.$matches[3];
		return $result;
	}

	function curr_page($matches) {
		global $cur_page_num;
		if ($cur_page_num>0)
			$res = $cur_page_num;
		return $res;
	}

	function dor_url($matches) {
		global $path_remote;
		return $path_remote;
	}

	function dor_host($matches) {
		global $path_remote;
		$url = parse_url($path_remote);
		return $url['host'];
	}

	function mem($matches) {
		global $a_mem_text;
		if (!preg_match('/(?:\[\[)|(?:\]\])|{|}/', $matches[2]))
			$res = $a_mem_text[$matches[1]] = $matches[2];
		else
			$res = '{MEM_'.$matches[1].'}'.$matches[2].'{/MEM}';
		return $res;
	}

	function ins($matches) {
		global $a_mem_text;
		if ($a_mem_text[$matches[1]] != '')
			$res = $a_mem_text[$matches[1]];
		else
			$res = '{INS_'.$matches[1].'}';
		return $res;
	}

	function dor_mem($matches) {
		global $a_dor_mem_text;
		if (!preg_match('/(?:\[\[)|(?:\]\])|{|}/', $matches[2]))
			$res = $a_dor_mem_text[$matches[1]] = $matches[2];
		else
			$res = '{DOR_MEM_'.$matches[1].'}'.$matches[2].'{/DOR_MEM}';
		return $res;
	}

	function dor_ins($matches) {
		global $a_dor_mem_text;
		if ($a_dor_mem_text[$matches[1]] != '')
			$res = $a_dor_mem_text[$matches[1]];
		else
			$res = '{DOR_INS_'.$matches[1].'}';
		return $res;
	}

	function counter($matches) { // {CNT_(.*)_(\d*)_(\d*)}(.*){\/CNT}
		global $a_counter_text;
		if ($a_counter_text[$matches[1]] == '') {
			$sign_num = $a_counter_text[$matches[1]] = $matches[2];
		}
		else {
			$sign_num = $a_counter_text[$matches[1]] = $a_counter_text[$matches[1]] + $matches[3];
		}
		$res = preg_replace('/{CNT_NUM}/', $sign_num, $matches[4]);

		return $res;
	}

	//Конец описания макросов
	//-----------------------


	function cache_file($file) { //кэширует содержимое файла $file, можно использовать различные файл -> многомерный массив
		global $data_cache_file;
		$out = $data_cache_file[$file];
		if ($out == "")
			$out = $data_cache_file[$file] = @file_get_contents($file);
		return $out;
	}

	function massTrim($keys) { //массовый тримминг \n и \s
		$tempKeys = array();
		foreach ($keys as $val) {
			if (!empty($val))
				$tempKeys[] = trim($val);
		}
		return $tempKeys;
	}

	function create_sitemap_xml($path_local) {
		global $dor_keys, $path_remote, $a_key_filename, $dor_num_pages;
		$timestamp = time();
		$step = 8035200 / $dor_num_pages; // 3 месяца
		foreach ($dor_keys as $val) {
			$timestamp -= $step;
			$val = $a_key_filename[$val];
			$out .= "	<url>\n";
			$out .= "		<loc>".$path_remote."/".$val."</loc>\n";
			$out .= "		<lastmod>".date("Y-m-d", $timestamp)."</lastmod>\n";
			$out .= "		<changefreq>weekly</changefreq>\n";
			$out .= "		<priority>0.5</priority>\n";
			$out .= "	</url>\n";
		}
		$out = "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n".$out;
		$out = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n".$out;
		$out = $out."</urlset>";
		$out = iconv("CP1251", "UTF-8", $out);
		file_put_contents($path_local."sitemap.xml", $out);
	}

	function create_robots_txt($path_local) {
		global $path_remote, $generate_sitemap_xml;
		$sm = "User-agent: *\n";
		if ($generate_sitemap_xml)
			$sm .= "Sitemap: ".$path_remote."/sitemap.xml";
		file_put_contents($path_local."robots.txt", $sm);
	}

	function get_perc_array($arr, $perc = 50, $mod = 0) { // $arr - массив исходных значений, $perc - процент необходимого, $mod=0 - вывод массива, $mod=1 - вывод строки через \n
		$total = count($arr);
		$y = $total/($total-($total * $perc)+0.0000000001);
		$y2 = 0.0000000001;
		for ($x=0;$x<$total;$x++) {
			if ($x<$y2)
				if (!$mod)
					$b[] = $arr[$x];
				else
					$b .= $arr[$x]."\n";
			else
				$y2 += $y;
		}
		return $b;
	}
	
	function str_to_bool($text) { // используется при чтении xml данных (стандартно тип - object)
	settype($text, "string");
	if ($text == "TRUE")
		$result = TRUE;
	else
		$result = FALSE;
	return $result;
	}

	function get_all_files_in_dir($src) {
		$dir = opendir($src);
		while(false !== ($file = readdir($dir))) {
			if (($file != ".") and ($file != "..")) {
				if (is_dir($src."/".$file))
					$file_structure = array_merge((array)$file_structure, get_all_files_in_dir($src."/".$file));
				else {
					if (preg_match('/^t_/', $file))
						$file_structure[] = $src."/".$file;
				}
			}
		}
		closedir($dir);
		return (array)$file_structure;
	}
	
	function key_to_filename($key, $enable_extension = FALSE) {
		global $extension;
		$a_bad_sym_search = array  ("/;/", "/:/", "/,/", "/\./", "/\"/", "/'/", "/\n/", "/\t/", "/\:/", "/\|/", "/\//", "/\\\/", "/\*/", "/\"/", "/№/", "/\?/", "/=/", "/\+/", "/&amp;/", "/&lt;/", "/</", "/&gt;/", "/>/", "/&/", "/\s+/", "/а/i", "/б/i", "/в/i", "/г/i", "/д/i", "/е/i", "/ё/i", "/ж/i", "/з/i", "/и/i", "/й/i", "/к/i", "/л/i", "/м/i", "/н/i", "/о/i", "/п/i", "/р/i", "/с/i", "/т/i", "/у/i", "/ф/i", "/х/i", "/ц/i", "/ч/i", "/ш/i", "/щ/i", "/ъ/i", "/ы/i", "/ь/i", "/э/i", "/ю/i", "/я/i", "/^-*/", "/-*$/"); //для имени файла, что ищем
		$a_bad_sym_replace = array ("",    "",    "",    "-",    "",     "",    "",     "",     "",     "",     "",     "",      "",     "",     "",    "",     " ",   " ",    " ",       "",       "",    "",       "",    " ",   "-",     "a",    "b",    "v",    "g",    "d",    "e",    "yo",   "zh",   "z",    "i",    "y",    "k",    "l",    "m",    "n",    "o",    "p",    "r",    "s",    "t",    "u",    "f",    "h",    "c",    "ch",   "sh",   "sh",   "",     "y",    "",     "e",    "yu",   "ya",   "",      ""); //для имени файла, чем заменяем
		$filename = trim(preg_replace($a_bad_sym_search, $a_bad_sym_replace, $key)).($enable_extension ? $extension : null); //превращаем регуляркой все "плохие" символы в нормальные с точки зрения файловой системы
		return $filename;
	}
	
	function array_rand_values($arr, $count_values) {
		if (($count_values > sizeof($arr)) or ($count_values == 0))
			$count_values = sizeof($arr);
		$a_rand_values = array_rand($arr, $count_values);
		foreach ($a_rand_values as $val)
			$res[] = $arr[$val];
		return $res;
	}

	function recurse_copy($src, $dst) {
		$dir = opendir($src);
		@mkdir($dst);
		while(false !== ($file = readdir($dir))) {
			if (($file != ".") and ($file != "..")) {
				if (is_dir($src."/".$file))
					recurse_copy($src."/".$file, $dst."/".$file);
				else {
					if ((!preg_match('/^t_.*/', $file)) and ($file != "index.html") and ($file != "page.txt") and ($file != "dp_sitemap.html") and ($file != "custom_macros.php"))
						copy($src."/".$file, $dst."/".$file);
				}
			}
		}
		closedir($dir);
	}
	
	function create_extract_php($out_dir, $job_name, $zip_filename) {
		$extract_filename = $job_name."_extract.php";
		$pclzip_lib = file_get_contents("lib/pclzip.lib.php");
		$extr = '<?
		set_time_limit(0);
		ini_set("max_execution_time", 0);
		ini_set("memory_limit", "1024M");
		chmod('.$zip_filename.', 0755);
		$zip = new PclZip("'.$zip_filename.'");
		if ($zip->extract(""))
			echo "Успех<br>";
		else
			echo "<u>Неудача</u><br>";
		@unlink("'.$zip_filename.'");
		@unlink("'.$extract_filename.'");
		?>
		'.$pclzip_lib;
		file_put_contents($out_dir."/".$extract_filename, $extr);
		return $extract_filename;
	}
	
	function array_unique_own($array) {
		foreach ($array as $val)
			$array_fn[$val] = key_to_filename($val);
		$array_fn = array_unique($array_fn);
		return array_keys($array_fn);
	}

	function compression_text($text) {
		$srs_literal = array ("/\n/", "/\r/", "/\t/", "/\s{2,}/");
		$repl_text = array ("", "", "", " ");
		$text = preg_replace($srs_literal, $repl_text, $text);
		return $text;
	}
	
	function del_comment_job_list($job_list) {
		for ($x=0; $x<count($job_list); $x++) {
			$job_list[$x] = preg_replace('/\s*\/\*.*/i', '',$job_list[$x]);
			if (trim($job_list[$x]) != '')
				$res[] = $job_list[$x];
		}
		return $res;
	}

	function aggress($s) {
	    // меняем макросы агресса на андрюхи
		$s = str_replace("{STAT}{ARANDKEYWORD}{/STAT}", "{BBMKEYWORD}", $s);
		$s = str_replace("{BOSKEYWORD}", "{BKEYWORD}", $s);
		$s = str_replace("{ABOSKEYWORD}", "{BBKEYWORD}", $s);
		$s = str_replace("{CBOSKEYWORD}", "{BKEYWORD}", $s);
		$s = str_replace("{RANDKEYWORD}", "{RAND_KEY}", $s);
		$s = str_replace("{ARANDKEYWORD}", "{BBRAND_KEY}", $s);
		$s = str_replace("{CRANDKEYWORD}", "{BRAND_KEY}", $s);
		$s = str_replace("{RANDLINKURL}", "{RAND_URL}", $s);
		$s = str_replace("{RANDLINK}", "{RAND_ANCOR}", $s);
		$s = str_replace("{ARANDLINK}", "{BBRAND_ANCOR}", $s);
		$s = str_replace("{CRANDLINK}", "{BRAND_ANCOR}", $s);
		$s = str_replace("{RANDMYLINK}", "{RANDTEXTLINE(netlinks.txt)}", $s);
		$s = str_replace("{INDEXLINK}", "{INDEX}", $s);
		$s = str_replace("{SITEMAPLINK}", "{MAPS_ }", $s);
		$s = str_replace("{ALLLINK}", "{MAP_LINKS_ }", $s);
		$s = str_replace("{I}", "{FOR_NUM}", $s);
		return $s;
	}

    function add_page_key($s) {
        $randkey = "RAND_KEY}";
        $keyword = "KEYWORD}";
        // сколько раз встречается рандомный кей
        $n = substr_count($s, $randkey);
        // сколько раз будем менять
        $m = min(mt_rand(3, 5), $n);
        for ($i = 0; $i < $m; $i++) {
            // какое вхождение меняем
            $p = mt_rand(1, $n);
            $offset = -1;
            for ($j = 0; $j < $p; $j++)
                $offset = strpos($s, $randkey, $offset + 1);
            // нашли, меняем
            $s = substr_replace($s, $keyword, $offset, strlen($randkey));
            $n -= 1;
        }
        return $s;
    }

?>