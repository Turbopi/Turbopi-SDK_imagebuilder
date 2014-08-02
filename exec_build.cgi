#!/bin/sh
Home_dir=$PWD
eval `$Home_dir/bin/proccgi.cgi $*`
Lang_list=`ls $Home_dir/etc/lang | awk -F "." {'print $1'}`
[ -n "$FORM_lang_set" ] && sed '/^LANG=/d' && echo "LANG=\"$FORM_lang_set\"" >> $Home_dir/etc/lang.conf
eval `cat $Home_dir/etc/lang.conf`
eval `cat $Home_dir/etc/lang/$LANG".i18n"`
eval `echo $LANG | sed 's/-/_/g'`"_seted"=selected
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
	<link rel="stylesheet" href="/common/css/bootstrap.min.css">
	<script src="/common/js/jquery.min.js"></script>
	<script src="/common/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="/common/js/jquery.zclip.js"></script>
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
<script>
\$(document).ready(function(){
    \$('#copyBtn').zclip({
        path : '/common/js/ZeroClipboard.swf',
        copy : \$('#clip_content').text()
    });
});
</script>
</head>
<body>

<div class="container">
    <div class="row">
EOF

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
EOF

[ -z "$FORM_builder" ] && Error_str1=`cat <<EOF
<font size=2 color=#516D87><h2><p class="bg-danger"><span class="glyphicon glyphicon-remove"></span> $Lang_Builder_not_seted </p></h2></font>
EOF`
[ -z "$FORM_model" ] && Error_str2=`cat <<EOF
<font size=2 color=#516D87><h2><p class="bg-danger"><span class="glyphicon glyphicon-remove"></span> $Lang_Model_not_seted </p></h2></font>
EOF`
[ -z "$FORM_packages" ] && Error_str3=`cat <<EOF
<font size=2 color=#516D87><h2><p class="bg-danger"><span class="glyphicon glyphicon-remove"></span> $Lang_Packages_not_seted </p></h2></font>
EOF`
[ -z "$FORM_file" ] && Error_str4=`cat <<EOF
<font size=2 color=#516D87><h2><p class="bg-danger"><span class="glyphicon glyphicon-remove"></span> $Lang_file_not_seted </p></h2></font>
EOF`
ps -aux | grep -v grep | grep -q "call_image.*$FORM_builder" && Error_str5=`cat <<EOF
<font size=2 color=#516D87><h2><p class="bg-danger"><span class="glyphicon glyphicon-remove"></span> $FORM_builder $Lang_Builder_in_work </p></h2></font>
EOF`
Error_str=`echo "$Error_str1" "$Error_str2" "$Error_str3" "$Error_str4" "$Error_str5"`
if
echo "$Error_str" | grep -q "bg-danger"
then
cat <<EOF
<div class="col-md-12">
<div class="form-group">
$Error_str
<a href="/" class="btn btn-primary" role="button"><span class="glyphicon glyphicon-chevron-left"></span> $Lang_GO_Back </a>
</div>
</div>
EOF
exit 1
fi

builder=$FORM_builder
model=$FORM_model
packages="$FORM_packages"
file=$FORM_file

Work_str="make image PROFILE=$model PACKAGES=\"$packages\" FILES=$Home_dir/files/$file/"
cat <<EOF
<div class="col-md-12">
<div class="form-group">
<a href="/" class="btn btn-info" role="button"><span class="glyphicon glyphicon-chevron-left"></span>$Lang_Back</a>
<!-- Button trigger modal -->
<button class="btn btn-primary" data-toggle="modal" data-target="#myModal">
<span class="glyphicon glyphicon-align-left"></span>$Lang_Used_command
</button>

<!-- Modal -->
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only"> $LANG_Close </span></button>
        <h4 class="modal-title" id="myModalLabel">$Lang_Used_command</h4>
      </div>
      <div class="modal-body">
        <kbd># $Work_str</kbd>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal"><span class="glyphicon glyphicon-remove"></span> $LANG_Close </button>
		<div id="clip_content" class="hidden">$Work_str</div>
		<button type="button" id="copyBtn" class="btn btn-primary"><span class="glyphicon glyphicon-floppy-disk"></span> $LANG_Copy </button>
      </div>
    </div>
  </div>
</div>


</div>
</div>
          <div class="controls">
            <div class="textarea">
                  <textarea disabled style="width:100%;height:460px" type="" class="">
EOF
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
cd $Home_dir/builder/$builder
make clean 2>&1
echo $packages
make image PROFILE=$model FILES=$Home_dir/files/$file/ PACKAGES="$packages" 2>&1


if [ $? = 0 ]
then
str=`cat <<EOF
<a href="/builder/$builder" class="btn btn-primary" role="button"><span class="glyphicon glyphicon-folder-open"></span> $Lang_GO_BinDir </a>
<font size=2 color=#0000FF>$Lang_Success</font>
EOF`
else
str=`cat <<EOF
<a href="/" class="btn btn-danger" role="button"><span class="glyphicon glyphicon-chevron-left"></span> $Lang_GO_Back </a>
<font size=2 color=#FF0000>$Lang_Failed</font>
EOF`
fi
cat <<END

					</textarea>
$str
            </div>
          </div>
        </div>
</div>
</div>




</body>
<footer class="bs-footer" role="contentinfo">
  <div class="container">
    <div>
<!--     -->
        <p>Powered by <a href="http://www.turbopi.com" target="_blank">Turbopi.com</a>&nbsp; 2014.
    </div>
    </p>
</div>
</footer>
</html>
END
