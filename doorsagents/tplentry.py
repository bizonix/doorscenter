# coding: utf-8
'''Составные части шаблона'''

strDivider = r'''---
'''

strIndex = r'''<html>
  <head>
    <title>{ABOSKEYWORD} - {STAT}{ARANDKEYWORD}{/STAT}</title>
      <meta http-equiv="Content-Type" content="text/html; charset=windows-1250">
      <meta name="description" content="{CBOSKEYWORD}. {CRANDKEYWORD}. {CRANDKEYWORD}. {CRANDKEYWORD}. {CRANDKEYWORD}. {CRANDKEYWORD}" >
      <meta name="keywords" content="{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD}">
      <style>
      <!--//
      * {margin:0;padding:0}
      body {
        background:url("/images/back/{{numBackground}}.jpg");
        color:{{rndColor1}};
        margin:0;
        padding:0;
        text-align:center;
      }
      div#wrapper {
        background:{{rndColor2}};
        width:1000px;
        margin:0 auto 0 auto;
        text-align:center;
      }
      img {
        margin:5px;
        border:none;
      }
      .headimg {
        margin:0;
      }
      .tabla {
        text-align:center;
      }
      a, a:hover, a:visited, a:active {
        color:{{rndColor3}};
      }
      //-->
      </style>
      <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js"></script>
  </head>
  <body>
    <div id="wrapper">
      <h1>{ABOSKEYWORD}</h1>
      <?php include("/var/www/common/bidtraffic.php"); ad('{BOSKEYWORD}'); ?>
      {{strEntries}}
      <br/>{FOR(1,{RAND(5,15)})}{CRANDLINK} {ENDFOR} {FOR(1,{RAND(1,3)})}{RANDMYLINK} {ENDFOR}<br/>
      <div id="footer">
        &copy 2011 {STAT}{ARANDKEYWORD}{/STAT}. All rights reserved. {INDEXLINK} {SITEMAPLINK}.
      </div>
    </div>
{PIWIK}
  </body>
</html>
'''

strSitemap = r'''<html>
  <head>
    <title>{ARANDKEYWORD}</title>
      <meta http-equiv="Content-Type" content="text/html; charset=windows-1250">
      <meta name="description" content="{CRANDKEYWORD}. {CRANDKEYWORD}. {CRANDKEYWORD}. {CRANDKEYWORD}. {CRANDKEYWORD}" >
      <meta name="keywords" content="{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD}">
      <style>
      <!--//
      * {margin:0;padding:0}
      body {
        background:url("/images/back/{{numBackground}}.jpg");
        color:{{rndColor1}};
        margin:0;
        padding:0;
        text-align:center;
      }
      div#wrapper {
        background:{{rndColor2}};
        width:1000px;
        margin:0 auto 0 auto;
        text-align:center;
      }
      img {
        margin:5px;
        border:none;
      }
      .headimg {
        margin:0;
      }
      .tabla {
        text-align:center;
      }
      a, a:hover, a:visited, a:active {
        color:{{rndColor3}};
      }
      //-->
      </style>
  </head>
  <body>
    <div id="wrapper">
      <h1>Sitemap</h1>
      {{strEntries}}
      <br/><?php include("/var/www/common/script/banner-xgen-{{tplKind}}.txt"); ?><br/>
      {INDEXLINK}<a href="sitemap.xml">sitemap</a>{ALLLINK}
      <br/><?php include("/var/www/common/script/banner-xgen-{{tplKind}}.txt"); ?><br/>
      <div id="footer">
        &copy 2011. All rights reserved. <a href="index.html">{RANDKEYWORD}</a>.
      </div>
    </div>
  </body>
{PIWIK}
</html>
'''

