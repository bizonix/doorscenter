<?php
	/*------------------------
	Синтаксис описания макросов:
	'{ВАШ_МАКРОС}' => 'строка, на которую заменится ваш макрос, может содержать любые встроенные макросы, в том числе и пользовательские'
	далее, если это не последний макрос, то ставим вконце запятую, если последний, то ничего не ставим.
	В целом, это обычное объявление массива в PHP
	------------------------*/
	$custom_macros = array(
	//также можно макросы комментировать
	'{IMG}' => '<img src="images/img{URAND_500_1000}.jpg" alt="{BRAND_KEY}">',
	//а можно и не комментировать
	'{ALL_MACROS}' => '<blockquote>
	В пользовательских макросах обрабатываются все остальные макросы, пример:<br>
	&#123;MKEYWORD&#125;: {MKEYWORD}<br>
	&#123;BMKEYWORD&#125;: {BMKEYWORD}<br>
	&#123;KEYWORD&#125;: {KEYWORD}<br>
	&#123;BKEYWORD&#125;: {BKEYWORD}<br>
	&#123;MAPS_, &#125;: {MAPS_, }<br>
	&#123;INDEX&#125;: {INDEX}<br>
	&#123;DOR_URAND_1_20&#125;: {DOR_URAND_500_1000}<br>
	&#123;DOR_RAND_1_20&#125;: {DOR_RAND_0_20}<br>
	&#123;RAND_KEY&#125;: {RAND_KEY}<br>
	&#123;BRAND_KEY&#125;: {BRAND_KEY}<br>
	&#123;RAND_URL&#125;: {RAND_URL}<br>
	&#123;RAND_ANCOR&#125;: {RAND_ANCOR}<br>
	&#123;BRAND_ANCOR&#125;: {BRAND_ANCOR}<br>
	&#123;RAND_TEXT_123.txt&#125;: {RAND_TEXT_123.txt}<br>
	&#123;LINKS_2_5_<br>&#125;: {LINKS_2_5_<br>}<br>
	&#123;RELINKS_2_5_<br>&#125;: {RELINKS_2_5_<br>}<br>
	&#123;MAP_LINKS_<br>&#125;: {MAP_LINKS_<br>}<br>
	&#91;&#91;qwe|rty|uio&#93;&#93;: [[qwe|rty|uio]]<br>
	&#123;DOR_TEXT_counter.txt&#125;: {DOR_TEXT_counter.txt}<br>
	&#123;LINE_FILE_15_123.txt&#125;: {LINE_FILE_15_123.txt}
	</blockquote>'
	);
?>