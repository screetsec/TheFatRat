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
echo "[ ! ] Installing zenity from your apt sources   ]"
xterm -T "☣ INSTALL ZENITY ☣" -geometry 100x30 -e "sudo apt-get install zenity -y"
fi

# check if gcc exists
which gcc > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] gcc compiler......................[ found ]"
sleep 2
else
echo "[ X ] gcc compiler      -> not found            ]"
echo "[ ! ] Download compiler -> apt-get install gcc  ]"
xterm -T "☣ INSTALL GCC COMPILLER ☣" -geometry 100x30 -e "sudo apt-get install gcc -y"
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
xterm -T "☣ INSTALL MINGW32 COMPILLER ☣" -geometry 100x30 -e "sudo apt-get install mingw32 -y"
echo "[ ✔ ] Done installing .... "
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
xterm -T "☣ INSTALL MINGW32 COMPILLER ☣" -geometry 100x30 -e "sudo apt-get install monodevelop -y"
echo "[ ✔ ] Done installing ...."
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
xterm -T "☣ INSTALL MINGW32 COMPILLER ☣" -geometry 100x30 -e "sudo apt-get install ruby -y"
echo "[ ✔ ] Done installing ...."
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
xterm -T "☣ INSTALL MINGW32 COMPILLER ☣" -geometry 100x30 -e "sudo apt-get install apache2 -y"
echo "[ ✔ ] Done installing ...."
sleep 2
fi

#################################
#inputrepo
#################################

cp /etc/apt/sources.list /etc/apt/sources.list.backup # backup
rm -f /etc/apt/sources.list
touch /etc/apt/sources.list
echo 'deb http://old.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb-src http://old.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb http://http.kali.org/kali kali-rolling main contrib non-free' >> /etc/apt/sources.list
echo 'deb-src http://http.kali.org/kali kali-rolling main contrib non-free' >> /etc/apt/sources.list
sleep 2

# check if msfconsole its installed
which msfconsole > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] msfconsole........................[ found ]"
rm -f config.path
touch config.path
echo "********************************************************************************************************" >> config.path
echo "** Configuration Paths for TheFatRat , do not delete anything from this file or program will not work **" >> config.path
echo "**       if you need to reconfig your tools path , then run ./setup.sh in (TheFatRat directory) .     **" >> config.path
echo "********************************************************************************************************" >> config.path
echo "msfconsole" >> config.path
echo "msfvenom" >> config.path
sleep 2
else
echo ""
echo "[ X ] msfconsole -> not found                   ]"
echo -e $yellow "[This script requires msfconsole , do you want to setup its path manually ?]";
read -p "Press Y/y to config metasploit paths for (msfconsole & msfvenom) or N/n to install it from Kali repositories. :" choice
case "$choice" in

  y|Y)
rm -f config.path
touch config.path
echo "********************************************************************************************************" >> config.path
echo "** Configuration Paths for TheFatRat , do not delete anything from this file or program will not work **" >> config.path
echo "**       if you need to reconfig your tools path , then run ./setup.sh in (TheFatRat directory) .     **" >> config.path
echo "********************************************************************************************************" >> config.path
echo -e $yellow "Enter the path for msfconsole ex:(/opt/metasploit-framework/msfconsole) or just press [ENTER] for default config : ";
read -p "Path:" msfc
if [[ -z "$msfc" ]]; then
echo "msfconsole" >> config.path
else
echo "ruby $msfc" >> config.path
fi
echo -e $green "Enter the path for msfvenom ex:(/opt/metasploit-framework/msfvenom) or just press [ENTER] for default config : ";
echo "Path:"
read msfv
if [[ -z "$msfv" ]]; then 
echo "msfvenom" >> config.path
else
echo "ruby $msfv" >> config.path
fi
;;

 n|N) xterm -T "☣ UPDATE YOUR REPO ☣" -geometry 100x30 -e "sudo apt-get update "
xterm -T "☣ INSTALL Metasploit-Framework" -geometry 100x30 -e "sudo apt-get install metasploit-framework -y"
echo "[ ✔ ] Done installing ...."
rm -f config.path
touch config.path
echo "********************************************************************************************************" >> config.path
echo "** Configuration Paths for TheFatRat , do not delete anything from this file or program will not work **" >> config.path
echo "**       if you need to reconfig your tools path , then run ./setup.sh in (TheFatRat directory) .     **" >> config.path
echo "********************************************************************************************************" >> config.path
echo "msfconsole" >> config.path
echo "msfvenom" >> config.path
;;

