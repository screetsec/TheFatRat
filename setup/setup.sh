#!/bin/bash

# setup.sh Author : Edo maland ( Screetsec )
# Install all dependencies nedded
# configuration all file for fixing all problem
# --------------------------------------------------------

#Check root dulu
[[ `id -u` -eq 0 ]] || { echo -e "\e[31mMust be root to run script"; exit 1; }
resize -s 30 73 > /dev/null
clear


#This colour
cyan='\e[0;36m'
green='\e[0;34m'
okegreen='\033[92m'
lightgreen='\e[1;32m'
white='\e[1;37m'
red='\e[1;31m'
yellow='\e[1;33m'
BlueF='\e[1;34m'
path=`pwd`

#Banner dong biar keren
echo -e $cyan ""
echo "         [ ]=================================================[ ]";
echo "         [ ]    ________       ____     __  ___       __     [ ]";
echo "         [ ]     /_  __/ /  ___ / __/__ _/ /_/ _ \___ _/ /_  [ ]";
echo "         [ ]     / / / _ \/ -_) _// _ \`/ __/ , _/ _ \`/ __/   [ ]";
echo "         [ ]     /_/ /_//_/\__/_/  \_,_/\__/_/|_|\_,_/\__/   [ ]";
echo "         [ ]=================================================[ ] ";
echo "         [ ]          Setup.sh - configuration script        [ ]"
echo "         [ ]        Use this script to configure fatrat      [ ]"
echo "         [ ]              Install all dependencies           [ ]"
echo "         [ ]=================================================[ ]";
echo ""

# check if msfconsole its installed
which msfconsole > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] msfconsole........................[ found ]"
sleep 2
else
echo ""
echo "[ X ] msfconsole -> not found                   ]"
echo "[ ! ] This script requires msfconsole           ]"
sleep 2
exit
fi

# check if msfvenom
which msfvenom > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] msfvenom..........................[ found ]"
sleep 2
else
echo ""
echo "[ X ] msfvenom -> not found                   ]"
echo "[ ! ] This script requires msfvenom too        ]"
sleep 2
exit
fi

#check if zenity its installed
which zenity > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] zenity............................[ found ]"
sleep 2
else
echo ""
echo "[ X ] zenity -> not found!                      ]"
echo "[ ! ] This script requires zenity               ]"
sleep 2
echo "[ ? ] Please download zenity                    ]"
su $user -c "xdg-open http://www.tecmint.com/zenity-creates-graphical-gtk-dialog-boxes-in-command-line-and-shell-scripts/" > /dev/null 2>&1
fi

# check if gcc exists
which gcc > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] gcc compiler......................[ found ]"
sleep 2
else
echo "[ X ] gcc compiler      -> not found            ]"
echo "[ ! ] Download compiler -> apt-get install gcc  ]"
xterm -T "☣ INSTALL GCC COMPILLER ☣" -geometry 100x30 -e "sudo apt-get install gcc"
sleep 2
fi





# check if mingw32 exists
which i586-mingw32msvc-gcc > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] mingw32 compiler..................[ found ]"
sleep 2
else
echo "[ X ] mingw32 compiler  -> not found            ]"
echo "[ ! ] Download compiler ........................."
echo "[ ! ] Create backup your sources.list for packages kali sana ( temporary )"
cd /etc/apt && cp sources.list sources.list.backup
rm /etc/apt/sources.list
echo 'deb http://old.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb http://http.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb-src http://http.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb http://repo.kali.org/kali kali-rolling main non-free contrib' >> /etc/apt/sources.list
echo 'deb-src http://repo.kali.org/kali kali-rolling main non-free contrib' >> /etc/apt/sources.list
xterm -T "☣ INSTALL MINGW32 COMPILLER ☣" -geometry 100x30 -e "sudo apt-get update && apt-get install mingw32 -y"
echo "[ ✔ ] Done installing,now wait for rebackup your sources.list & update packages"
rm /etc/apt/sources.list
mv /etc/apt/sources.list.backup sources.list && cd $path
xterm -T "☣ UPDATE YOUR REPO ☣" -geometry 100x30 -e "sudo apt-get update "
sleep 2
fi

