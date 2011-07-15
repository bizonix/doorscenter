<?php
	require ("permissions.php");
	echo "<table border=\"1\">\n";
	echo "<tr><td colspan=\"7\"><b>Табл 3. Где выполняются макросы</b></td></tr>\n";
	echo "<tr><td>Имя макроса</td><td>index.txt</td><td>page.txt</td><td>map.txt</td><td>t_*.*</td><td>jobs/*.txt</td><td>Текст анкора на sitemap'ы</td></tr>\n";
	for ($i=0;$i<count($access_macros_jobs);$i++)
		echo "<tr><td>".$macros_name[$i]."</td><td>".($access_macros_index[$i] ? "+" : null)."</td><td>".($access_macros_page[$i] ? "+" : null)."</td><td>".($access_macros_sitemap[$i] ? "+" : null)."</td><td>".($access_macros_custom_page[$i] ? "+" : null)."</td><td>".($access_macros_jobs[$i] ? "+" : null)."</td><td>".($access_macros_text_ancor_sitemap_links[$i] ? "+" : null)."</td></tr>\n";

	echo "<tr><td>NUM_SITEMAP</td><td></td><td></td><td>+</td><td></td><td></td><td></td></tr>\n";
	echo "<tr><td>DOR</td><td></td><td></td><td></td><td></td><td>+</td><td></td></tr>\n";
	echo "</table>\n";
