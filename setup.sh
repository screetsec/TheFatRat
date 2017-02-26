#!/bin/bash
#Fail safe for original user sources.list in case setup was interrupted in middle last time
file="/etc/apt/sources.list.fatrat"
if [ -f "$file" ]
then
echo "Setup Detected that your previous run was interrupted in middle , fixing your original repositories list ."
sleep 4s
rm -f /etc/apt/sources.list
mv /etc/apt/sources.list.fatrat /etc/apt/sources.list
echo "Your Original repository list was recovered. ;) ..... beginning setup"
echo ""
echo "Cleaning previous repositories cache & updating your repository ."
sudo apt-get clean && apt-get update -y
sleep 3s
else
echo ""
fi 
path=`pwd`
log=$path/logs/setup.log
config=$path/config/config.path

#Removing any previous setup log created
rm -f $log 
# setup.sh Author : Edo maland ( Screetsec )
# Install all dependencies nedded
# configuration all file for fixing all problem
# --------------------------------------------------------

#Check root dulu
[[ `id -u` -eq 0 ]] || { echo -e "\e[31m Must be root to run script"; exit 1; }
resize -s 30 73 > /dev/null 2>&1
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
touch $log
echo "------------------------------------------------------" >> $log
echo "| Tools paths configured in (setup.sh) for TheFatRat |" >> $log
echo "------------------------------------------------------" >> $log
echo "                                                      " >> $log
#check if xterm is installed
which xterm > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Xterm.............................[ found ]"
which xterm >> $log 2>&1
sleep 2
else
echo ""
echo "[ X ] xterm -> not found!                        ]"
echo "[ ! ] This script requires xterm                 ]"
sleep 2
sudo apt-get install xterm -y
clear
echo "[ ✔ ] Done installing .... "
which xterm >> $log 2>&1
fi

#check if zenity its installed
which zenity > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Zenity............................[ found ]"
which zenity >> $log 2>&1
sleep 2
else
echo ""
echo "[ X ] zenity -> not found!                       ]"
echo "[ ! ]  This script requires zenity               ]"
sleep 2
echo "[ ! ]  Installing zenity from your apt sources   ]"
xterm -T "☣ INSTALL ZENITY ☣" -geometry 100x30 -e "sudo apt-get install zenity -y"
echo "[ ✔ ] Done installing .... "
which zenity >> $log 2>&1
fi

# check if gcc exists
which gcc > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Gcc compiler......................[ found ]"
which gcc >> $log 2>&1
sleep 2
else
echo "[ X ] gcc compiler      -> not found              ]"
echo "[ ! ]   Installing gcc from your apt sources      ]"
xterm -T "☣ INSTALL GCC COMPILLER ☣" -geometry 100x30 -e "sudo apt-get install gcc -y"
echo "[ ✔ ] Done installing .... "
which gcc >> $log 2>&1
sleep 2
fi

# check if mingw32 exists
which i586-mingw32msvc-gcc > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Mingw32 Compiler..................[ found ]"
which i586-mingw32msvc-gcc >> $log 2>&1
sleep 2
else
echo "[ X ] mingw32 compiler  -> not found               ]"
echo "[ ! ]   Installing zenity from your apt sources    ]"
xterm -T "☣ INSTALL MINGW32 COMPILLER ☣" -geometry 100x30 -e "sudo apt-get install mingw32 -y"
echo "[ ✔ ] Done installing .... "
which i586-mingw32msvc-gcc >> $log 2>&1
sleep 2
fi

# check if monodevelop exists
which monodevelop > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Monodevelop ......................[ found ]"
which monodevelop >> $log 2>&1
sleep 2
else
echo "[ X ] Monodevelop  -> not found                     ]"
echo "[ ! ]  Installing monodevelop from your apt sources ]"
xterm -T "☣ INSTALL MONODEVELOP ☣" -geometry 100x30 -e "sudo apt-get install monodevelop -y"
echo "[ ✔ ] Done installing ...."
which monodevelop >> $log 2>&1
sleep 2
fi

# check if ruby exists
which ruby > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Ruby .............................[ found ]"
which ruby >> $log 2>&1
sleep 2
else
echo "[ X ] Ruby  -> not found                             ]"
echo "[ ! ]     Installing ruby from your apt sources      ]"
xterm -T "☣ INSTALL RUBY ☣" -geometry 100x30 -e "sudo apt-get install ruby -y"
echo "[ ✔ ] Done installing ...."
which ruby >> $log 2>&1
sleep 2
fi

