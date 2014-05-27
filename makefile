config:
	sudo apt-get install xsel genius zenity espeak goldendict
install: build
	sudo gdebi --non-interactive dothis_UNSTABLE.deb
uninstall :
	sudo rm -v /usr/bin/calcthis
	sudo rm -v /usr/bin/speakthis
	sudo rm -v /usr/bin/definethis
build: 
	sudo make build-deb;
build-deb:
	mkdir -p debian
	mkdir -p debian/DEBIAN
	mkdir -p debian/usr
	mkdir -p debian/usr/bin
	# copy over program files
	cp speakthis.py ./debian/usr/bin/speakthis
	cp calcthis.py ./debian/usr/bin/calcthis
	cp definethis.py ./debian/usr/bin/definethis
	chmod +x ./debian/usr/bin/calcthis
	chmod +x ./debian/usr/bin/speakthis
	chmod +x ./debian/usr/bin/definethis
	# Create the md5sums file
	find ./debian/ -type f -print0 | xargs -0 md5sum > ./debian/DEBIAN/md5sums
	# cut filenames of extra junk
	sed -i.bak 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	sed -i.bak 's/\\n*DEBIAN*\\n//g' ./debian/DEBIAN/md5sums
	sed -i.bak 's/\\n*DEBIAN*//g' ./debian/DEBIAN/md5sums
	rm -v ./debian/DEBIAN/md5sums.bak
	# figure out the package size	
	du -sx --exclude DEBIAN ./debian/ > Installed-Size.txt
	# copy over package data
	cp -rv debdata/. debian/DEBIAN/
	# fix permissions in package
	chmod -Rv 775 debian/DEBIAN/
	chmod -Rv ugo+r debian/
	chmod -Rv go-w debian/
	chmod -Rv u+w debian/
	# build the package
	dpkg-deb --build debian
	cp -v debian.deb dothis_UNSTABLE.deb
	rm -v debian.deb
	rm -rv debian
