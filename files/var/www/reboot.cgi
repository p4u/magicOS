#!/bin/bash

echo "Content-type: text/html"
echo ""


echo "<a target=\"_blank\" href=\"http://magicpool.org\">"
echo "<img src=\"/logo.png\" style=\"display:block;margin-left: auto;margin-right: auto;\">"
echo "</a>"
echo "<hr>"

[ -z "$QUERY_STRING" ] && {
echo "
<form id='reboot' action='reboot.cgi' method='GET'>
	Password: <input type='text' name='password' />
	<input type='submit' value='Reboot' />
</form>"
} || {
	password="$(echo $QUERY_STRING | cut -d\& -f1 | cut -d= -f2)"
	system_password="$(cat /etc/magicpool.password 2>/dev/null)"

	[ -n "$system_password" -a "$password" != "$system_password" ] && {
		echo "<b>Wrong password!</b><br/>"
		echo "System not rebooted"
		exit 0
	}
	echo "Updating magicpool agent..."
	echo "<pre>"
	sudo /bin/mpconfandreboot &
	echo "</pre>"
	echo "<p>Rebooting... see you in a minute!</p>"
}