*) echo "Invalid Input (Choose y/Y or n/N only)"
;;
esac ;

# check if backdoor-factory exists
which backdoor-factory > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] backdoor-factory..................[ found ]"
echo "backdoor-factory" >> config.path
sleep 2
else
echo "[ X ] backdoor-factory  -> not found            ]"
echo "[This script requires backdoor-factory , do you want to setup its path manually ?]"
read -p "[Press Y/y to setup backdoor-factory path or N/n to install it from Kali repositories .]" choice1
case "$choice1" in
  
 y|Y )
echo "Enter the path for backdoor.py ex:(/opt/backdoor-factory/backdoor.py) or just press [ENTER] for default config : "
read -p "Path:" backdoor
if [[ -z "$backdoor" ]]; then
echo "backdoor-factory" >> config.path
else
echo "python2 $backdoor" >> config.path
fi
;;

 n|N )
echo "[ ! ] Download Backdoor-Factory ........................."
xterm -T "☣ INSTALL BACKDOOR-FACTORY ☣" -geometry 100x30 -e "sudo apt-get install backdoor-factory -y"
echo "[ ✔ ] Done installing ...."
echo "backdoor-factory" >> config.path
;;

*) 
echo "Invalid Input (Choose y/Y or n/N only)"
;;
esac;
fi
sleep 2

# check if searchsploit exists
which searchsploit > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] searchsploit..................[ found ]"
echo "searchsploit" >> config.path
sleep 2
else
echo "[ X ] searchsploit  -> not found            ]"
echo "[This script requires searchsploit , do you want to setup its path manually ?]"
read -p "[Press Y/y to config searchsploit path or N/n to install it from Kali repositories .]" choice2
case "$choice2" in
  
  y|Y )
echo "Enter the path for searchsploit ex:(/opt/searchsploit/searchsploit) or (searchsploit) for default and press [ENTER]: "
read -p "Path: " searchsploit
if [[ -z "$searchsploit" ]]; then
echo "searchsploit" >> config.path
else
echo ".$searchsploit" >> config.path
fi
;;

n|N )
echo "[ ! ] Download Searchsploit ........................."
xterm -T "☣ INSTALL Searchsploit ☣" -geometry 100x30 -e "sudo apt-get install searchsploit -y"
echo "[ ✔ ] Done installing ...."
echo "searchsploit" >> config.path
sleep 2
echo ""
echo "Configuration and tool installed with success!";
sleep 2
;;

*) 
echo "Invalid Input (Choose y/Y or n/N only)"
;;
esac
fi
################################
# rebackyo repo
################################
echo "reactivating repositories"
rm -f /etc/apt/sources.list
mv /etc/apt/sources.list.backup /etc/apt/sources.list
apt-get clean
xterm -T "☣ UPDATE YOUR REPO ☣" -geometry 100x30 -e "sudo apt-get update "
clear
echo "Do you want to create a shortcut for (fatrat) on your (/usr/local/sbin) , so you can run the script from anywhere ?"
read -p "Press y/Y to create the script , or press n/N to cancel : " choice4
case "$choice4" in

  y|Y)

dir=`pwd` 
scrp="cd $dir && ./fatrat"
rm -f /usr/local/sbin/fatrat
touch /usr/local/sbin/fatrat
echo "#!/bin/bash" > /usr/local/sbin/fatrat
echo $scrp >> /usr/local/sbin/fatrat
chmod +x /usr/local/sbin/fatrat
clear
echo "";
  echo "[ ]====================================================================[ ]";
  echo "[ ] Script Created!! Write: fatrat , on your terminal anywhere   :) !  [ ]";
  echo "[ ]====================================================================[ ]";
  echo "";
  sleep 2 
;;

 n|N)
echo "[ ]=================================================================[ ]";
echo "[ ]              To execute Fatrat , write ./fatrat                 [ ]";
echo "[ ]=================================================================[ ]";
chmod +x fatrat
;;

*)
echo "[ ]=================================================================[ ]";
echo "[ ]              To execute Fatrat , write ./fatrat                 [ ]";
echo "[ ]=================================================================[ ]";
chmod +x fatrat
;;
esac
fi 
