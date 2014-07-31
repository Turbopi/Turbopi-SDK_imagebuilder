#!/bin/sh
Home_dir=$PWD
eval `$Home_dir/bin/proccgi.cgi $*`
Lang_list=`ls $Home_dir/etc/lang | awk -F "." {'print $1'}`
[ -n "$FORM_lang_set" ] && sed -i '/LANG=/d' $Home_dir/etc/lang.conf && echo "LANG=\"$FORM_lang_set\"" >> $Home_dir/etc/lang.conf
eval `cat $Home_dir/etc/lang.conf`
eval `cat $Home_dir/etc/lang/$LANG".i18n"`
Builders=`ls -l $Home_dir/builder |grep ^d | grep "ImageBuilder.*i686" | awk {'print $NF'}`
Files=`ls -l $Home_dir/files |grep ^d | awk {'print $NF'} | grep "^files"`
temp_session=`echo "$Builders\n$Files" | sed '/^$/d' | md5sum | awk {'print $1'}`
[ "`cat $Home_dir/tmp/temp_session`" = "$temp_session" ] || rm $Home_dir/tmp/index.cgi.* && echo $temp_session > $Home_dir/tmp/temp_session
if
cat $Home_dir/tmp/$(basename $SCRIPT_NAME).$LANG | grep -q "DOCTYPE html"
then
cat $Home_dir/tmp/$(basename $SCRIPT_NAME).$LANG | sed "s/127.0.0.1/$SERVER_ADDR/g"
exit 0
else
	ps -aux | grep -v grep | grep -q "curl.*index.cgi" || if
		[ "$QUERY_STRING" == "temp" ]
		then
		echo "" > $Home_dir/tmp/$(basename $SCRIPT_NAME).$LANG
		curl $REQUEST_SCHEME://127.0.0.1:$SERVER_PORT$SCRIPT_NAME?temp >> $Home_dir/tmp/$(basename $SCRIPT_NAME).$LANG
		cat $Home_dir/tmp/$(basename $SCRIPT_NAME).$LANG | sed "s/127.0.0.1/$SERVER_ADDR/g"
		exit 0
		else
		echo "" > $Home_dir/tmp/$(basename $SCRIPT_NAME).$LANG
		curl $REQUEST_SCHEME://127.0.0.1:$SERVER_PORT$SCRIPT_NAME?temp >> $Home_dir/tmp/$(basename $SCRIPT_NAME).$LANG
		fi
fi


cat <<EOF

<!DOCTYPE html>
<!--[if lt IE 7]><html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]><html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]><html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--><html lang="en" class="no-js"> <!--<![endif]-->
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<title>$Lang_Turbopi_SDK_imagebuilder</title>
    <link href="/common/css/bootstrap.min.css" rel="stylesheet" />
    <link href="/common/css/bootstrap-theme.css" rel="stylesheet" />
    <link href="/common/css/common.css" rel="stylesheet" />
<style>
	body {
padding-top: 30px;
color: #3f3f3f;
}
body {
min-width: 960px;
}
body {
margin: 0;
font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
font-size: 14px;
line-height: 20px;
color: #333;
background-color: #fff;
}
.container, .navbar-static-top .container, .navbar-fixed-top .container, .navbar-fixed-bottom .container {
width: 940px;
}
.container {
margin-right: auto;
margin-left: auto;
}
.container {
max-width: 1000px;
}
.masthead{
    margin-bottom: 8px;
}
.jumbotron {
-webkit-background-size: cover;
-moz-background-size: cover;
background-size: cover;
padding: 0;
}
.main{
    background-color: #fff;
}
.features-section-wrapper {
    margin-bottom: 20px;
}
.bs-footer {
padding-top: 30px;
padding-bottom: 20px;
color: #777;
border-top: 1px solid #e5e5e5;
}
</style>
</head>
<body>
<script src="/common/js/jquery.min.js" type="text/javascript"></script>
<script src="/common/js/bootstrap.min.js" type="text/javascript"></script>
<script src="/common/js/common.js" type="text/javascript"></script>

<div class="container">
    <div class="row">
          <div class="controls">

