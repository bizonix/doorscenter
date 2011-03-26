<?php

class httpdata
{	
	var $proxy; //Прокси в формате ip:port
	var $headers;
	
	
	
	/* хуйнягенератор */
	function Generate($max)
	{
		$abc = array("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z");
		$data = "";
		for($i=0;$i<$max;$i++)
		{
			$data .= $abc(array_rand($abc));
		}
		
		$data .= rand(100, 1000);
		return $data;
	}
	
	/* GET Запрос */
	function GetData($ch, $url, $referer = "")
	{
		if(isset($url)){
			curl_setopt($ch, CURLOPT_URL, $url);
			$res = curl_exec($ch);
			return $res;
		}
		else{
			return "Enter URL\r\n";
		}
	}
	
	/* POST Запрос */
	function PostData($ch, $url, $data, $referer = "")
	{
		if(isset($url) && isset($data)){
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_POST, 1);
		curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
		$res = curl_exec($ch);
		return $res;
		}
		
	}
	/* Инициализация cUrl */
	function CurlInit()
	{
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_HEADER, 0);
		curl_setopt($ch, CURLOPT_USERAGENT, $this->getUserAgent());		
		/*if($referer!=""){
		curl_setopt($ch, CURLOPT_REFERER, $referer);
		}*/
		if($this->Proxy!=0){
		curl_setopt($ch, CURLOPT_PROXY, $this->Proxy);  
		}		
		curl_setopt($ch, CURLOPT_COOKIE, 0);
		
		return $ch;
	}
	
	
	function CurlClose($ch)
	{
		curl_close($ch);
	}
	
	/* $string - что искать, $data - где искать */
	function CheckData($string, $data)
	{
		if(eregi($string, $data)){
			return TRUE;
		}
		else{
			return FALSE;
		}
	}
	/* UserAgent генератор */
	function getUserAgent()
	{

		$_a[] = "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4 WebMoney Advisor";
		$_a[] = "Mozilla/6.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4 WebMoney Advisor";
		$_a[] = "Mozilla/7.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4 WebMoney Advisor";
		$_a[] = "Opera/10.00 (Windows NT 5.1; U; ru) Presto/2.2.0";
		$_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618)";
		$_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 1.1.4322; InfoPath.1)";
		$_a[] = "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7";
		$_a[] = "Opera/9.63 (Windows NT 5.1; U; ru) Presto/2.1.1";
		$_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2)";
		$_a[] = "Opera/9.62 (Windows NT 5.1; U; ru) Presto/2.1.1";
		$_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; MRSPUTNIK 2, 0, 1, 31 SW; MRA 5.2 (build 02415); .NET CLR 1.1.4322; InfoPath.2; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)";
		$_a[] = "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7";

		return $_a[array_rand($_a)];
	
	}
	
	function setProxy($proxy)
	{
		if ($proxy)
			$this->proxy = $proxy;
		else
			unset($this->proxy);
	}
	
}
			


?>