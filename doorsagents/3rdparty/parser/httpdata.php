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
    /*if($this->proxy!=0){
      curl_setopt($ch, CURLOPT_PROXY, $this->proxy);
      curl_setopt($ch, CURLOPT_PROXYTYPE, CURLPROXY_SOCKS5);
      echo $this->proxy;
    }*/    
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
    $_a[] = "Opera/10.00 (Windows NT 5.1; U; ru) Presto/2.2.0";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; OfficeLiveConnector.1.3; OfficeLivePatch.0.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618)";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 1.1.4322; InfoPath.1)";
    $_a[] = "Opera/9.62 (Windows NT 5.1; U; ru) Presto/2.1.1";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; MRSPUTNIK 2, 0, 1, 31 SW; MRA 5.2 (build 02415); .NET CLR 1.1.4322; InfoPath.2; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)";
    $_a[] = "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 1.1.4322)";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; (R1 1.5); .NET CLR 1.1.4322)";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; FunWebProducts; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)";
    $_a[] = "Mozilla/5.0 (Windows; U; Windows NT 5.1; pl; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0)";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1)";
    $_a[] = "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11";
    $_a[] = "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.8.0.6) Gecko/20060728 Firefox/1.5.0.6";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)";
    $_a[] = "Opera/9.25 (Windows NT 5.1; U; pl)";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; AT&amp;T CSM6.0; .NET CLR 1.1.4322)";
    $_a[] = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FDM)";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; InfoPath.2)";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727)";
    $_a[] = "Opera/9.20 (Windows NT 5.1; U; ru)";
    $_a[] = "Opera/9.23 (Windows NT 5.1; U; ru)";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FileDownloader; .NET CLR 1.0.3705; .NET CLR 1.1.4322; InfoPath.1; FileDownloader; Media Center PC 4.0; .NET CLR 2.0.50727; MEGAUPLOAD 2.0)";
    $_a[] = "Opera/9.21 (Windows NT 5.0; U; ru)";
    $_a[] = "Opera/9.25 (Windows NT 5.1; U; bg)";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; PeoplePal 3.0)";
    $_a[] = "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1); afcid=Wadf57d6951da76af4c6f0b08181c298d";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; MEGAUPLOAD 2.0)";
    $_a[] = "Opera/8.54 (Windows NT 5.1; U; ru)";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; YComp 5.0.0.0; .NET CLR 1.0.3705; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648)SAMSUNG-SGH-P910/1.0 SHP/VPP/R5 NetFront/3.3 SMM-MMS/1.2.0 profile/MIDP-2.0 configuration/CLDC-1.1";
    $_a[] = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; ADVPLUGIN|K115|165|S548873517|dial; 666XXX040507; .NET CLR 2.0.50727)";

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