EOF
if
[ "$FORM_userchange" = "userchange" ] && [ -n "$FORM_user" ] && [ -n "$FORM_passwd" ]
then
if
$Home_dir/httpd/bin/htpasswd -c -b -d .htpasswd $FORM_user $FORM_user >/dev/null 2>&1
#echo "$FORM_passwd" | $Home_dir/bin/htpasswd -c $Home_dir/.htpasswd $FORM_user | grep -q "Adding password"
then
cat <<EOF
<div class="col-md-12">
<div class="form-group">
<font size=2 color=#516D87><h2><p class="bg-info"><span class="glyphicon glyphicon-user"></span> $Lang_Username:$FORM_user </p></h2></font>
<font size=2 color=#516D87><h2><p class="bg-info"><span class="glyphicon glyphicon-credit-card"></span></span> $Lang_Password:$FORM_passwd </p></h2></font>
<font size=2 color=#516D87><h1><p class="bg-danger"><span class="glyphicon glyphicon-envelope"></span></span></span> $Lang_User_change_tip </p></h1></font>
<a href="/" class="btn btn-primary" role="button"><span class="glyphicon glyphicon-chevron-left"></span> $Lang_GO_Back </a>
</div>
</div>
EOF
exit 0
fi
elif
[ "$FORM_userchange" = "userchange" ] && [ -z "$FORM_user" ]
then
cat <<EOF
<div class="col-md-12">
<div class="form-group">
<font size=2 color=#516D87><h1><p class="bg-danger"><span class="glyphicon glyphicon-envelope"></span></span></span> $Lang_Username_not_seted </p></h1></font>
<a href="/" class="btn btn-primary" role="button"><span class="glyphicon glyphicon-chevron-left"></span> $Lang_GO_Back </a>
</div>
</div>
EOF
exit 1
elif
[ "$FORM_userchange" = "userchange" ] && [ -z "$FORM_passwd" ]
then
cat <<EOF
<div class="col-md-12">
<div class="form-group">
<font size=2 color=#516D87><h1><p class="bg-danger"><span class="glyphicon glyphicon-envelope"></span></span></span> $Lang_Password_not_seted </p></h1></font>
<a href="/" class="btn btn-primary" role="button"><span class="glyphicon glyphicon-chevron-left"></span> $Lang_GO_Back </a>
</div>
</div>
EOF
exit 1
fi
for i in `echo "$Lang_list"`
do
i_seted=""
[ "${i}" = "$LANG" ] && i_seted="selected"
Lang_str=`echo "$Lang_str""<option value="${i}" $i_seted>${i}</option>"`
done
cat <<EOF
<div class="form-group">
	<a href="/"><h1><p class="bg-primary col-sm-2"> $LANG_Index </p></h1></a>
	<a href="http://www.turbopi.com" target="_blank"><h1><p class="bg-primary col-sm-8">$Lang_Turbopi_SDK_imagebuilder</p></h1></a>
	<form class="form-horizontal" role="form" method="post">
	<div class="col-sm-2">
		<select class="form-control" name="lang_set" onChange="javascript:this.form.submit()">
		$Lang_str
		</select>
	</div>
	</form>
</div>
<div class="form-group col-sm-12">
<div class="form-group col-sm-10">
<font size=2 color=#516D87><h4><p class="bg-danger"><span class="glyphicon glyphicon-envelope"></span></span></span> $Lang_Logout_tip </p></h4></font>
</div>
	<div class="form-group col-sm-2">
	<form class="form-horizontal" role="form" method="post">
	<a href="http://logout:logout@$HTTP_HOST:$SERVER_PORT/logout/" class="btn btn-large btn-info"><span class="glyphicon glyphicon-log-out"></span> $Lang_Logout </a>
	</form>
	</div>
