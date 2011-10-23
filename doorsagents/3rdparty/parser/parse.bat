@echo off
set path=%path%;C:\Work\snippets\parser
C:\Work\snippets\parser\lib\php -c C:\Work\snippets\parser\lib\php.ini -f C:\Work\snippets\parser\snipit.php >> C:\Work\snippets\parser\parser.log
C:\Work\doorscenter\doorsagents\snippets-done.bat
exit
