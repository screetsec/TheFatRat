#!/bin/bash

# setup.sh Original Author : Edo maland ( Screetsec )
# Script rebuilded by peterpt
# Install all dependencies nedded
# configuration all file for fixing all problems
# --------------------------------------------------------


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
rm -f $log > /dev/null 2>&1

#This colour
cyan='\e[0;36m'
green='\e[0;32m'
lightgreen='\e[1;32m'
white='\e[1;37m'
red='\e[1;31m'
yellow='\e[1;33m'
blue='\e[1;34m'
path=`pwd`

#Check root dulu
[[ `id -u` -eq 0 ]] || { echo -e $red "Must be root to run script"; exit 1; }
resize -s 80 103 > /dev/null 2>&1
clear

#Banner dong biar keren
echo -e $green ""
echo "___________         __  __________          __    "
echo "\_   _____/_____  _/  |_\______   \_____  _/  |_  "
echo " |    __)  \__  \ \   __\|       _/\__  \ \   __\ "
echo " |     \    / __ \_|  |  |    |   \ / __ \_|  |   "
echo " \___  /   (____  /|__|  |____|_  /(____  /|__|   "
echo "     \/         \/              \/      \/        "
echo "                 ____    ________                 "
echo "                /_   |  /   __   \                "
echo "                 |   |  \____    /                "
echo "                 |   |     /    /                 "
echo "                 |___| /\ /____/                  "
echo "                       \/                         "
echo ""
echo -e $blue "         Setup Script for FATRAT 1.9       "
touch $log
echo "------------------------------------------------------" >> $log
echo "| Tools paths configured in (setup.sh) for TheFatRat |" >> $log
echo "------------------------------------------------------" >> $log
echo "                                                      " >> $log
#check if xterm is installed
which xterm > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Xterm.............................[ found ]"
which xterm >> $log 2>&1
sleep 2
else
echo ""
echo -e $red "[ X ] xterm -> not found! "
sleep 2
echo -e $yellow "[ ! ] Installing Xterm                     "
sleep 2
echo -e $green ""
sudo apt-get install xterm -y
clear
echo -e $green "[ ✔ ] Done installing .... "
which xterm >> $log 2>&1
fi

#check if zenity its installed
which zenity > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Zenity............................[ found ]"
which zenity >> $log 2>&1
sleep 2
else
echo ""
echo -e $red "[ X ] zenity -> not found! "
sleep 2
echo -e $yellow "[ ! ]  Installing zenity                   "
xterm -T "☣ INSTALL ZENITY ☣" -geometry 100x30 -e "sudo apt-get install zenity -y"
echo -e $green "[ ✔ ] Done installing .... "
which zenity >> $log 2>&1
fi

# check if gcc exists
which gcc > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Gcc compiler......................[ found ]"
which gcc >> $log 2>&1
sleep 2
else
echo -e $red "[ X ] gcc compiler      -> not found "
echo -e $yellow "[ ! ]   Installing gcc "
xterm -T "☣ INSTALL GCC COMPILLER ☣" -geometry 100x30 -e "sudo apt-get install gcc -y"
echo -e $green "[ ✔ ] Done installing .... "
which gcc >> $log 2>&1
sleep 2
fi

# check if mingw32 exists
which i586-mingw32msvc-gcc > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Mingw32 Compiler..................[ found ]"
which i586-mingw32msvc-gcc >> $log 2>&1
sleep 2
else
echo -e $red "[ X ] mingw32 compiler  -> not found "
echo -e $yellow "[ ! ]   Installing Mingw32 "
xterm -T "☣ INSTALL MINGW32 COMPILLER ☣" -geometry 100x30 -e "sudo apt-get install mingw32 -y"
echo -e $green "[ ✔ ] Done installing .... "
which i586-mingw32msvc-gcc >> $log 2>&1
sleep 2
fi

# check if monodevelop exists
which monodevelop > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Monodevelop ......................[ found ]"
which monodevelop >> $log 2>&1
sleep 2
else
echo -e $red "[ X ] Monodevelop  -> not found "
echo -e $yellow "[ ! ]  Installing monodevelop "
xterm -T "☣ INSTALL MONODEVELOP ☣" -geometry 100x30 -e "sudo apt-get install monodevelop -y"
echo -e $green "[ ✔ ] Done installing ...."
which monodevelop >> $log 2>&1
sleep 2
fi