</div>
EOF
grep [^.*$] $Home_dir/.htpasswd >/dev/null 2>&1 || cat <<EOF
<div class="col-md-12">
<font size=2 color=#516D87><h2><p class="bg-danger"><span class="glyphicon glyphicon-user"></span> $Lang_Username $Lang_Password $Lang_not_seted</p></h2></font>
</div>
EOF
colors="bg-primary bg-success bg-info bg-warning bg-danger"
for i in `echo "$Builders"`
do
[ -n "$color_num" ] || color_num=1
[ "$color_num" -gt "`echo "$colors" |grep -o " "| wc -l`" ] && color_num=1
color=`echo "$colors" | awk {'print $color_num'} color_num=$color_num`
color_num="`expr $color_num + 1`"
li_str_tmp=`cat <<EOF
<li><a href="#div_${i}" data-toggle="tab" class="$color">${i}</a></li>
EOF`
li_str=`echo "$li_str\n$li_str_tmp"`
cd $Home_dir/builder/${i}
models_str=""
make_info=`make info`
for modlel in `echo "$make_info" | grep ":$" | grep -v "Available Profiles" | sed 's/:$//g'`
do
model_tmp=`cat <<EOF
<label class="radio-inline">
  <input type="radio" name="model" id="models" value="${modlel}"> ${modlel}
</label>
EOF`
models_str=`echo "$models_str\n$model_tmp"`
done
files_str=""
for file in `echo "$Files"`
do
files_str_tmp=`cat <<EOF
<label class="radio-inline">
  <input type="radio" name="file" id="files" value="${file}"> ${file}
</label>
EOF`
files_str=`echo "$files_str\n${files_str_tmp}"`
done
content_str_temp=`cat <<EOF
<div class="tab-pane " id="div_${i}">
<form action="exec_build.cgi" method="post">
<div class="col-sm-6">
<legend><span class="glyphicon glyphicon-hdd"></span> $Lang_Model </legend>

<div class="panel-group" id="accordion">
  <div class="panel panel-primary">
    <div class="panel-heading">
      <h4 class="panel-title">
        <a data-toggle="collapse" data-parent="#accordion" href="#collapse${i}">
          <span class="glyphicon glyphicon-comment"></span> $Lang_Make_Info_Detail
        </a>
      </h4>
    </div>
    <div id="collapse${i}" class="panel-collapse collapse">
      <div class="panel-body">
      <pre>$make_info</pre>
	  </div>
    </div>
  </div>
</div>

$models_str
<legend><span class="glyphicon glyphicon-file"></span> $Lang_Files </legend>
$files_str
</div>
            <div class="textarea col-sm-6">
			<legend><span class="glyphicon glyphicon-briefcase"></span> $Lang_Packages </legend>
                  <textarea style="width:100%;height:400px" name="packages" class="bg-warning"></textarea>
            </div>
<input type="hidden" name="builder" value="${i}">
<button type="submit" class="btn btn-large btn-info" id="submit"><span class="glyphicon glyphicon-check"></span> $Lang_Submit </button>
</form>
</div>

EOF`
content_str=`echo "$content_str\n$content_str_temp"`
done
cat <<EOF

<ul class="nav nav-tabs">
$li_str
</ul>
<div class="tab-content">
$content_str

<div class="tab-pane active" id="none">
<div class="col-sm-12">
<font size=2 color=#516D87><h2><p class="bg-info">$Lang_Please_choose_a_Builder</p></h2></font>
</div>
</div>

</div>

EOF
cat <<END

          </div>
        </div>
     </div>
</div>


</body>
<footer class="bs-footer" role="contentinfo">
  <div class="container">
    <div>
<div class="form-group">
	<div class="col-sm-5">
    <p>Powered by <a href="http://www.turbopi.com" target="_blank">Turbopi.com</a>&nbsp; 2014.
	</div>
<form class="form-horizontal" role="form" method="post">
	<div class="col-sm-3">
    <input type="text" name="user" value="" class="form-control" placeholder="$Lang_Username">
	</div>
	<div class="col-sm-3">
    <input type="password" name="passwd" class="form-control" placeholder="$Lang_Password">
	</div>
	<div class="col-sm-1">
	<input type="hidden" name="userchange" value="userchange">
	<button type="submit" class="btn btn-large btn-info" id="submit"><span class="glyphicon glyphicon-user"></span> $Lang_Submit </button>
	</div>
</form>
</div>
    </div>
    </p>
</div>
</footer>
</html>
END