strEntries = r'''<br/><br/><img src="{{imgPath}}/img/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /><br/><br/>
---
<br/>{FOR(1,{RAND(4,6)})}{RANDKEYWORD}[[||||||.]] {ENDFOR}{RANDKEYWORD}.<br/>
---
<br/>{FOR(1,{RAND(2,5)})}{RANDTEXTLINE(bred-en.txt)}<br/>{ENDFOR}<br/>
---
<br/><?php include("/var/www/common/script/banner-xgen-{{tplKind}}.txt"); ?><br/>
---
<br/><?php include("/var/www/common/script/banner-xgen-{{tplKind}}.txt"); ?><br/>
---
<br/><?php include("/var/www/common/script/banner-xgen-{{tplKind}}.txt"); ?><br/>
---
<table cellspacing="10px" align="center" class="tabla">{{strTableEntries}}</table>
---
<table cellspacing="10px" align="center" class="tabla">{{strTableEntries}}</table>
---
<table cellspacing="10px" align="center" class="tabla">{{strTableEntries}}</table>
---
<table cellspacing="10px" align="center" class="tabla">{{strTableEntries}}</table>
---
<table cellspacing="10px" align="center" class="tabla">{{strTableEntries}}</table>
'''

strTableEntries = r'''<tr>{FOR(1,6)}<td><a href="http://searchpro.ws/go2.php?sid={{tdsSchema}}"><img src="{{imgPath}}/thumb/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></a></td>{ENDFOR}</tr>
<tr>{FOR(1,6)}<td>{RANDKEYWORD}, {RANDKEYWORD}, {RANDKEYWORD}, {RANDKEYWORD}.</td>{ENDFOR}</tr>
---
<tr>{FOR(1,2)}<td><a href="http://searchpro.ws/go2.php?sid={{tdsSchema}}"><img src="{{imgPath}}/thumb/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></a></td><td>{RANDKEYWORD} {RANDKEYWORD} {RANDKEYWORD} {RANDKEYWORD}</td>{ENDFOR}</tr>
<tr>{FOR(1,2)}<td><a href="http://searchpro.ws/go2.php?sid={{tdsSchema}}"><img src="{{imgPath}}/thumb/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></a></td><td>{RANDKEYWORD} {RANDKEYWORD} {RANDKEYWORD} {RANDKEYWORD}</td>{ENDFOR}</tr>
---
<tr>{FOR(1,2)}<td><a href="http://searchpro.ws/go2.php?sid={{tdsSchema}}"><img src="{{imgPath}}/imgm/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></a></td>{ENDFOR}</tr>
---
<tr>{FOR(1,2)}<td><a href="http://searchpro.ws/go2.php?sid={{tdsSchema}}"><img src="{{imgPath}}/imgm/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></a></td>{ENDFOR}</tr>
<tr>{FOR(1,2)}<td>{RANDKEYWORD}</td>{ENDFOR}</tr>
---
<tr>{FOR(1,2)}<td><a href="http://searchpro.ws/go2.php?sid={{tdsSchema}}"><img src="{{imgPath}}/imgm/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></a></td>{ENDFOR}</tr>
<tr>{FOR(1,2)}<td>{RANDKEYWORD}</td>{ENDFOR}</tr>
<tr>{FOR(1,2)}<td><a href="http://searchpro.ws/go2.php?sid={{tdsSchema}}"><img src="{{imgPath}}/imgm/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></a></td>{ENDFOR}</tr>
<tr>{FOR(1,2)}<td>{RANDKEYWORD}</td>{ENDFOR}</tr>
---
<tr>
  <td width="50%">
    <table cellspacing="10px" align="center" class="tabla">
      <tr>{FOR(1,2)}<td><a href="http://searchpro.ws/go2.php?sid={{tdsSchema}}"><img src="{{imgPath}}/thumb/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></a></td>{ENDFOR}</tr>
      <tr>{FOR(1,2)}<td>{RANDKEYWORD}</td>{ENDFOR}</tr>
      <tr>{FOR(1,2)}<td><a href="http://searchpro.ws/go2.php?sid={{tdsSchema}}"><img src="{{imgPath}}/thumb/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></a></td>{ENDFOR}</tr>
      <tr>{FOR(1,2)}<td>{RANDKEYWORD}</td>{ENDFOR}</tr>
    </table>
  </td>
  <td><a href="http://searchpro.ws/go2.php?sid={{tdsSchema}}"><img src="{{imgPath}}/imgm/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></a></td>
</tr>
'''

strHtAccess = r'''RemoveHandler .html
AddType application/x-httpd-php .php .html
'''

strCmd = r'''<?php
umask(0);
symlink('/var/www/common/images', 'images');
system('tar -zxf bean.tgz');
unlink('bean.tgz');
?>
'''
strRobots = r'''User-Agent: *
Allow: /
Disallow: /script
'''