#check if apache2 exists
which apache2 > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Apache2 ..........................[ found ]"
which apache2 >> $log 2>&1
sleep 2
else
echo "[ X ] Apache2 -> not found                            ]"
echo "[ ! ]    Installing apache2 from your apt sources     ]"
xterm -T "☣ INSTALL APACHE2 ☣" -geometry 100x30 -e "sudo apt-get install apache2 -y"
echo "[ ✔ ] Done installing ...."
which apache2 >> $log 2>&1
sleep 2
fi

#check if gnome terminal exists
#added this new install option because user may be running a distro that may not have gnome terminal installed by default
#gnome terminal is used in main script to run searchsploit
which gnome-terminal > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Gnome Terminal....................[ found ]"
which gnome-terminal >> $log 2>&1
sleep 2
else
echo "[ X ] Gnome-terminal-> not found                      ]"
echo "[ ! ] Installing gnome-terminal from your apt sources ]"
xterm -T "☣ INSTALL GNOME-TERMINAL ☣" -geometry 100x30 -e "sudo apt-get install gnome-terminal -y"
echo "[ ✔ ] Done installing ...."
which gnome-terminal >> $log 2>&1
sleep 2
fi

#Checking if upx compressor exists
which upx > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] UPX Compressor....................[ found ]"
which upx >> $log 2>&1
sleep 2
else
echo "[ X ] Upx compressor  -> not found                    ]"
echo "[ ! ] Installing upx-compressor from your apt sources ]"
xterm -T "☣ INSTALL UPX COMPRESSOR ☣" -geometry 100x30 -e "sudo apt-get install upx-ucl -y"
echo "[ ✔ ] Done installing ...."
which upx >> $log 2>&1
sleep 2
fi

#Checking if keytool exists
which keytool > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Keytool (java)....................[ found ]"
which keytool >> $log 2>&1
sleep 2
else
echo "[ X ] Keytool (java) -> not found                    ]"
echo "[ ! ] Installing Java from your apt sources ]"
xterm -T "☣ INSTALL JAVA ☣" -geometry 100x30 -e "sudo apt-get install default-jre default-jdk -y "
echo "[ ✔ ] Done installing ...."
which keytool >> $log 2>&1
sleep 2
fi

#Checking if Jarsigner exists
which jarsigner > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Jarsigner (java)..................[ found ]"
which jarsigner >> $log 2>&1
sleep 2
else
echo "[ X ] Jarsigner (java) -> not found                    ]"
echo "[ ! ] Installing Java from your apt sources ]"
xterm -T "☣ INSTALL JAVA ☣" -geometry 100x30 -e "sudo apt-get install default-jdk -y "
echo "[ ✔ ] Done installing ...."
which jarsigner >> $log 2>&1
sleep 2
fi

#Checking if Unzip exists
which unzip > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Unzip.............................[ found ]"
which unzip >> $log 2>&1
sleep 2
else
echo "[ X ] Unzip -> not found                    ]"
echo "[ ! ] Installing Unzip from your apt sources ]"
xterm -T "☣ INSTALL UNZIP ☣" -geometry 100x30 -e "sudo apt-get install unzip -y "
echo "[ ✔ ] Done installing ...."
which unzip >> $log 2>&1
sleep 2
fi

#Checking if Aapt exists
which aapt > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Aapt..............................[ found ]"
which aapt >> $log 2>&1
sleep 2
else
echo "[ X ] Aapt -> not found                    ]"
echo "[ ! ] Installing Aapt from your apt sources ]"
xterm -T "☣ INSTALL AAPT ☣" -geometry 100x30 -e "sudo apt-get install aapt -y "
echo "[ ✔ ] Done installing ...."
which aapt >> $log 2>&1
sleep 2
fi

#Installing dependencies for Zipalign
echo "[ ! ] Installing Zipalign & Android-sdk dependencies from your apt sources"
xterm -T "☣ INSTALL ZIPALING & ANDROID-SDK DEPENDENCIES ☣" -geometry 100x30 -e "sudo apt-get install lib32stdc++6 lib32z1 lib32z1-dev -y "
echo "[ ✔ ] Done installing ...."
sleep 2

#Checking if Zipalign exists
which zipalign > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Zipalign..........................[ found ]"
which zipalign >> $log 2>&1
sleep 2
else
echo "[ X ] Zipalign -> not found                    ]"
echo "[ ! ] Installing Zipalign from your apt sources "
xterm -T "☣ INSTALL ZIPALIGN ☣" -geometry 100x30 -e "sudo apt-get install zipalign -y "
echo "[ ✔ ] Done installing ...."
which zipalign >> $log 2>&1
sleep 2
fi