#check if apache2 exists
which apache2 > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Apache2 ..........................[ found ]"
which apache2 >> $log 2>&1
sleep 2
else
echo -e $red "[ X ] Apache2 -> not found  "
echo -e $yellow "[ ! ]    Installing apache2 "
xterm -T "☣ INSTALL APACHE2 ☣" -geometry 100x30 -e "sudo apt-get install apache2 -y"
echo -e $green "[ ✔ ] Done installing ...."
which apache2 >> $log 2>&1
sleep 2
fi

#check if gnome terminal exists
#added this new install option because user may be running a distro that may not have gnome terminal installed by default
#gnome terminal is used in main script to run searchsploit
which gnome-terminal > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Gnome Terminal....................[ found ]"
which gnome-terminal >> $log 2>&1
sleep 2
else
echo -e $red "[ X ] Gnome-terminal-> not found "
echo -e $yellow "[ ! ] Installing gnome-terminal "
xterm -T "☣ INSTALL GNOME-TERMINAL ☣" -geometry 100x30 -e "sudo apt-get install gnome-terminal -y"
echo -e $green "[ ✔ ] Done installing ...."
which gnome-terminal >> $log 2>&1
sleep 2
fi

#Checking if upx compressor exists
which upx > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] UPX Compressor....................[ found ]"
which upx >> $log 2>&1
sleep 2
else
echo -e $red "[ X ] Upx compressor  -> not found "
echo -e $yellow "[ ! ] Installing upx-compressor "
xterm -T "☣ INSTALL UPX COMPRESSOR ☣" -geometry 100x30 -e "sudo apt-get install upx-ucl -y"
echo -e $green "[ ✔ ] Done installing ...."
which upx >> $log 2>&1
sleep 2
fi

#Checking if Ruby exists
which ruby > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Ruby..............................[ found ]"
which upx >> $log 2>&1
sleep 2
else
echo -e $red "[ X ] Ruby  -> not found "
echo -e $yellow "[ ! ] Installing Ruby "
xterm -T "☣ INSTALL Ruby ☣" -geometry 100x30 -e "sudo apt-get install ruby -y"
echo -e $green "[ ✔ ] Done installing ...."
which upx >> $log 2>&1
sleep 2
fi


#Checking if Jarsigner exists
which jarsigner > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Jarsigner (java)..................[ found ]"
which jarsigner >> $log 2>&1
rm -f $config
#Creating new config file 
touch $config
echo "********************************************************************************************************" >> $config
echo "** Configuration Paths for TheFatRat , do not delete anything from this file or program will not work **" >> $config
echo "**       if you need to reconfig your tools path , then run ./setup.sh in (TheFatRat directory) .     **" >> $config
echo "********************************************************************************************************" >> $config
echo "jarsigner" | tee -a $config >> /dev/null 2>&1
sleep 2
else
echo -e $red "[ X ] Jarsigner (java) -> not found "
echo -e $yellow "[ ! ] Installing Java "
xterm -T "☣ INSTALL OPENJDK-8 ☣" -geometry 100x30 -e "sudo apt-get install openjdk-8-jre openjdk-8-jdk -y "
echo -e $green "[ ✔ ] Done installing ...."
which jarsigner >> $log 2>&1
rm -f $config
#Creating new config file 
touch $config
echo "********************************************************************************************************" >> $config
echo "** Configuration Paths for TheFatRat , do not delete anything from this file or program will not work **" >> $config
echo "**       if you need to reconfig your tools path , then run ./setup.sh in (TheFatRat directory) .     **" >> $config
echo "********************************************************************************************************" >> $config
echo "jarsigner" | tee -a $config >> /dev/null 2>&1
sleep 2
fi

#Checking if Unzip exists
which unzip > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Unzip.............................[ found ]"
which unzip >> $log 2>&1
echo "unzip" | tee -a $config >> /dev/null 2>&1
sleep 2
else
echo -e $red "[ X ] Unzip -> not found "
echo -e $yellow "[ ! ] Installing Unzip "
xterm -T "☣ INSTALL UNZIP ☣" -geometry 100x30 -e "sudo apt-get install unzip -y "
echo -e $green "[ ✔ ] Done installing ...."
which unzip >> $log 2>&1
echo "unzip" | tee -a $config >> /dev/null 2>&1
sleep 2
fi

