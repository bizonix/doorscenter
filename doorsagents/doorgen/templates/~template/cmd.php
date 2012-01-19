<?php
umask(0);
symlink('/var/www/common/images', 'images');
symlink('/var/www/common/js', 'js');
system('tar -zxf bean.tgz');
unlink('bean.tgz');
?>