#################################
#inputrepo
#################################

cp /etc/apt/sources.list /etc/apt/sources.list.backup # backup
# Second backup created in case user stops the script after this point , then on next startup this script will
# copy the already changed sources file before as backup , and user lost his original sources lists
file="/etc/apt/sources.list.fatrat"
if [ -f "$file" ]
then
echo ""
else
cp /etc/apt/sources.list /etc/apt/sources.list.fatrat
fi
rm -f /etc/apt/sources.list
touch /etc/apt/sources.list
echo 'deb http://old.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb-src http://old.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list
echo 'deb http://http.kali.org/kali kali-rolling main contrib non-free' >> /etc/apt/sources.list
echo 'deb-src http://http.kali.org/kali kali-rolling main contrib non-free' >> /etc/apt/sources.list
sleep 2
xterm -T "☣ UPDATING KALI REPO ☣" -geometry 100x30 -e "sudo apt-get update" >>$log 2>&1

#Checking if apktool exists
which apktool > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Apktool...........................[ found ]"
which apktool >> $log 2>&1
sleep 2
else
echo "[ X ] Apktool  -> not found                     "
echo "[ ! ] Installing apktool from Kali repositories "
xterm -T "☣ INSTALL APKTOOOL ☣" -geometry 100x30 -e "sudo apt-get install apktool --force-yes -y"
echo "[ ✔ ] Done installing ...."
which apktool >> $log 2>&1
sleep 2
fi

#Checking if dex2jar exists
which d2j-jar2dex > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Dex2Jar...........................[ found ]"
which d2j-jar2dex >> $log 2>&1
sleep 2
else
echo "[ X ] Dex2jar  -> not found                     "
echo "[ ! ] Installing dex2jar from Kali repositories "
xterm -T "☣ INSTALL APKTOOOL ☣" -geometry 100x30 -e "sudo apt-get install dex2jar --force-yes -y"
echo "[ ✔ ] Done installing ...."
which d2j-jar2dex >> $log 2>&1
sleep 2
fi

#installing dependencies for ruby script
echo "[ ! ] Installing dedepndencies for ruby script from Kali repositories "
xterm -T "☣ INSTALL DEPENDENCIES ☣" -geometry 100x30 -e "sudo apt-get install zlib1g-dev libmagickwand-dev imagemagick  -y"
echo "[ ✔ ] Done installing ...."
sleep 2

# check if metasploit-framework its installed
which msfconsole > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Metasploit-Framework..............[ found ]"
# msf was detected , removing config file in case setup was already configured before
rm -f $config

#Creating new config file based on last detection of msf
touch $config
echo "********************************************************************************************************" >> $config
echo "** Configuration Paths for TheFatRat , do not delete anything from this file or program will not work **" >> $config
echo "**       if you need to reconfig your tools path , then run ./setup.sh in (TheFatRat directory) .     **" >> $config
echo "********************************************************************************************************" >> $config
echo "msfconsole" | tee -a $config $log > /dev/null 2>&1
echo "msfvenom" | tee -a $config $log > /dev/null 2>&1
sleep 2
else
echo ""
echo "[ X ] metasploit-framework -> not found                         "

# Providing manual input to user in case metasploit was installed from git and is not on system path
echo ""
echo -e $white "This script requires Metasploit-Framework do you want to setup its path manually ?";
echo ""
read -p "Press Y/y to config metasploit-framework path or N/n to install it from Kali repositories. :" choice
case "$choice" in

  y|Y)
rm -f $config
touch $config
echo "********************************************************************************************************" >> $config
echo "** Configuration Paths for TheFatRat , do not delete anything from this file or program will not work **" >> $config
echo "**       if you need to reconfig your tools path , then run ./setup.sh in (TheFatRat directory) .     **" >> $config
echo "********************************************************************************************************" >> $config
clear
echo -e $white "Enter the path of your Metasploit Instalation or just press enter for default config :
ex:(/opt/metasploit-framework)";
read -p "Path: " msfc
if [[ -z "$msfc" ]]; then
echo "msfconsole" | tee -a $config $log > /dev/null 2>&1
echo "msfvenom" | tee -a $config $log > /dev/null 2>&1
else
echo "ruby $msfc/msfconsole" | tee -a $config $log > /dev/null 2>&1
echo "ruby $msfc/msfvenom" | tee -a $config $log > /dev/null 2>&1
fi
;;

 n|N) 
