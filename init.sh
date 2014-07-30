#!/bin/sh
HOME_DIR=`pwd`
if
[ "`whoami`" == "root" ]
then
echo "Canot Run by root!!" && exit 2
fi
build()
{
[ -d $HOME_DIR/sources ] || mkdir $HOME_DIR/sources
[ -f $HOME_DIR/sources/httpd-2.4.10.tar.gz ] || wget -P $HOME_DIR/sources/ http://archive.apache.org/dist/httpd/httpd-2.4.10.tar.gz
[ $? -eq 0 ] && echo "Source httpd-2.4.10.tar.gz esit."
[ -f $HOME_DIR/sources/apr-1.5.1.tar.gz ] || wget -P $HOME_DIR/sources/ http://archive.apache.org/dist/apr/apr-1.5.1.tar.gz
[ $? -eq 0 ] && echo "Source apr-1.5.1.tar.gz esit."
[ -f $HOME_DIR/sources/apr-util-1.5.3.tar.gz ] || wget -P $HOME_DIR/sources/ http://archive.apache.org/dist/apr/apr-util-1.5.3.tar.gz
[ $? -eq 0 ] && echo "Source apr-util-1.5.3.tar.gz esit."
[ -f $HOME_DIR/sources/pcre-8.34.tar.gz ] || wget -P $HOME_DIR/sources/ http://ftp.cs.stanford.edu/pub/exim/pcre/pcre-8.34.tar.gz
[ $? -eq 0 ] && echo "Source pcre-8.34.tar.gz esit."

md5_str=`cat <<EOF
9b5f9342f73a6b1ad4e8c4b0f3f5a159  httpd-2.4.10.tar.gz
d3538d67e6455f48cc935d8f0a50a1c3  apr-1.5.1.tar.gz
71a11d037240b292f824ba1eb537b4e3  apr-util-1.5.3.tar.gz
eb34b2c9c727fd64940d6fd9a00995eb  pcre-8.34.tar.gz
EOF`
cd $HOME_DIR/sources/
if
for i in httpd-2.4.10.tar.gz apr-1.5.1.tar.gz apr-util-1.5.3.tar.gz pcre-8.34.tar.gz; do md5sum ${i}; done | sed '/^$/d' | tr -d "\r" | sort -n | md5sum | awk {'print $1'} | grep "`echo "$md5_str" | sed '/^$/d' | sort -n | md5sum | awk {'print $1'}`"
then
echo "file match!"
else
echo "Source No offcial !!" && exit 1
fi
for i in httpd-2.4.10.tar.gz apr-1.5.1.tar.gz apr-util-1.5.3.tar.gz pcre-8.34.tar.gz; do tar zxvf ${i}; done
cd $HOME_DIR/sources/apr-1.5.1
[ -f Makefile ] && make clean
./configure --prefix=$HOME_DIR/local/apr --with-devrandom=/dev/urandom --disable-dso ac_cv_sizeof_struct_iovec=1 apr_cv_process_shared_works=no apr_cv_mutex_robust_shared=no apr_cv_tcp_nodelay_with_cork=yes ac_cv_struct_rlimit=yes && make && make install
cd $HOME_DIR/sources/apr-util-1.5.3
[ -f Makefile ] && make clean
./configure --prefix=$HOME_DIR/local/apr-util --with-apr=$HOME_DIR/local/apr/bin/apr-1-config ac_cv_file_dbd_apr_dbd_mysql_c=no ac_cv_path_ODBC_CONFIG= APR_BUILD_DIR="$HOME_DIR/local/apr-1.5.1" && make && make install
cd $HOME_DIR/sources/pcre-8.34
[ -f Makefile ] && make clean
./configure --prefix=$HOME_DIR/local/pcre --enable-utf8 --enable-unicode-properties --disable-cpp && make && make install
cd $HOME_DIR/sources/httpd-2.4.10
[ -f Makefile ] && make clean
[ -d $HOME_DIR/logs ] || $HOME_DIR/logs
./configure --prefix=$HOME_DIR/local/httpd --with-apr="$HOME_DIR/local/apr/bin/apr-1-config" --with-apr-util="$HOME_DIR/local/apr-util/bin/apu-1-config" --with-pcre="$HOME_DIR/local/pcre/bin/pcre-config" --enable-http --enable-ssl --enable-proxy --disable-disk-cache --enable-maintainer-mode --enable-mime-magic --without-suexec-bin --sysconfdir=$HOME_DIR/etc ap_void_ptr_lt_long=no logfiledir="$HOME_DIR/logs" && make && make install

}


