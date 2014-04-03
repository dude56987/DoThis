config:
	sudo apt-get install xsel genius zenity espeak goldendict
install:
	pycompile speakthis.py
	pycompile calcthis.py
	pycompile definethis.py
	cp speakthis.pyc speakthis
	cp calcthis.pyc calcthis
	cp definethis.pyc definethis
	chmod +x calcthis
	chmod +x speakthis
	chmod +x definethis
	cp -v calcthis /usr/bin/calcthis
	cp -v speakthis /usr/bin/speakthis
	cp -v definethis /usr/bin/definethis
	rm -v calcthis.pyc calcthis
	rm -v speakthis.pyc speakthis
	rm -v definethis.pyc definethis
	speakthis -S
	calcthis -S
	definethis -S
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
	cp speakthis.py ./debian/usr/bin/speakthis
	cp calcthis.py ./debian/usr/bin/calcthis
	cp definethis.py ./debian/usr/bin/definethis
	chmod +x ./debian/usr/bin/calcthis
	chmod +x ./debian/usr/bin/speakthis
	chmod +x ./debian/usr/bin/definethis
	md5sum ./debian/usr/bin/calcthis > ./debian/DEBIAN/md5sums
	md5sum ./debian/usr/bin/speakthis >> ./debian/DEBIAN/md5sums
	md5sum ./debian/usr/bin/definethis >> ./debian/DEBIAN/md5sums
	sed -i.bak 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	rm -v ./debian/DEBIAN/md5sums.bak
	cp -rv debdata/. debian/DEBIAN/
	dpkg-deb --build debian
	cp -v debian.deb dothis.deb
	rm -v debian.deb
	rm -rv debian
clean:
	rm -v calcthis.pyc calcthis
	rm -v speakthis.pyc speakthis
	rm -v definethis.pyc definethis