# check if backdoor-factory exists
which backdoor-factory > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] backdoor-factory..................[ found ]"
sleep 2
else
echo "[ X ] backdoor-factory  -> not found            ]"
echo "[ ! ] Download compiler ........................."
echo "[ ! ] Create backup your sources.list for packages kali sana ( temporary )"
cd /etc/apt && cp sources.list sources.list.backup
rm sources.list
echo 'deb http://old.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb http://http.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb-src http://http.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb http://repo.kali.org/kali kali-rolling main non-free contrib' >> /etc/apt/sources.list
echo 'deb-src http://repo.kali.org/kali kali-rolling main non-free contrib' >> /etc/apt/sources.list
xterm -T "☣ INSTALL BACKDOOR-FACTORY ☣" -geometry 100x30 -e "sudo apt-get update && apt-get install backdoor-factory -y"
echo "[ ✔ ] Done installing,now wait for rebackup your sources.list & update packages"
rm sources.list
mv sources.list.backup sources.list && cd $path
xterm -T "☣ UPDATE YOUR REPO ☣" -geometry 100x30 -e "sudo apt-get update "
sleep 2
fi


# check if monodevelop exists
which monodevelop > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] monodevelop ......................[ found ]"
sleep 2
else
echo "[ X ] Monodevelop  -> not found            ]"
echo "[ ! ] Download Monodevelop ........................."
echo "[ ! ] Create backup your sources.list for packages kali sana ( temporary )"
cd /etc/apt && cp sources.list sources.list.backup
rm sources.list
echo 'deb http://old.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb http://http.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb-src http://http.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb http://repo.kali.org/kali kali-rolling main non-free contrib' >> /etc/apt/sources.list
echo 'deb-src http://repo.kali.org/kali kali-rolling main non-free contrib' >> /etc/apt/sources.list
xterm -T "☣ INSTALL MINGW32 COMPILLER ☣" -geometry 100x30 -e "sudo apt-get update && apt-get install monodevelop -y"
echo "[ ✔ ] Done installing,now wait for rebackup your sources.list & update packages"
rm sources.list
mv sources.list.backup sources.list && cd $path
xterm -T "☣ UPDATE YOUR REPO ☣" -geometry 100x30 -e "sudo apt-get update "
sleep 2
fi

# check if ruby exists
which ruby > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Ruby .............................[ found ]"
sleep 2
else
echo "[ X ] ruby  -> not found            ]"
echo "[ ! ] Download ruby ........................."
echo "[ ! ] Create backup your sources.list for packages kali sana ( temporary )"
cd /etc/apt && cp sources.list sources.list.backup
rm sources.list
echo 'deb http://old.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb http://http.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb-src http://http.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb http://repo.kali.org/kali kali-rolling main non-free contrib' >> /etc/apt/sources.list
echo 'deb-src http://repo.kali.org/kali kali-rolling main non-free contrib' >> /etc/apt/sources.list
xterm -T "☣ INSTALL MINGW32 COMPILLER ☣" -geometry 100x30 -e "sudo apt-get update && apt-get install ruby -y"
echo "[ ✔ ] Done installing,now wait for rebackup your sources.list & update packages"
rm sources.list
mv sources.list.backup sources.list && cd $path
xterm -T "☣ UPDATE YOUR REPO ☣" -geometry 100x30 -e "sudo apt-get update "
sleep 2
fi

#check if apache2 exists
which apache2 > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] apache2 ..........................[ found ]"
sleep 2
else
echo "[ X ] ruby  -> not found            ]"
echo "[ ! ] Download apache2 ........................."
echo "[ ! ] Create backup your sources.list for packages kali sana ( temporary )"
cd /etc/apt && cp sources.list sources.list.backup
rm sources.list
echo 'deb http://old.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb http://http.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb-src http://http.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb http://repo.kali.org/kali kali-rolling main non-free contrib' >> /etc/apt/sources.list
echo 'deb-src http://repo.kali.org/kali kali-rolling main non-free contrib' >> /etc/apt/sources.list
xterm -T "☣ INSTALL MINGW32 COMPILLER ☣" -geometry 100x30 -e "sudo apt-get update && apt-get install apache2 -y"
echo "[ ✔ ] Done installing,now wait for rebackup your sources.list & update packages"
rm sources.list
mv sources.list.backup sources.list && cd $path
xterm -T "☣ UPDATE YOUR REPO ☣" -geometry 100x30 -e "sudo apt-get update "
sleep 2
fi
echo ""
echo "Configuration and tool installed with success!";
sleep 2

clear
echo "";
  echo "[ ]====================================================================[ ]";
  echo "[ ]           All is done!! You can execute TheFatRat :) !             [ ]";
  echo "[ ]====================================================================[ ]";
  echo "";
  sleep 2
  exit
