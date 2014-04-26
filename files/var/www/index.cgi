#!/bin/bash

echo "Content-type: text/html"
echo ""
export DISPLAY=:0

echo "<a target=\"_blank\" href=\"http://magicpool.org\">"
echo "<img src=\"/logo.png\" style=\"display:block;margin-left: auto;margin-right: auto;\">"
echo "</a>"
echo "<hr>"

echo "<ul>"
echo "<li><a href=\"/configure.cgi\">Configure your magic miner!</a></li>"
echo "<li><a href=\"/reboot.cgi\">Reboot your miner!</a></li>"
echo "</ul>"

echo "<h1>Miner status</h1>"
echo "[Uptime]"
echo "<pre>"
uptime
echo "</pre>"
echo "[GPU]" 
echo "<pre>"
sudo -u crypto /usr/local/bin/atitweak -s
echo "</pre>"

echo "<h1>Magicpool</h1>"
echo "<p>Access to magicpool.org over Internet?"
timeout 2 ping magicpool.org -c 1 -s 16 2>/dev/null 1>/dev/null
[ $? -eq 0 ] && echo "YES" || echo "NO"

echo "<h1>Sgminer</h1>"
echo "<p>Is sgminer working?"
[ $(ps -ef| grep sgminer | wc -l) -lt 2 ] && echo "NO" || echo "YES"
echo "</p>"
echo "[Config file]"
echo "<pre>"
cat /home/crypto/.sgminer/sgminer.conf
echo "</pre>"


