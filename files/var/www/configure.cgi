#!/bin/bash

echo "Content-type: text/html"
echo ""


echo "<a target=\"_blank\" href=\"http://magicpool.org\">"
echo "<img src=\"/logo.png\" style=\"display:block;margin-left: auto;margin-right: auto;\">"
echo "</a>"
echo "<hr>"

#system_password="$(cat /etc/magicpool.password 2>/dev/null)"
#
#[ -n "$system_password" ] && {
#	form_sys_pass="$(echo $QUERY_STRING | cut -d\& -f1 | cut -d= -f2)"
#	[ "$form_sys_pass" != "$system_password" ] && {
#		echo '
#		<form id="pass" action="configure.cgi" method="GET">
#			Please, enter the password to configure your miner
#		<input type="text" name="sys_pass"/>
#		<input type="submit" value="Go" />
#		</form>'
#		exit 0
#	}
#}

[ -z "$QUERY_STRING" ] && {

echo "<p>Welcome to the MagicOS, first of all you need to create a new worker in your magicpool.org account.<br/>"
echo "Also you must enable the remote file configuration, then you can edit the sgminer config file from your account.<br/>"
echo "If you already did so, you can proceed.</p>"

echo "<p>Bienvenido a MagicOS, antes que nada necesitas crear un nuevo worker en tu cuenta de magicpool.org.<br/>"
echo "También necessitas activar la opción de configuración remota, entonces podrás editar el fichero de configuratión de sgminer des de tu cuenta.<br/>"
echo "Si ya lo has hecho puedes continuar.</p>"

echo "<hr>"

current_username="$(cat /etc/magicpool.conf | cut -d: -f2 | cut -d, -f1 | tr -d \"{})"
current_worker="$(cat /etc/magicpool.conf  | cut -d: -f3 | cut -d, -f1 | tr -d \"{})"

echo "
<form id='conf' action='configure.cgi' method='GET'>
	<ul>
	<li>User name: <input type='text' name='user' value='$current_username'/></li>
	<li>Worker alias: <input type='text' name='worker' value='$current_worker' /></li>
	<li>Password: <input type='text' name='password' /></li>
	</ul>
	<input type='submit' value='Configure' />
</form>"
echo '<p>The password will be used for future accesses to this configuration page. Leave it blank if you do not want to be asked for it.</p>'
echo '<p>If you do not have account register it in <a target="_blank" href="http://magicpool.org">magicpool.org</a></p>'

} || {
	user="$(echo $QUERY_STRING | cut -d\& -f1 | cut -d= -f2)"
	worker="$(echo $QUERY_STRING | cut -d\& -f2 | cut -d= -f2)"
	password="$(echo $QUERY_STRING | cut -d\& -f3 | cut -d= -f2)"
	system_password="$(cat /etc/magicpool.password 2>/dev/null)"

	[ -n "$system_password" -a "$password" != "$system_password" ] && {
		echo "<b>Wrong password!</b><br/>"
		echo "Miner not configured."
		exit 0
	}
	

	[ -z "$user" -o -z "$worker" ] && echo "ERROR: You must enter username and worker name" && exit 2
	echo "{\"username\":\"$user\",\"workeralias\":\"$worker\"}" | tee /tmp/magicpool.conf
	echo $password > /tmp/magicpool.password
	sudo /bin/mpconfsync
	sudo /bin/mphostsync "$worker"
	echo "<p>Magicpool agent configured!</p>"
	echo "<p><b>Now you must go to your <a target='_blank' href='http://magicpool.org'>magicpool</a> user account, enable and configure the sgminer options for your card.</b></p>"
	echo "<p>Once it is properly configured, click the button Reboot.</p>"
	echo "<form id='reboot' action='reboot.cgi' method='GET'>"
	echo "<input type='hidden' name='password' value='$system_password'/>"
	echo "<input type='submit' value='Reboot' />"
	echo "</form>"
}