ask()
{
echo -n "Bind to(127.0.0.1/0.0.0.0:)"
read IP
if
echo "$IP" | grep -qE "^127\.0\.0\.1$|^0\.0\.0\.0$"
then
echo "Use IP:$IP"
else
echo "Wrong IP!!" && exit 2
fi

echo -n "Bind port(80/8080/etc:)"
read PORT
if
echo "$PORT" | grep -qE "^[0-9]+$"
then
echo "Use PORT:$IP"
else
echo "Wrong Port!!" && exit 2
fi
}


if
[ ! -f $HOME_DIR/etc/httpd.conf ] || [ `grep "#" $HOME_DIR/etc/httpd.conf | wc -l` -gt 10 ]
then
ask
build
cat <<EOF > $HOME_DIR/etc/httpd.conf
ServerRoot "$HOME_DIR/"
Timeout 600
KeepAlive On
MaxKeepAliveRequests 0
KeepAliveTimeout 150
Listen $IP:$PORT
<IfModule unixd_module>
User `logname`
Group `logname`
</IfModule>
ServerAdmin turbopi@example.com
<Directory />
    AllowOverride none
    Require all denied
</Directory>
DocumentRoot "$HOME_DIR/"
<Directory "$HOME_DIR/">
AuthType Basic
AuthName "Authentication Required"
AuthUserFile $HOME_DIR/.htpasswd
Require valid-user
Order allow,deny
Allow from localhost
Allow from 127.0.0.1
Satisfy Any
    Options Indexes FollowSymLinks
    Options +ExecCGI
</Directory>
<Directory "$HOME_DIR/logout">
AuthType Basic
AuthName "Logout"
AuthUserFile $HOME_DIR/logout/.htpasswd
Require user logout
</Directory>
<IfModule dir_module>
    DirectoryIndex index.html index.cgi
</IfModule>
<Files ".ht*">
    Require all denied
</Files>
ErrorLog "logs/error_log"
LogLevel warn
<IfModule log_config_module>
    LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
    LogFormat "%h %l %u %t \"%r\" %>s %b" common
    <IfModule logio_module>
      LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %I %O" combinedio
    </IfModule>
    CustomLog "logs/access_log" common
</IfModule>
<IfModule alias_module>
    ScriptAlias /cgi-bin/ "$HOME_DIR/httpd/cgi-bin/"
</IfModule>
<IfModule cgid_module>
</IfModule>
<Directory "$HOME_DIR/httpd/cgi-bin">
    AllowOverride None
    Options None
    Require all granted
</Directory>
<IfModule mime_module>
    TypesConfig $HOME_DIR/etc/mime.types
    AddType application/x-compress .Z
    AddType application/x-gzip .gz .tgz
    AddHandler cgi-script .cgi
</IfModule>
<IfModule proxy_html_module>
Include $HOME_DIR/etc/extra/proxy-html.conf
</IfModule>
<IfModule ssl_module>
SSLRandomSeed startup builtin
SSLRandomSeed connect builtin
</IfModule>

EOF
[ -f $HOME_DIR/.htpasswd ] || $HOME_DIR/local/httpd/bin/htpasswd -c -b -d $HOME_DIR/.htpasswd admin admin
[ -d $HOME_DIR/logout ] || mkdir $HOME_DIR/logout
[ -f $HOME_DIR/logout/.htpasswd ] || $HOME_DIR/local/httpd/bin/htpasswd -c -b -d $HOME_DIR/logout/.htpasswd logout logout
[ -d $HOME_DIR/tmp ] || mkdir $HOME_DIR/tmp
[ -d $HOME_DIR/logs ] || mkdir $HOME_DIR/logs
fi

cat <<EOF
Starting Web Server on `cat $HOME_DIR/etc/httpd.conf | grep "^Listen " | awk {'print $2'}`..
############
# Default User: admin
# Default Pass: admin
############

############
# You can change Password by:
# $HOME_DIR/local/httpd/bin/htpasswd -c .htpasswd [username]
############

############
# To start service run:
# sudo $HOME_DIR/local/httpd/bin/apachectl restart
############
EOF