echo "[ ! ] Installing metasploit-framework from kali repositories "
xterm -T "☣ INSTALL METASPLOIT-FRAMEWORK ☣" -geometry 100x30 -e "sudo apt-get install metasploit-framework --force-yes -y"
echo "[ ✔ ] Done installing ...."
rm -f $config
touch $config
echo "********************************************************************************************************" >> $config
echo "** Configuration Paths for TheFatRat , do not delete anything from this file or program will not work **" >> $config
echo "**       if you need to reconfig your tools path , then run ./setup.sh in (TheFatRat directory) .     **" >> $config
echo "********************************************************************************************************" >> $config

# adding the msf startups automatically to config file
echo "msfconsole" | tee -a $config $log > /dev/null 2>&1
echo "msfvenom" | tee -a $config $log > /dev/null 2>&1
;;

 *)
 echo "Invalid Input (Choose y/Y or n/N only)"
;;
esac;
fi

# check if backdoor-factory exists
which backdoor-factory > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Backdoor-Factory..................[ found ]"
echo "backdoor-factory" | tee -a $config $log > /dev/null 2>&1
sleep 2
else
echo "[ X ] backdoor-factory  -> not found                  "
echo ""
echo -e $white "[This script requires backdoor-factory , do you want to setup its path manually ?]";
read -p "[Press Y/y to setup backdoor-factory path or N/n to install it from Kali repositories . ]" choice1
case "$choice1" in
  
 y|Y )
 clear
echo -e $white "Enter the path for backdoor.py , or just press [ENTER] for default config : 
ex:(/opt/backdoor-factory/backdoor.py)";
read -p "Path: " backdoor
if [[ -z "$backdoor" ]]; then
echo "backdoor-factory" | tee -a $config $log > /dev/null 2>&1
else
echo "python2 $backdoor" | tee -a $config $log > /dev/null 2>&1
fi
;;

 n|N )
echo "[ ! ]   Installing backdoor-factory from kali repositories   ]"
xterm -T "☣ INSTALL BACKDOOR-FACTORY ☣" -geometry 100x30 -e "sudo apt-get install backdoor-factory --force-yes -y"
echo "[ ✔ ] Done installing ...."
echo "backdoor-factory" | tee -a $config $log > /dev/null 2>&1
;;

*) 
echo "Invalid Input (Choose y/Y or n/N only)"
;;
esac;
fi

# check if searchsploit exists
which searchsploit > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo "[ ✔ ] Searchsploit......................[ found ]"
echo "searchsploit" | tee -a $config $log > /dev/null 2>&1
sleep 2
else
echo "[ X ] searchsploit  -> not found]"
echo ""
echo -e $white "[This script requires searchsploit , do you want to setup its path manually ?]";
read -p "[Press Y/y to config searchsploit path or N/n to install it from Kali repositories .]" choice2
case "$choice2" in
  
  y|Y )
  clear
echo -e $white "Enter the path for searchsploit , or just press [ENTER] for default config : 
ex:(/opt/searchsploit/searchsploit) "
read -p "Path: " searchsploit
if [[ -z "$searchsploit" ]]; then
echo "searchsploit" | tee -a $config $log > /dev/null 2>&1
else
echo "bash $searchsploit" | tee -a $config $log > /dev/null 2>&1
fi
;;

n|N )
echo "[ ! ]    Installing searchsploit from kali repositories      ]"
xterm -T "☣ INSTALL SEARCHSPLOIT ☣" -geometry 100x30 -e "sudo apt-get install exploitdb --force-yes -y"
echo "[ ✔ ] Done installing ...."
echo "searchsploit" | tee -a $config $log > /dev/null 2>&1
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
echo "Reactivating you original repositories"
rm -f /etc/apt/sources.list
mv /etc/apt/sources.list.backup /etc/apt/sources.list
#now we can remove the emergency backup securely
rm -f /etc/apt/sources.list.fatrat
apt-get clean
xterm -T "☣ UPDATE YOUR REPO ☣" -geometry 100x30 -e "sudo apt-get update "
clear
echo -e $yellow "Do you want to create a shortcut for (fatrat) on your (/usr/local/sbin) 
, so you can run the script from anywhere ?";
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
  chmod +x fatrat
  which fatrat >> $log 2>&1
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
