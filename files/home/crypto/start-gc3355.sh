#!/bin/bash
config="/home/crypto/configs/gc3355"
modules=0
GC=""
GC_devs=""
for d in $(ls /dev/ttyACM*); do
	GC="${GC}${d},"
        GC_devs="$GC_devs $d"
	modules=$(($modules+1))
done
GC=$(echo $GC | sed s/",$"//g)

[ $modules -lt 1 ] && {
	echo "Not found any gc3355 device, exiting..."
	read p
	exit 1
}

echo "Found $modules GC3355 devices"

[ ! -f $config ] && {
	echo "Config file foor pools do not exist, please execute the gc3355 configurator tool"
	exit 2
}

sha_pool="$(cat $config | grep ^sha | cut -d'|' -f2)"
sha_user="$(cat $config | grep ^sha | cut -d'|' -f3)"
sha_pass="$(cat $config | grep ^sha | cut -d'|' -f4)"
scrypt_pool="$(cat $config | grep ^scrypt | cut -d'|' -f2)"
scrypt_user="$(cat $config | grep ^scrypt | cut -d'|' -f3)"
scrypt_pass="$(cat $config | grep ^scrypt | cut -d'|' -f4)"
dual=""

[ -n "$sha_pool" ] && {
	screen -x sha -X quit
	echo "Starting sha256 gc3355 miners in screen sha"
	screen -S sha -m -d sudo cgminer \
	--gridseed-options=baud=115200,freq=800,chips=5,modules=$modules,usefifo=0,btc=16 --hotplug=1 \
	 -o $sha_pool -u $sha_user -p $sha_pass
	dual="--dual"
	(xterm -e "screen -x sha") &
}

[ -n "$scrypt_pool" ] && {
	screen -x scrypt -X quit
	echo "Starting scrypt gc3355 miners in screen scrypt"
        [ -n "$sha_pool" ] && {
		# dual mode
		screen -S scrypt -m -d sudo minerd -o $scrypt_pool -u $scrypt_user -p $scrypt_pass -G $GC $dual -D
		(xterm -e "screen -x scrypt") &
	} || {
		# scrypt only mode
		m=0
		for g in $GC_devs; do
			echo "Starting gc3355 in scrypt only mode"
			screen -S scrypt${m} -m -d sudo minerd -o $scrypt_pool -u $scrypt_user -p $scrypt_pass -G $g -F 850 -D
			m=$(($m+1))
			sleep 1
                        (xterm -e "screen -x scrypt${m}") &
		done
	}
}
	
ln -s /home/crypto/start-gc3355.sh /home/crypto/start_gc 2>/dev/null

echo "Done, press any key to exit"
read

