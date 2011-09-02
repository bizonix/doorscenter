<?php
umask(0);
symlink('/var/www/common/images', 'images');
system('tar -zxf bean.tgz');
unlink('bean.tgz');
?>
