#!bin/bash

if [ 'whoami' != root ]
then
	echo "Please run this script as root."
	exit
fi

if [ -d "/etc/passwdman" ]
then
	echo ""
else
	mkdir /etc/passwdman
fi

cd /etc/passwdman

touch profile.txt
touch info.txt

echo "passwdman" > profile.txt

chmod ugo=r+w profile.txt
chmod ugo=r+w info.txt