#Checking if keytool exists
which keytool > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Keytool (java)....................[ found ]"
which keytool >> $log 2>&1
echo "keytool" | tee -a $config >> /dev/null 2>&1
sleep 2
else
echo -e $red "[ X ] Keytool (java) -> not found  "
echo -e $yellow "[ ! ] Installing Java "
xterm -T "☣ INSTALL JAVA ☣" -geometry 100x30 -e "sudo apt-get install openjdk-8-jdk -y "
echo -e $green "[ ✔ ] Done installing ...."
which keytool >> $log 2>&1
echo "keytool" | tee -a $config >> /dev/null 2>&1
sleep 2
fi

#installing dependencies for ruby script 
echo -e $green "[ ! ] Installing dedendencies for ruby script"
xterm -T "☣ INSTALL DEPENDENCIES ☣" -geometry 100x30 -e "sudo apt-get install zlib1g-dev libmagickwand-dev imagemagick -y"
echo -e $green "[ ✔ ] Done installing ...."
sleep 2

#Adding zipalign path to config
echo -e $green "[ ✔ ] Zipalign "
echo "$path/tools/android-sdk-25.0.2/zipalign" >> $log 2>&1
echo "$path/tools/android-sdk-25.0.2/zipalign" | tee -a $config >> /dev/null 2>&1
sleep 2


#Adding Proguard path to config
echo -e $green "[ ✔ ] Proguard "
echo "$path/tools/proguard5.3.2/lib/proguard" >> $log 2>&1
echo "$path/tools/proguard5.3.2/lib/proguard" | tee -a $config >> /dev/null 2>&1
sleep 2

xterm -T "☣ INSTALL APKCREATION DEPENDENCIES ☣" -geometry 100x30 -e "sudo apt-get install lib32z1 lib32ncurses5 lib32stdc++6 -y"
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

#Adding Dx & Aapt path to config 
which aapt > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $red "[ X ] Aapt..........................."

# Removing current installed aapt version on user system and setting aapt 25.0.2 in thirdparty tools
# This must be done because apktool 2.2.2 will conflict with an old aapt version on building apk files
# Aapt is not a variable that could be set automatically , calls to aapt are made by apktool internally
xterm -T "☣ Removing Your Current Aapt ☣" -geometry 100x30 -e "sudo apt-get remove --purge aapt -y" >>$log 2>&1
unlink /usr/local/sbin/aapt > /dev/null 2>&1
unlink /usr/bin/aapt > /dev/null 2>&1
ln -s $path/tools/android-sdk-25.0.2/aapt /usr/local/sbin/aapt > /dev/null 2>&1
echo -e $green "[ ✔ ] Dx & Aapt"
echo "$path/tools/android-sdk-25.0.2/dx" >> $log 2>&1
echo "$path/tools/android-sdk-25.0.2/dx" | tee -a $config >> /dev/null 2>&1
echo "$path/tools/android-sdk-25.0.2/aapt" >> $log 2>&1
echo "$path/tools/android-sdk-25.0.2/aapt" | tee -a $config >> /dev/null 2>&1
sleep 2
else
echo -e $green "[ ✔ ] Dx & Aapt"
echo "$path/tools/android-sdk-25.0.2/dx" >> $log 2>&1
echo "$path/tools/android-sdk-25.0.2/dx" | tee -a $config >> /dev/null 2>&1
echo "$path/tools/android-sdk-25.0.2/aapt" >> $log 2>&1
echo "$path/tools/android-sdk-25.0.2/aapt" | tee -a $config >> /dev/null 2>&1
ln -s $path/tools/android-sdk-25.0.2/aapt /usr/local/sbin/aapt > /dev/null 2>&1
sleep 2
fi

#Adding Apktool path to config
xterm -T "☣ REMOVE OLD APKTOOL ☣" -geometry 100x30 -e "sudo apt-get remove --purge apktool -y"
echo -e $green "[ ✔ ] Apktool 2.2.2 "
echo "$path/tools/apktool2.2.2/apktool" >> $log 2>&1
echo "$path/tools/apktool2.2.2/apktool" | tee -a $config >> /dev/null 2>&1
unlink /usr/local/sbin/apktool > /dev/null 2>&1
unlink /usr/bin/apktool > /dev/null 2>&1
ln -s $path/tools/apktool2.2.2/apktool /usr/local/sbin/apktool > /dev/null 2>&1
sleep 2

