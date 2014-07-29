#!/bin/sh
PWD=`pwd`
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
[ -d $PWD/builder ] || mkdir $PWD/builder
[ -d $PWD/files ] || mkdir $PWD/files
[ -d $PWD/tmp ] || mkdir $PWD/tmp

if
[ ! -f $PWD/etc/web_server.conf ]
then
ask
cat <<EOF > $PWD/etc/web_server.conf
nochroot # no
user=`whoami`
host=$IP
port=$PORT
dir=`pwd`
cgipat=**.cgi
pidfile=$PWD/tmp/web_server.pid
logfile=$PWD/tmp/web_server.log
charset=UTF-8
EOF
fi
chown `whoami` $PWD/etc/web_server.conf
killall mini_httpd
eval `cat $PWD/etc/web_server.conf | grep -E "^host=|^port="`
cat <<EOF
Starting mini_httpd Server on $host:$port..
You can change Password by:
$PWD/bin/htpasswd .htpasswd [username]
EOF
$PWD/bin/mini_httpd -C $PWD/etc/web_server.conf 2>&1



