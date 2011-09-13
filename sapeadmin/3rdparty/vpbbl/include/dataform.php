<?
//чистим временную папку
	remove_dir('../out',true);
	//запускаем морфологию
	require_once('common.php');
	// запускаем библиотеку
	$morphy =& new phpMorphy(
		new phpMorphy_FilesBundle()
	);

//делаем цикл по числу текста
$tt=0;
	foreach ($outcontent as $key=>$line){
	echo 'Готовим данные №: [<b>'.($key+1).'</b>]'. "</b><br>\r\n";
	    echo '<script language="JavaScript">scrl(30)</script>';
		flush();
	//обрабатываем каждую страницу:
	//обрезаем по длине
	$outtitle[$key]=str_replace("ЂЂЂ","",strip_tags($outtitle[$key]));
	$outcontent[$key]=str_replace("ЂЂЂ","",substr($outcontent[$key],0,$config['maxlen']));
	$array[$tt]['title']=$outtitle[$key];
	$textos=obtext($outcontent[$key],$outtitle[$key],$tt);
	$array[$tt]['text']=$textos;
	 		//формируем ключевые слова
	$array[$tt]['keywords2']=keywords($outcontent[$key]);
	$array[$tt]['keywords']=join(", ",$array[$tt]['keywords2']);
	if((count($array[$tt]['keywords'])>0)){
				//формируем дескрипшн
		$array[$tt]['description']=description($outcontent[$key]);
		 		//формируем облако слов
		$array[$tt]['oblako']=$array[$tt]['keywords2'];
		 		//формируем псевдо дату
		$array[$tt]['time']=time()-(count($outcontent)-$tt)*rand(70,100)*1000+rand(0,999);
		 		//формируем новостную рецензию
		$array[$tt]['news']=news($outcontent[$key]);
		 		//формируем короткое название

		  		$word=@checkword($array[$tt]['keywords2'],$wordas,$key);
				$wordas[]=$word;
				if($_GET['mymenu']!="true"){
		$array[$tt]['smalltitle']=$word;
		}else{
		if($tt<5){		$array[$tt]['smalltitle']=$_GET['word'.($tt+1)];		}else{		$array[$tt]['smalltitle']=$word;
		}		}
				//формируем короткое имя
		 		if($tt===0){
		$array[$tt]['name']="index";
		 			}else{
		 			switch ($_GET['names']) {
        case "own":
        $array[$tt]['name']=translit($array[$tt]['smalltitle']);

          break;
        case "title":
        $array[$tt]['name']=translit($array[$tt]['title']);
          break;
        case "num":
        $array[$tt]['name']=$tt;
          break;
        case "rand":
        $array[$tt]['name']=rand(0,9999999);
          break;
         case "randrazdel":
        $array[$tt]['name']=$config['razdel'][rand(0,(count($config['razdel'])-1))]."-".rand(0,9999);
          break;
      }
		}

		$tt++;
	}
	}
 echo 'Подготовили данные для формирования страницю'. "<br>\r\n";
		    echo '<script language="JavaScript">scrl(30)</script>';
	flush();


?>