#Checking if dex2jar exists
which d2j-jar2dex > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Dex2Jar...........................[ found ]"
which d2j-jar2dex >> $log 2>&1
echo "d2j-jar2dex" | tee -a $config >> /dev/null 2>&1
sleep 2
else
echo -e $red "[ X ] Dex2jar  -> not found "
echo -e $yellow "[ ! ] Installing dex2jar "
xterm -T "☣ INSTALL DEX2JAR ☣" -geometry 100x30 -e "sudo apt-get install dex2jar --force-yes -y"
echo -e $green "[ ✔ ] Done installing ...."
which d2j-jar2dex >> $log 2>&1
echo "d2j-jar2dex" | tee -a $config >> /dev/null 2>&1
sleep 2
fi

# check if metasploit-framework its installed
which msfconsole > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Metasploit-Framework..............[ found ]"
echo "msfconsole" | tee -a $config $log >> /dev/null 2>&1
echo "msfvenom" | tee -a $config $log >> /dev/null 2>&1
sleep 2
else
echo ""
echo -e $red "[ X ] metasploit-framework -> not found "

# Providing manual input to user in case metasploit was installed from git and is not on system path

q1=$(zenity  --list  --radiolist  --column "Pick" --column "Action" TRUE "Setup Metasploit path manually" FALSE "Install Metasploit from Repository" FALSE "Use default config" --text="`printf "Metasploit-Framework was not detected in your system path ! \n Choose one of the options bellow ."`");
case $q1 in 
 
"Setup Metasploit path manually")

minpm=$(zenity --entry --title="Metasploit Path Manual Input" --width=100 --height=100 --text="Write the location of your Metasploit Path?" --entry-text="/opt/metasploit-framework");
ret=$?

if [ $ret = "0" ]; then
#Creation of symlinks to metasploit manual path in /usr/local/sbin to avoid changes in fatrat scripts

unlink /usr/local/sbin/msfconsole > /dev/null 2>&1
unlink /usr/local/sbin/msfvenom > /dev/null 2>&1
ln -s $minpm/msfconsole /usr/local/sbin/msfconsole > /dev/null 2>&1
ln -s $minpm/msfvenom /usr/local/sbin/msfvenom > /dev/null 2>&1
echo "msfconsole" | tee -a $config $log > /dev/null 2>&1
echo "msfvenom" | tee -a $config $log > /dev/null 2>&1
fi

if [ $ret = "1" ]; then
echo "msfconsole" | tee -a $config $log > /dev/null 2>&1
echo "msfvenom" | tee -a $config $log > /dev/null 2>&1
fi
;;

"Install Metasploit from Repository")
echo -e $yellow "[ ! ] Installing Metasploit-Framework  "
xterm -T "☣ INSTALL METASPLOIT-FRAMEWORK ☣" -geometry 100x30 -e "sudo apt-get install metasploit-framework --force-yes -y"
echo -e $green "[ ✔ ] Done installing ...."
echo "msfconsole" | tee -a $config $log > /dev/null 2>&1
echo "msfvenom" | tee -a $config $log > /dev/null 2>&1
;;
"Use default config")cd
echo "msfconsole" | tee -a $config $log > /dev/null 2>&1
echo "msfvenom" | tee -a $config $log > /dev/null 2>&1
;;
esac
fi
# Check if backdoor-factory exists

which backdoor-factory > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Backdoor-Factory..................[ found ]"
echo "backdoor-factory" | tee -a $config $log > /dev/null 2>&1
sleep 2
else
echo -e $red "[ X ] backdoor-factory  -> not found "
echo ""

q2=$(zenity  --list  --radiolist  --column "Pick" --column "Action" TRUE "Setup Backdoor-Factory path manually" FALSE "Install Backdoor-Factory from Repository" FALSE "Use default config" --text="`printf "Backdoor-Factory was not detected in your system path ! \n Choose one of the options bellow ."`");
case $q2 in 
 
"Setup Backdoor-Factory path manually")
minpb=$(zenity --entry --title="Backdoor-Factory Path Manual Input" --width=100 --height=100 --text="Write the location of your Backdoor-Factory Path?" --entry-text="/opt/backdoor-factory/backdoor.py");
ret=$?

if [ $ret = "0" ]; then
echo "python2 $minpb" | tee -a $config $log > /dev/null 2>&1
fi

if [ $ret = "1" ]; then
echo "backdoor-factory" | tee -a $config $log > /dev/null 2>&1
fi
;;

