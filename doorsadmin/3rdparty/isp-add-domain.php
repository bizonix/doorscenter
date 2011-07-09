<?php

AddDomain($_POST['domainName'], $_POST['ipAddress'], $_POST['useDNS'], $_POST['controlPanelUrl'], $_POST['controlPanelServerId']);
//AddDomain('test-xxx.com', '1.1.1.1', true, 'http://searchpro.name:15671', 2);

function AddDomain($domainName, $ipAddress, $useDNS, $controlPanelUrl, $controlPanelServerId) {
	// common params
	$client_id = 0;
	$ns1_name = 'ns1.ralenc.net';
	$ns2_name = 'ns2.ralenc.net';
	$ns1_ip_address = '178.79.184.225';
	//$ns2_ip_address = '';
	$ns1_server_id = 2;
	$ns2_server_id = 3;
	
	// domain params
	$params['server_id'] = $controlPanelServerId;
	$params['ip_address'] = '*';
	$params['domain'] = $domainName;
	$params['type'] = 'vhost';
	$params['parent_domain_id'] = 0;
	$params['vhost_type'] = 'name';
	$params['hd_quota'] = -1;
	$params['traffic_quota'] = -1;
	$params['cgi'] = 'n';
	$params['ssi'] = 'n';
	$params['suexec'] = 'n';
	$params['errordocs'] = 0;
	$params['subdomain'] = 'www';
	$params['php'] = 'mod';
	$params['ruby'] = 'n';
	$params['redirect_type'] = '';
	$params['redirect_path'] = '';
	$params['ssl'] = 'n';
	$params['ssl_action'] = '';
	$params['active'] = 'y';
	$params['system_user'] = '1';
	$params['system_group'] = '1';
	$params['allow_override'] = 'All';
	$params['document_root'] = '/home/admin';
	$params['php_open_basedir'] = '/home/admin';
	$params['stats_type'] = 'webalizer';
	$params['backup_copies'] = 1;
	$params['backup_interval'] = 'none';
	$params['sys_perm_user'] = 'riud';
	$params['sys_perm_group'] = 'ru';
	
	// primary dns params
	$params1['server_id'] = $ns1_server_id;
	$params1['origin'] = $domainName . '.';
	$params1['ns'] = $ns1_name . '.';
	$params1['mbox'] = 'admin.' . $domainName . '.';
	$params1['serial'] = date('Ymd') . '01';
	$params1['refresh'] = 28800;
	$params1['retry'] = 7200;
	$params1['expire'] = 604800;
	$params1['minimum'] = 86400;
	$params1['ttl'] = 86400;
	$params1['active'] = 'Y';
	$params1['xfer'] = '';
	$params1['also_notify'] = '';
	$params1['update_acl'] = '';
	$params1['sys_perm_user'] = 'riud';
	$params1['sys_perm_group'] = 'riud';
	
	// dns records params
	$params2['server_id'] = $ns1_server_id;
	$params2['ttl'] = 86400;
	$params2['aux'] = 0;
	$params2['active'] = 'Y';
	$params2['stamp'] = date('Y-m-d H:i:s');
	$params2['serial'] = date('Ymd') . '01';
	$params2['sys_perm_user'] = 'riud';
	$params2['sys_perm_group'] = 'riud';
	
	// slave dns params
	$params3['server_id'] = $ns2_server_id;
	$params3['origin'] = $domainName.'.';
	$params3['ns'] = $ns1_ip_address;
	$params3['active'] = 'Y';
	$params3['xfer'] = '';
	$params3['sys_perm_user'] = 'riud';
	$params3['sys_perm_group'] = 'riud';
	
	// the action
	$soap_location = $controlPanelUrl . '/remote/index.php';
	$soap_uri = $controlPanelUrl . '/remote/';
	$username = 'admin';
	$password = '7hcX54s4';
	$client = new SoapClient(null, array('location' => $soap_location, 'uri' => $soap_uri));
	try {
		// login
		$session_id = $client->login($username,$password);
		// domain
		$website_id = $client->sites_web_domain_add($session_id, $client_id, $params);
		if ($useDNS) {
			// primary dns
			$zone_id = $client->dns_zone_add($session_id, $client_id, $params1);
			// a record
			$params2['zone'] = $zone_id;
			$params2['type'] = 'A';
			$params2['data'] = $ipAddress;
			$params2['name'] = $domainName.'.';
			$client->dns_a_add($session_id, $client_id, $params2);
			$params2['name'] = 'www';
			$client->dns_a_add($session_id, $client_id, $params2);
			$params2['name'] = 'mail';
			$client->dns_a_add($session_id, $client_id, $params2);
			// ns record
			$params2['type'] = 'NS';
			$params2['name'] = $domainName.'.';
			$params2['data'] = $ns1_name.'.';
			$client->dns_ns_add($session_id, $client_id, $params2);
			$params2['data'] = $ns2_name.'.';
			$client->dns_ns_add($session_id, $client_id, $params2);
			// mx record
			$params2['type'] = 'MX';
			$params2['name'] = $domainName.'.';
			$params2['data'] = 'mail.'.$domainName.'.';
			$params2['aux'] = 10;
			$client->dns_mx_add($session_id, $client_id, $params2);
			// slave dns
			$slave_id = $client->dns_zone_slave_add($session_id, $client_id, $params3);
		}
		// logout
		$client->logout($session_id);
		echo('ok');
	}
	catch (SoapFault $e) {
		die('Error: '.$e->getMessage());
	}
}

?>
