<?
error_reporting  (6143);
include("include/function.php");
include("config.php");
include("confbd.php");
include("include/bd.php");

if(count($_POST)>1){switch (@$_GET['module']) {
              case "zip":
               include("post/zip.php");
                break;
              case "ftp":
               include("post/ftp.php");
                break;
              case "hand":
               include("post/hand.php");
                break;
               case "config":
               include("post/config.php");
                break;
               case "sinonim":
               include("post/sinonim.php");
                break;
               case "proxy":
               include("post/proxy.php");
                break;
               case "help":
               include("post/help.php");
                break;
                default:
               include("post/zip.php");
                break;
            }
            exit();}
?><html>

<head>
<title>VIP Bablo - генератор сателлитов</title>
<meta http-equiv="content-type" content="text/html; charset=windows-1251"></head>
<script language="JavaScript">
function na_open_window(name, url, left, top, width, height, toolbar, menubar, statusbar, scrollbar, resizable)
{
  toolbar_str = toolbar ? 'yes' : 'no';
  menubar_str = menubar ? 'yes' : 'no';
  statusbar_str = statusbar ? 'yes' : 'no';
  scrollbar_str = scrollbar ? 'yes' : 'no';
  resizable_str = resizable ? 'yes' : 'no';


  window.open(url, name, 'left='+left+',top='+top+',width='+width+',height='+height+',toolbar='+toolbar_str+',menubar='+menubar_str+',status='+statusbar_str+',scrollbars='+scrollbar_str+',resizable='+resizable_str);
}
function changetpl(name){
opt=document.getElementById("tpl");
for (var i=opt.options.length-1; i >= 0; i--)
  {
      if(opt.options[i].value==name){
      	opt.options[i].selected=true;
      }
  }
}
function getSelectedIndexes (oListbox)
{
  var arrIndexes = new Array;
  for (var i=0; i < oListbox.options.length; i++)
  {
      if (oListbox.options[i].selected) arrIndexes.push(i);
  }
  return arrIndexes;
};
</script>

<body bgcolor="#EFEFDE" text="black" link="blue" vlink="purple" alink="red">
<table width="731" height="79" cellpadding="0" cellspacing="0" align="center">
    <tr>
        <td width="731" height="44">
            <table width="691" height="40" cellpadding="0" cellspacing="0">
                <tr>
                    <td width="576" height="34"><b><font size="4" face="Verdana" color="#A8A2A2">Генератор Сателлитов</font></b></td>
                    <td width="53" height="34">
                        <p align="center"><b><font size="5">VIP</font></b></p>
                    </td>
                    <td width="62" height="34">
                        <p align="left"><b><font size="4" color="red">Bablo</font></b></p>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td width="731">
        <table width="698" cellpadding="0" cellspacing="0" style="padding:4pt; border-width:1pt; border-color:rgb(189,193,190); border-style:solid;" height="149">
                <tr>
                    <td width="696" height="147">
                        <div align="right">
                            <table width="692" cellpadding="0" cellspacing="0" height="100%">
                                <tr>
                                    <td width="468">
                                        <table width="453" cellpadding="0" cellspacing="0" bgcolor="white" style="padding:4pt; border-width:1pt; border-color:rgb(185,203,220); border-style:solid;" height="100%">
                                            <tr>
                                                <td width="451" height="468" valign="top">
            <?
            switch (@$_GET['module']) {
              case "zip":
               include("block/zip.php");
                break;
              case "ftp":
               include("block/ftp.php");
                break;
              case "hand":
               include("block/hand.php");
                break;
               case "config":
               include("block/config.php");
                break;
               case "sinonim":
               include("block/sinonim.php");
                break;
               case "proxy":
               include("block/proxy.php");
                break;
               case "help":
               include("block/help.php");
                break;
                default:
               include("block/zip.php");
                break;
            }
            ?>
               </td>
                                            </tr>
                                        </table>
                                    </td>
                                    <td width="224" valign="top">
                                        <? include('menu.php'); ?>
                                       </td>
                                </tr>
                            </table>
                        </div>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
<p>&nbsp;</p>
</body>

</html>