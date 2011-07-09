<?php

AddDomain($_POST['domainName'], $_POST['controlPanelUrl']);

function AddDomain($domainName, $controlPanelUrl) {
	$client_id = 0;
	$params['server_id'] = 1;
	$params['ip_address'] = '*';
	$params['type'] = 'vhost'; //Site / Alias
	$params['parent_domain_id']="";
	$params['vhost_type'] = 'name'; //Namebased / IP-Based
	$params['hd_quota'] = '-1';
	$params['cgi'] = 'n'; //n // y
	$params['ssi'] = 'n';//n / y
	$params['suexec'] = 'n'; //n / y
	$params['errordocs'] = 0; //0 / 1
	$params['subdomain'] = 'www'; //none / www. / *.
	$params['ssl'] = 'n'; //n / y
	$params['php'] = 'mod'; //Disabled, Fast-CGI, CGI, Mod-PHP, SuPHP
	$params['active'] = 'y'; //n / y
	$params['redirect_type'] = ''; //array('' => 'No redirect', 'no' => 'No flag', 'R' => 'R', 'L' => 'L', 'R,L' => 'R,L')
	$params['redirect_path'] = '';
	$params['ssl_action'] = '';
	$params['traffic_quota'] = '-1';
	$params['document_root'] = '/home/admin';
	$params['system_user'] = '1';
	$params['system_group'] = '1';
	$params['allow_override'] = 'All';
	$params['php_open_basedir'] = '/home/admin';
	$params['stats_type'] = 'webalizer';
	$params['backup_copies'] = 1;
	$params['backup_interval'] = 'none';
	$params['sys_perm_user'] = 'riud';
	$params['sys_perm_group'] = 'ru';
	
	$soap_location = $controlPanelUrl . '/remote/index.php';
	$soap_uri = $controlPanelUrl . '/remote/';
	$username = 'admin';
	$password = '7hcX54s4';
	$client = new SoapClient(null, array('location' => $soap_location, 'uri' => $soap_uri));
	try {
		$session_id = $client->login($username,$password);
		$params['domain'] = $domainName;
		$website_id = $client->sites_web_domain_add($session_id, $client_id, $params);
		$client->logout($session_id);
		echo('ok');
	}
	catch (SoapFault $e) {
		die('Error: '.$e->getMessage());
	}
}
?>
