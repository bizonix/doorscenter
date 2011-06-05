# coding: utf-8
'''Составные части шаблона'''

strDivider = r'''---
'''

strIndex = r'''<html>
  <head>
    <title>{ABOSKEYWORD} - {STAT}{ARANDKEYWORD}{/STAT}</title>
      <meta name="description" content="{CBOSKEYWORD}. {CRANDKEYWORD}. {CRANDKEYWORD}. {CRANDKEYWORD}. {CRANDKEYWORD}. {CRANDKEYWORD}" >
      <meta name="keywords" content="{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD}">
      <style>
      <!--//
      * {margin:0;padding:0}
      body {
        background:url("{STAT}{RAND(1,5)}.png{/STAT}");
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
      {STAT}<img src="{{imgPath}}/img/{RAND(1,{{imgCount}})}.jpg" alt="{BOSKEYWORD}" class="headimg" />{/STAT}
      <h1>{ABOSKEYWORD}</h1>
      {{strEntries}}
      <br/>{FOR(1,{RAND(5,15)})}{CRANDLINK} {ENDFOR} {FOR(1,{RAND(1,3)})}{RANDMYLINK} {ENDFOR}<br/>
      <div id="footer">
        &copy 2011 {STAT}{ARANDKEYWORD}{/STAT}. All rights reserved. {CYCLIK} {INDEXLINK} {SITEMAPLINK}.
      </div>
    </div>
{PIWIKCOUNTER}
  </body>
</html>
'''

strSitemap = r'''<html>
  <head>
    <title>{ARANDKEYWORD}</title>
      <meta name="description" content="{CRANDKEYWORD}. {CRANDKEYWORD}. {CRANDKEYWORD}. {CRANDKEYWORD}. {CRANDKEYWORD}" >
      <meta name="keywords" content="{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD},{RANDKEYWORD}">
      <style>
      <!--//
      * {margin:0;padding:0}
      body {
        background:url("{STAT}{RAND(1,5)}.png{/STAT}");
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
      <img src="1.jpg" alt="{RANDKEYWORD}" class="headimg" />
      <h1>Sitemap</h1>
      {{strEntries}}
      <br/><!-- bnr --><br/>
      {INDEXLINK}<a href="sitemap.xml">sitemap</a>{ALLLINK}
      <br/><!-- bnr --><br/>
      <div id="footer">
        &copy 2011. All rights reserved. <a href="index.html">{RANDKEYWORD}</a>.
      </div>
    </div>
  </body>
{PIWIKCOUNTER}
</html>
'''

strEntries = r'''<br/><br/><img src="{{imgPath}}/img/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /><br/><br/>
---
<br/>{FOR(1,{RAND(4,6)})}{RANDKEYWORD}{RANDTEXT(15,.)} {ENDFOR}{RANDKEYWORD}.<br/>
---
<br/>{FOR(1,{RAND(2,5)})}{RANDTEXTLINE(C:\Work\text\bred-en.txt)}<br/>{ENDFOR}<br/>
---
<br/><!-- bnr --><br/>
---
<br/><!-- bnr --><br/>
---
<br/><!-- bnr --><br/>
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

strTableEntries = r'''<tr>{FOR(1,6)}<td><img src="{{imgPath}}/thumb/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></td>{ENDFOR}</tr>
<tr>{FOR(1,6)}<td>{RANDKEYWORD}, {RANDKEYWORD}, {RANDKEYWORD}, {RANDKEYWORD}.</td>{ENDFOR}</tr>
---
<tr>{FOR(1,2)}<td><img src="{{imgPath}}/thumb/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></td><td>{RANDKEYWORD} {RANDKEYWORD} {RANDKEYWORD} {RANDKEYWORD}</td>{ENDFOR}</tr>
<tr>{FOR(1,2)}<td><img src="{{imgPath}}/thumb/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></td><td>{RANDKEYWORD} {RANDKEYWORD} {RANDKEYWORD} {RANDKEYWORD}</td>{ENDFOR}</tr>
---
<tr>{FOR(1,2)}<td><img src="{{imgPath}}/imgm/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></td>{ENDFOR}</tr>
---
<tr>{FOR(1,2)}<td><img src="{{imgPath}}/imgm/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></td>{ENDFOR}</tr>
<tr>{FOR(1,2)}<td>{RANDKEYWORD}</td>{ENDFOR}</tr>
---
<tr>{FOR(1,2)}<td><img src="{{imgPath}}/imgm/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></td>{ENDFOR}</tr>
<tr>{FOR(1,2)}<td>{RANDKEYWORD}</td>{ENDFOR}</tr>
<tr>{FOR(1,2)}<td><img src="{{imgPath}}/imgm/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></td>{ENDFOR}</tr>
<tr>{FOR(1,2)}<td>{RANDKEYWORD}</td>{ENDFOR}</tr>
---
<tr>
  <td width="50%">
    <table cellspacing="10px" align="center" class="tabla">
      <tr>{FOR(1,2)}<td><img src="{{imgPath}}/thumb/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></td>{ENDFOR}</tr>
      <tr>{FOR(1,2)}<td>{RANDKEYWORD}</td>{ENDFOR}</tr>
      <tr>{FOR(1,2)}<td><img src="{{imgPath}}/thumb/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></td>{ENDFOR}</tr>
      <tr>{FOR(1,2)}<td>{RANDKEYWORD}</td>{ENDFOR}</tr>
    </table>
  </td>
  <td><img src="{{imgPath}}/imgm/{RAND(1,{{imgCount}})}.jpg" alt="{RANDKEYWORD}" /></td>
</tr>
'''
