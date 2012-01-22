<?php

if (isset($_POST['domainName']))
  DelDomain($_POST['domainName'], $_POST['controlPanelUrl']);
//DelDomain('test-xxx.com', 'http://searchpro.name:15671');

function DelDomain($domainName, $controlPanelUrl) {
	$con = mysql_connect('localhost', 'root', 'yo2k21iO');
	mysql_select_db('dbispconfig', $con);
	// get domain id
	$sql = 'select domain_id from web_domain where domain="' . $domainName . '"';
	$result = mysql_query($sql);
	$row = mysql_fetch_array($result);
	$domainId = $row[0];
	// get zone id
	$sql = 'select id from dns_soa where origin="' . $domainName . '."';
	$result = mysql_query($sql);
	$row = mysql_fetch_array($result);
	$zoneId = $row[0];
	
	if ($domainId || $zoneId) {
		// the action
		$soap_location = $controlPanelUrl . '/remote/index.php';
		$soap_uri = $controlPanelUrl . '/remote/';
		$username = 'admin';
		$password = '7hcX54s4';
		$client = new SoapClient(null, array('location' => $soap_location, 'uri' => $soap_uri));
		try {
			$session_id = $client->login($username, $password);
			// delete website
			$website_id = $client->sites_web_domain_delete($session_id, $domainId);
			// delete dns zone
			$website_id = $client->dns_zone_delete($session_id, $zoneId);
			// delete dns records
			$sql = 'select id, type from dns_rr where zone=' . $zoneId;
			$result = mysql_query($sql);
			while ($row = mysql_fetch_array($result)) {
				if ($row[1] == 'A')
					$client->dns_a_delete($session_id, $row[0]);
				if ($row[1] == 'MX')
					$client->dns_mx_delete($session_id, $row[0]);
				if ($row[1] == 'NS')
					$client->dns_ns_delete($session_id, $row[0]);
			}
			$client->logout($session_id);
			echo('ok');
		}
		catch (SoapFault $e) {
			echo('Error: ' . $e->getMessage());
		}
	}
	else
		echo('domain not found');
	mysql_close($con);
}

?>
