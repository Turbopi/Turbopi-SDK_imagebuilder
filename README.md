Turbopi-SDK_imagebuilder
=========
## Make OpenWrt image packaging more easy

![Turbopi-SDK_imagebuilder screencapture](https://github.com/Turbopi/Turbopi-SDK_imagebuilder/raw/master/common/screencapture-Turbopi-imagebuilder.png)

### Support Multi-Languages,Now:
	en
	zh-cn
	zh-tw
	jp
look forward to your contribution

### Run command:
	./init.sh


Your ImageBuilder dictionary must keep in builder/ folder.
And your Custom files must keep in files/

### So does like:

	builder
	├── OpenWrt-ImageBuilder-ramips_mt7620n-for-linux-i686
	└── OpenWrt-ImageBuilder-x86_generic-for-linux-i686

### and

	files
	├── files_ar71xx
	├── files_ar71xx_bb
	├── files_n14u_bb
	├── files_rg100a
	└── files_x86

Browser open: http://[Server]:[Port]
Use Default User:admin Pass:admin
And it will Works Well.

	############
	# Default User: admin
	# Default Pass: admin
	############

	############
	# You can change Password by:
	# cd [PATH]
	# local/httpd/bin/htpasswd -c .htpasswd [username]
	############

	############
	# To start service run:
	# cd [PATH]
	# sudo local/httpd/bin/apachectl restart
	############



www.turbopi.com © 2014. All Rights Reserved.	E-mail:417@xmlad.com