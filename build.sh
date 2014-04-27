#¡/bin/bash
FS="magicOSfiles.tar.gz"
FILES="files"
BUILD="build"
ROOT_SIZE="5000"
SWAP_SIZE="500"
OFFSET="10"
IMG_OUTPUT="magicOS.img"
MBR="mbr.bin"
MNT="mnt"

error() {
	echo "[ERROR]: $@"
	exit 1
}

prepare() {
	echo "Preparing environment"
	[ ! -d "$BUILD" ] && mkdir -p $BUILD
	[ ! -d "$MNT" ] && mkdir -p $MNT
	[ ! -f "$FS" ] && error "filesystem file $FS does not exist, you need to download it, please see README"
	sudo tar xzf $FS -C $BUILD
	[ $? -eq 0 ] && echo "Filesystem directory prepared" || error "with $FS file, corrupted?"
}

copy_files() {
	echo "Copying files"
	[ ! -d "$BUILD" ] && error "$BUILD directory does not exist"
	sudo cp -a $FILES/* $BUILD/
	[ $? -eq 0 ] && echo "Custom files copied" || error "copying custom files"
}

build_img_partitions() {
	echo "Creating images"
	dd if=/dev/zero of=${IMG_OUTPUT}.root bs=1048576 count=$ROOT_SIZE
	dd if=/dev/zero of=${IMG_OUTPUT}.offset bs=1048576 count=$OFFSET
	dd if=/dev/zero of=${IMG_OUTPUT}.swap bs=1048576 count=$SWAP_SIZE
		
	echo "Creating filesystems"
	mkfs.ext4 ${IMG_OUTPUT}.root -U 00000000-0000-0000-0000-000000000069 -F -L magicOSroot
	mkswap ${IMG_OUTPUT}.swap -U 00000000-0000-0000-0000-000000000070 -f
	
}

mount_root() {
	echo "Mounting root image to $MNT"
	sudo mount magicOS.img.root $MNT -o loop
	[ $? -ne 0 ] && error "Cannot mount root partition to $MNT!"
}

copy_root_files() {
	echo "Copying files from $BUILD to $MNT"
	cp -a $BUILD/* $MNT/
}

build_final_img() {
	echo "Creating final image"
	cat $MBR ${IMG_OUTPUT}.root ${IMG_OUTPUT}.offset ${IMG_OUTPUT}.swap > ${IMG_OUTPUT}
	parted -s ${IMG_OUTPUT} mklabel msdos
	parted -s ${IMG_OUTPUT} unit MiB mkpart primary ext3 1 $(($ROOT_SIZE+$OFFSET))
	parted -s ${IMG_OUTPUT} unit MiB mkpart primary linux-swap $(($ROOT_SIZE+$OFFSET)) $(($ROOT_SIZE+$OFFSET+${SWAP_SIZE}))
}

clean() {
	sudo umount $MNT
	rm -f ${IMG_OUTPUT}.root ${IMG_OUTPUT}.swap ${IMG_OUTPUT}.offset
}

print_help() {
	echo "Available commands:"
	echo -e "\tprepare\t\tprepare the environment, create partitions and mount root partition"
	echo -e "\tsyncbuild\tcopy root partition files from $BUILD and generate final image"
	echo -e "\tclean\t\tclean temporay files and umount root partition"
	echo -e "\tall\t\tdo prepare and syncbuild"
}

[ "$1" == "prepare" ] && prepare && build_img_partitions && mount_root
[ "$1" == "syncbuild" ] && copy_root_files && build_final_img
[ "$1" == "clean" ] && clean
[ "$1" == "all" ] && prepare && build_img_partitions && mount_root && copy_root_files && build_final_img && clean
[ -z "$1" ] && print_help