"Install Backdoor-Factory from Repository")
echo -e $yellow "[ ! ]   Installing backdoor-factory "
xterm -T "☣ INSTALL BACKDOOR-FACTORY ☣" -geometry 100x30 -e "sudo apt-get install backdoor-factory --force-yes -y"
echo -e $green "[ ✔ ] Done installing ...."
echo "backdoor-factory" | tee -a $config $log > /dev/null 2>&1
;;

"Use default config")
echo "backdoor-factory" | tee -a $config $log > /dev/null 2>&1
;;
esac
fi
# check if searchsploit exists

which searchsploit > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Searchsploit......................[ found ]"
echo "searchsploit" | tee -a $config $log > /dev/null 2>&1
sleep 2
else
echo -e $red "[ X ] searchsploit  -> not found"
echo ""
q3=$(zenity  --list  --radiolist  --column "Pick" --column "Action" TRUE "Setup Searchsploit path manually" FALSE "Install Searchsploit from Repository" FALSE "Use default config" --text="`printf "Searchsploit was not detected in your system path ! \n Choose one of the options bellow ."`");
case $q3 in 
 
"Setup Searchsploit path manually")
minpc=$(zenity --entry --title="Searchsploit Path Manual Input" --width=100 --height=100 --text="Write the location of your Searchsploit Path?" --entry-text="/opt/searchsploit/searchsploit");
ret=$?

if [ $ret = "0" ]; then
echo "bash $minpc" | tee -a $config $log > /dev/null 2>&1
fi

if [ $ret = "1" ]; then
echo "searchsploit" | tee -a $config $log > /dev/null 2>&1
fi
;;

"Install Searchsploit from Repository")
echo -e $yellow "[ ! ]    Installing searchsploit "
xterm -T "☣ INSTALL SEARCHSPLOIT ☣" -geometry 100x30 -e "sudo apt-get install exploitdb --force-yes -y"
echo -e $green "[ ✔ ] Done installing ...."
echo "searchsploit" | tee -a $config $log > /dev/null 2>&1
sleep 2
echo ""
echo -e $green "Configuration and tool installed with success!";
sleep 2
;;

"Use default config")
echo "searchsploit" | tee -a $config $log > /dev/null 2>&1
;;
esac
fi

################################
# rebackyo repo
################################
echo -e $blue "Reactivating you original repositories"
rm -f /etc/apt/sources.list
mv /etc/apt/sources.list.backup /etc/apt/sources.list
#now we can remove the emergency backup securely
rm -f /etc/apt/sources.list.fatrat
apt-get clean
xterm -T "☣ UPDATE YOUR REPO ☣" -geometry 100x30 -e "sudo apt-get update "
clear

zenity --width=100 --height=100 --no-wrap --title="FatRat Shorcut Creation" --question --ok-label="Yes" --cancel-label="No" --text="`printf "Do you wish to create a fatrat shortcut in your system path ? \n So you can call fatrat from anywhere in terminal ."`";
lnk=$?
if [ $lnk ==  "0" ];then
dir=`pwd` 
scrp="cd $dir && ./fatrat"
rm -f /usr/local/sbin/fatrat
touch /usr/local/sbin/fatrat
echo "#!/bin/bash" > /usr/local/sbin/fatrat
echo $scrp >> /usr/local/sbin/fatrat
chmod +x /usr/local/sbin/fatrat
chmod +x fatrat
chmod +x backdoor_apk
chmod +x $path/tools/android-sdk-25.0.2/zipalign
chmod +x $path/tools/proguard5.3.2/lib/proguard
chmod +x $path/tools/android-sdk-25.0.2/dx
chmod +x $path/tools/android-sdk-25.0.2/aapt
chmod +x $path/tools/apktool2.2.2/apktool
which fatrat >> $log 2>&1
clear
zenity --info --width=100 --height=100 --no-wrap --text="FatRat shorcut created , write (fatrat) anywhere in terminal to open it ."
sleep 2 
echo -e $green "Instalation completed"
exit
fi
if [ $lnk ==  "1" ];then
chmod +x fatrat
chmod +x backdoor_apk
chmod +x $path/tools/android-sdk-25.0.2/zipalign
chmod +x $path/tools/proguard5.3.2/lib/proguard
chmod +x $path/tools/android-sdk-25.0.2/dx
chmod +x $path/tools/android-sdk-25.0.2/aapt
chmod +x $path/tools/apktool2.2.2/apktool
zenity --width=100 --height=100 --no-wrap --info --text="To execute fatrat write in fatrat directory (./fatrat) to execute it."
sleep 2
echo -e $green "Instalation completed"
fi
exit
