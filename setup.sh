#!/bin/bash
#Instalation of searchsploit (exploitdb)
function ssplt() {

# check if searchsploit exists
which searchsploit > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Searchsploit......................[ found ]"
echo "searchsploit" | tee -a "$config" "$log" > /dev/null 2>&1
echo "Searchsploit -> OK" >> "$inst"
sleep 1
else
echo -e $red "[ X ] searchsploit  -> not found"
echo ""
echo -e $okegreen "Select one of the options bellow"
echo -e $orange "+-------------------------------------------------+"
echo -e $orange "|$white [$okegreen 1$white ]$yellow Setup Searchsploit Path Manually$orange          |"
echo -e $orange "|$white [$okegreen 2$white ]$yellow Install Searchsploit from Kali Repository$orange |"
echo -e $orange "+-------------------------------------------------+"
echo ""
echo -ne $okegreen "Option : ";tput sgr0
read q1
case $q1 in
 
1)
echo ""
echo -e $green "Enter The Path of your Searchsploit instalation"
echo -e $cyan "ex : /opt/searchsploit/searchsploit"
echo ""
echo -ne $green "PATH : ";tput sgr0
read sspp
if [ ! -f $sspp ]
then
echo ""
echo -e $red "It was not possible to found searchsploit executable in : $sspp"
echo ""
echo -e $green "Make sure you write the right path of your instalation"
echo ""
echo -e $okegreen "Press [ENTER] key to try again ."
read cont
ssplt
else
echo "bash $sspp" | tee -a "$config" "$log" > /dev/null 2>&1
echo "Searchsploit -> OK" >> "$inst"
fi
;;

#ok
2)
echo -e $yellow "[ ! ]  Installing Searchsploit "
xterm -T "☣ INSTALL SEARCHSPLOIT ☣" -geometry 100x30 -e "sudo apt-get install exploitdb --force-yes -y"
which searchsploit > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Searchsploit"
echo "searchsploit" | tee -a "$config" "$log" > /dev/null 2>&1
echo "Searchsploit -> OK" >> "$inst"
else
echo "0" > "$stp"
echo "Searchsploit -> Not OK" >> "$inst"
fi
;;
*)
ssplt
;;
esac
fi
echo ""
#Go check the check file exists and read its value
chk=$path/logs/check
if [ -f "$chk" ]
then
ct=`sed -n 1p $chk`
#if value of check is 0 theen some package was not installed sucefully 
if [ "$ct" == "0" ]; then
clear
echo -e $red "Fatrat was not able to install some packages"
echo ""
echo -e $blue "Reactivating your original repositories"
rm -f /etc/apt/sources.list
mv /etc/apt/sources.list.backup /etc/apt/sources.list
#now we can remove the emergency backup securely
rm -f /etc/apt/sources.list.fatrat
apt-get clean
xterm -T "☣ UPDATE YOUR REPO ☣" -geometry 100x30 -e "sudo apt-get update "
clear
rm -rf "$config" >/dev/null 2>&1
# Currently building the diagnostic script
#echo -e $okegreen "Starting diagnostics"
#chmod +x diag.sh > /dev/null 2>&1
#./diag.sh

#Display to user the install.log file and inform him what to do
echo "Was not possible to install The Packages Labeled (Not Ok) in this list above" >> "$inst"
echo "Try : (apt-get remove --purge <packagename> && apt-get autoremove && apt-get install -f)" >> "$inst"
echo "before running fatrat setup script again" >> "$inst"
cat "$inst"
exit
elif [ "$ct" == "1" ]; then
echo ""
#value in check file is 1 , then everything is ok , delete install.log file and proceed to finish setup
rm -rf "$inst" >/dev/null 2>&1
fi
else
#in case value in check file is not 0 or 1 then something is wrong
echo -e $okegreen "Something went very wrong , execute ./setup.sh again"
rm -rf "$config" >/dev/null 2>&1
echo ""
echo "Was not possible to install The Packages Labeled (Not Ok) in this list above" >> "$inst"
echo "Try : (apt-get remove --purge <packagename> && apt-get autoremove && apt-get install -f)" >> "$inst"
echo "before running fatrat setup script again" >> "$inst"
echo "" >> "$inst"
echo "***********Your current sources.list***************"
sclst=`cat /etc/apt/sources.list`
echo $sclst >> "$inst"
echo "***************Finish sources.list*****************" >> "$inst"
dist=`uname -a`
echo "" >> "$inst"
echo "Your linux distribution :" >> "$inst"
echo $dist >> "$inst"
cat "$inst"
echo -e $lightgreen "This log file can be found in : $inst "
exit
fi
}

function bkf() {
# Check if backdoor-factory exists

which backdoor-factory > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Backdoor-Factory..................[ found ]"
echo "backdoor-factory" | tee -a "$config" "$log" > /dev/null 2>&1
echo "Backdoor-Factory -> OK" >> "$inst"
sleep 1
ssplt
else
echo -e $red "[ X ] backdoor-factory  -> not found "
echo ""

echo ""
echo -e $green "Select one of the options bellow"
echo -e $orange "+-----------------------------------------------------+"
echo -e $orange "|$white [$okegreen 1$white ]$yellow Setup Backdoor-Factory Path Manually$orange          |"
echo -e $orange "|$white [$okegreen 2$white ]$yellow Install Backdoor-Factory from Kali Repository$orange |"
echo -e $orange "+-----------------------------------------------------+"
echo ""
echo -ne $green "Option : ";tput sgr0
read q2
case $q2 in

1)
echo ""
echo -e $green "Enter The Path of your backdoor-factory instalation"
echo -e $cyan "ex : /opt/backdoor-factory/backdoor.py"
echo ""
echo -ne $green "PATH : ";tput sgr0
read msp
bkdf=$msp
if [ ! -f $bkdf ]
then
echo ""
echo -e $red "It was not possible to found backdoor-factory executable in : $bkdf"
echo ""
echo -e $green "Make sure you write the right path of your instalation"
echo ""
echo -e $green "Press [ENTER] key to try again ."
read cont
bkf
fi
echo "python2 $bkdf" | tee -a "$config" "$log" > /dev/null 2>&1
echo "Backdoor-factory -> OK" >> "$inst"
ssplt
;;

2)
echo -e $yellow "[ ! ] Installing backdoor-factory "
xterm -T "☣ INSTALL BACKDOOR-FACTORY ☣" -geometry 100x30 -e "sudo apt-get install backdoor-factory --force-yes -y"
which backdoor-factory > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Backdoor-Factory -> OK"
echo "backdoor-factory" | tee -a "$config" "$log" > /dev/null 2>&1
echo "Backdoor-factory -> OK" >> "$inst"
else
echo -e $red "[ X ] backdoor-factory"
echo "0" > "$stp"
echo "Backdoor-factory -> Not OK" >> "$inst"
ssplt
fi
;;

*)
bkf
;;
esac
fi
}

function mtspl() {
# check if metasploit-framework its installed
which msfconsole > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Metasploit-Framework..............[ found ]"
echo "msfconsole" | tee -a "$config" "$log" >> /dev/null 2>&1
echo "msfvenom" | tee -a "$config" "$log" >> /dev/null 2>&1
echo "Metasploit -> OK" >> "$inst"
sleep 1
bkf
else
echo -e $red "[ X ] metasploit-framework -> not found "

# Providing manual input to user in case metasploit was installed from git and is not on system path

echo ""
echo -e $okegreen "Select one of the options bellow"
echo -e $orange "+---------------------------------------------------------+"
echo -e $orange "|$white [$okegreen 1$white ]$yellow Setup Metasploit Framework Path Manually$orange          |"
echo -e $orange "|$white [$okegreen 2$white ]$yellow Install Metasploit Framework from Kali Repository$orange |"
echo -e $orange "+---------------------------------------------------------+"
echo ""
echo -ne $okegreen "Option : ";tput sgr0
read q3
case $q3 in
1)
echo ""
echo -e $green "Enter The Path of your metasploit instalation"
echo -e $cyan "ex : /opt/metasploit-framework"
echo ""
echo -ne $green "PATH : ";tput sgr0
read msp
msfc=$msp/msfconsole
msfv=$msp/msfvenom
if [ ! -f $msfc ]
then
echo ""
echo -e $red "It was not possible to found msfconsole in : $msfc"
echo ""
echo -e $green "Make sure you write the right path of your instalation"
echo ""
echo -e $green "Press [ENTER] key to try again ."
read cont
mtspl
fi
if [ ! -f $msfv ]
then
echo ""
echo -e $red "It was not possible to found msfvenom in : $msfv"
echo ""
echo -e $green "Make sure you write the right path of your instalation"
echo ""
echo -e $green "Press [ENTER] key to try again ."
read cont
mtspl
fi
#Creation of symlinks to metasploit manual path in /usr/local/sbin to avoid changes in fatrat scripts

unlink /usr/local/sbin/msfconsole > /dev/null 2>&1
unlink /usr/local/sbin/msfvenom > /dev/null 2>&1
ln -s $msfc /usr/local/sbin/msfconsole > /dev/null 2>&1
ln -s $msfv /usr/local/sbin/msfvenom > /dev/null 2>&1
echo "msfconsole" | tee -a "$config" "$log" > /dev/null 2>&1
echo "msfvenom" | tee -a "$config" "$log" > /dev/null 2>&1
echo "Metasploit -> OK" >> "$inst"
bkf
;;

2)
echo -e $yellow "[ ! ] Installing Metasploit-Framework  "
xterm -T "☣ INSTALL METASPLOIT-FRAMEWORK ☣" -geometry 100x30 -e "sudo apt-get install metasploit-framework --force-yes -y"
which msfconsole > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Metasploit (msfconsole) -> OK"
echo "msfconsole" | tee -a "$config" "$log" > /dev/null 2>&1
echo "Metasploit (msfconsole) -> OK" >> "$inst"
else
echo -e $red "[ x ] Metasploit (msfconsole)"
echo "Metasploit (msfconsole) -> Not OK" >> "$inst"
echo "0" > "$stp"
fi
which msfvenom > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Metasploit (msfvenom) -> OK"
echo "msfvenom" | tee -a "$config" "$log" > /dev/null 2>&1
echo "Metasploit (msfvenom) -> OK" >> "$inst"
else
echo -e $red "[ x ] Metasploit (msfvenom)"
echo "0" > "$stp"
echo "Metasploit (msfvenom) -> Not OK" >> "$inst"
fi
bkf
;;
*)
mtspl
;;
esac
fi
}


function cont() {

stp="logs/check"
#remove any previous check file from previous attempts
rm -rf "$stp" >/dev/null 2>&1
#starting setup , input 1 value to check file
echo "1" > "$stp"
#remove any previous install.log file from previous attempts
rm -rf "$inst" >/dev/null 2>&1

#check if xterm is installed
which xterm > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Xterm.............................[ found ]"
which xterm >> "$log" 2>&1
echo "xterm -> OK" > "$inst"
else
echo ""
echo -e $red "[ X ] Xterm -> not found! "
echo -e $yellow "[ ! ] Installing Xterm                     "
echo -e $green ""
sudo apt-get install xterm -y
which xterm >> "$log" 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Xterm -> OK"
echo "Xterm -> OK" > "$inst"
else
echo -e $red "[ x ] Xterm"
echo "0" > "$stp"
echo "xterm -> Not OK" > "$inst"
fi
fi

sleep 1
#check if dig its installed
which dig > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Dns-Utils ........................[ found ]"
which dig >> "$log" 2>&1
echo "Dns-Utils -> OK" >> "$inst"
else
echo -e $red "[ X ] dnsutils -> not found! "
echo -e $yellow "[ ! ]  Installing dnsutils"
xterm -T "☣ INSTALL DNSUTILS ☣" -geometry 100x30 -e "sudo apt-get install dnsutils -y"
which dig >> "$log" 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Dns-Utils -> OK"
echo "Dns-Utils -> OK" >> "$inst"
else
echo -e $red "[ x ] Dns-Utils"
echo "0" > "$stp"
echo "dns-utils -> Not OK" >> "$inst"
fi
fi
sleep 1
# check if gcc exists
which gcc > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Gcc compiler......................[ found ]"
which gcc >> "$log" 2>&1
echo "GCC -> OK" >> "$inst"
else
echo -e $red "[ X ] gcc compiler      -> not found "
echo -e $yellow "[ ! ]   Installing gcc "
xterm -T "☣ INSTALL GCC COMPILLER ☣" -geometry 100x30 -e "sudo apt-get install gcc -y"
which gcc >> "$log" 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] GCC -> OK"
echo "GCC -> OK" >> "$inst"
else
echo -e $red "[ x ] GCC"
echo "0" > "$stp"
echo "gcc -> Not OK" >> "$inst"
fi
fi
sleep 1
#check if apache2 exists
which apache2 > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Apache2 ..........................[ found ]"
which apache2 >> "$log" 2>&1
echo "Apache2 -> OK" >> "$inst"
else
echo -e $red "[ X ] Apache2 -> not found  "
echo -e $yellow "[ ! ]    Installing apache2 "
xterm -T "☣ INSTALL APACHE2 ☣" -geometry 100x30 -e "sudo apt-get install apache2 -y"
which apache2 >> "$log" 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Apache2 -> OK"
echo "Apache2 -> OK" >> "$inst"
else
echo -e $red "[ x ] Apache2"
echo "0" > "$stp"
echo "apache2 -> Not OK" >> "$inst"
fi
fi
sleep 1
#check if gnome terminal exists
#added this new install option because user may be running a distro that may not have gnome terminal installed by default
#gnome terminal is used in main script to run searchsploit
which gnome-terminal > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Gnome Terminal....................[ found ]"
which gnome-terminal >> "$log" 2>&1
echo "Gnome Terminal -> OK" >> "$inst"
else
echo -e $red "[ X ] Gnome-terminal-> not found "
echo -e $yellow "[ ! ] Installing gnome-terminal "
xterm -T "☣ INSTALL GNOME-TERMINAL ☣" -geometry 100x30 -e "sudo apt-get install gnome-terminal -y"
which gnome-terminal >> "$log" 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Gnome Terminal -> OK"
echo "Gnome Terminal -> OK" >> "$inst"
else
echo -e $red "[ x ] Gnome Terminal"
echo "0" > "$stp"
echo "gnome-terminal -> Not OK" >> "$inst"
fi
fi

#Checking if upx compressor exists
sleep 1
which upx > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] UPX Compressor....................[ found ]"
which upx >> "$log" 2>&1
echo "UPX -> OK" >> "$inst"
else
echo -e $red "[ X ] Upx compressor  -> not found "
echo -e $yellow "[ ! ] Installing upx-compressor "
xterm -T "☣ INSTALL UPX COMPRESSOR ☣" -geometry 100x30 -e "sudo apt-get install upx-ucl -y"
which upx >> "$log" 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] UPX Compressor -> OK"
echo "UPX -> OK" >> "$inst"
else
echo -e $red "[ x ] UPX Compressor"
echo "0" > "$stp"
echo "upx-ucl -> Not OK" >> "$inst"
fi
fi
sleep 1
#Checking if Ruby exists
which ruby > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Ruby..............................[ found ]"
which ruby >> "$log" 2>&1
echo "Ruby -> OK" >> "$inst"
else
echo -e $red "[ X ] Ruby  -> not found "
echo -e $yellow "[ ! ] Installing Ruby "
xterm -T "☣ INSTALL Ruby ☣" -geometry 100x30 -e "sudo apt-get install ruby -y && gem install nokogiri"
which ruby >> "$log" 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Ruby -> OK"
echo "Ruby -> OK" >> "$inst"
else
echo -e $red "[ x ] Ruby"
echo "0" > "$stp"
echo "ruby -> Not OK" >> "$inst"
fi
fi
sleep 1
#Checking if Openssl exists
which openssl > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Openssl...........................[ found ]"
which openssl >> "$log" 2>&1
echo "Openssl -> OK" >> "$inst"
else
echo -e $red "[ X ] Openssl  -> not found "
echo -e $yellow "[ ! ] Installing Openssl "
xterm -T "☣ INSTALL OPENSSL ☣" -geometry 100x30 -e "sudo apt-get install openssl -y"
which openssl >> "$log" 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Openssl -> OK"
echo "Openssl -> OK" >> "$inst"
else
echo -e $red "[ x ] Openssl"
echo "0" > "$stp"
echo "openssl -> Not OK" >> "$inst"
fi
fi
sleep 1
#installing dependencies for ruby script 
echo -e $green "[ ! ] Installing tools dependencies"
xterm -T "☣ INSTALL DEPENDENCIES ☣" -geometry 100x30 -e "sudo apt-get install zlib1g-dev libmagickwand-dev imagemagick lib32z1 lib32ncurses5 lib32stdc++6 python-pip python-dev build-essential -y && pip install names"
sleep 1

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
#echo 'deb http://http.kali.org/kali kali-rolling main contrib non-free' >> /etc/apt/sources.list
#echo 'deb-src http://http.kali.org/kali kali-rolling main contrib non-free' >> /etc/apt/sources.list
echo 'deb https://http.kali.org/kali kali-rolling main non-free contrib' > /etc/apt/sources.list
xterm -T "☣ UPDATING KALI REPO ☣" -geometry 100x30 -e "sudo apt-get clean && sudo apt-get update"
sleep 1

# check if monodevelop exists
#which monodevelop > /dev/null 2>&1
#if [ "$?" -eq "0" ]; then
#echo -e $green "[ ✔ ] Monodevelop ......................[ found ]"
#which monodevelop >> "$log" 2>&1
#echo "Monodevelop -> OK" >> "$inst"
#else
#echo -e $red "[ X ] Monodevelop  -> not found "
#echo -e $yellow "[ ! ]  Installing monodevelop "
#xterm -T "☣ INSTALL MONODEVELOP ☣" -geometry 100x30 -e "sudo apt-get install monodevelop --force-yes -y"
#which monodevelop >> "$log" 2>&1
#if [ "$?" -eq "0" ]; then
#echo -e $green "[ ✔ ] Monodevelop -> OK"
#echo "Monodevelop -> OK" >> "$inst"
#else
#echo -e $red "[ x ] Monodevelop"
#echo "0" > "$stp"
#echo "monodevelop -> Not OK" >> "$inst"
#fi
#fi
#sleep 1

#Checking if Jarsigner exists
which jarsigner > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Jarsigner (java)..................[ found ]"
which jarsigner >> "$log" 2>&1
echo "Jarsigner -> OK" >> "$inst"
rm -f "$config"
#Creating new config file 
touch "$config"
echo "********************************************************************************************************" >> "$config"
echo "** Configuration Paths for TheFatRat , do not delete anything from this file or program will not work **" >> "$config"
echo "**       if you need to reconfig your tools path , then run ./setup.sh in (TheFatRat directory) .     **" >> "$config"
echo "********************************************************************************************************" >> "$config"
echo "jarsigner" | tee -a "$config" >> /dev/null 2>&1
else
echo -e $red "[ X ] Jarsigner (java) -> not found "
echo -e $yellow "[ ! ] Installing Java "
xterm -T "☣ INSTALL OPENJDK-8 ☣" -geometry 100x30 -e "sudo apt-get install openjdk-8-jdk openjdk-8-jre --force-yes -y "
which jarsigner > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Jarsigner -> OK"
which jarsigner >> "$log" 2>&1
echo "Jarsigner -> OK" >> "$inst"
rm -f "$config"
#Creating new config file 
touch "$config"
echo "********************************************************************************************************" >> "$config"
echo "** Configuration Paths for TheFatRat , do not delete anything from this file or program will not work **" >> "$config"
echo "**       if you need to reconfig your tools path , then run ./setup.sh in (TheFatRat directory) .     **" >> "$config"
echo "********************************************************************************************************" >> "$config"
echo "jarsigner" | tee -a "$config" >> /dev/null 2>&1
else
echo -e $red "[ x ] Jarsigner"
echo "0" > "$stp"
echo "jarsigner (openjdk-8-jdk)-> Not OK" >> "$inst"
fi
fi
sleep 1

#Checking if Unzip exists
which unzip > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Unzip.............................[ found ]"
which unzip >> "$log" 2>&1
echo "unzip" | tee -a "$config" >> /dev/null 2>&1
echo "Unzip -> OK" >> "$inst"
else
echo -e $red "[ X ] Unzip -> not found "
echo -e $yellow "[ ! ] Installing Unzip "
xterm -T "☣ INSTALL UNZIP ☣" -geometry 100x30 -e "sudo apt-get install unzip --force-yes -y "
which unzip >> "$log" 2>&1
if [ "$?" -eq "0" ]; then
echo "unzip" | tee -a "$config" >> /dev/null 2>&1
echo -e $green "[ ✔ ] Unzip -> OK"
echo "Unzip -> OK" >> "$inst"
else
echo -e $red "[ x ] Unzip"
echo "0" > "$stp"
echo "unzip -> Not OK" >> "$inst"
fi
fi

sleep 1
#Checking if keytool exists
which keytool > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Keytool (java)....................[ found ]"
which keytool >> "$log" 2>&1
echo "keytool" | tee -a "$config" >> /dev/null 2>&1
echo "Keytool -> OK" >> "$inst"
else
echo -e $red "[ X ] Keytool (java) -> not found  "
echo -e $yellow "[ ! ] Installing Java "
xterm -T "☣ INSTALL JAVA ☣" -geometry 100x30 -e "sudo apt-get install openjdk-8-jdk --force-yes -y "
which keytool >> "$log" 2>&1
if [ "$?" -eq "0" ]; then
echo "keytool" | tee -a "$config" >> /dev/null 2>&1
echo -e $green "[ ✔ ] Keytool -> OK"
echo "Keytool -> OK" >> "$inst"
else 
echo -e $red "[ x ] Keytool"
echo "0" > "$stp"
echo "keytool -> Not OK" >> "$inst"
fi
fi

sleep 1

#Adding zipalign path to config
echo -e $green "[ ✔ ] Zipalign "
echo "$path/tools/android-sdk/zipalign" >> "$log" 2>&1
echo "$path/tools/android-sdk/zipalign" | tee -a "$config" >> /dev/null 2>&1
sleep 1


#Adding Proguard path to config
echo -e $green "[ ✔ ] Proguard "
echo "$path/tools/proguard5.3.2/lib/proguard" >> "$log" 2>&1
echo "$path/tools/proguard5.3.2/lib/proguard" | tee -a "$config" >> /dev/null 2>&1
sleep 1

# check if mingw32 or mingw-64 exists 
# Case not exists then reedirect to mingw instalation depending on arch

which x86_64-w64-mingw32-gcc >> /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Mingw-w64 Compiler................[ found ]"
which x86_64-w64-mingw32-gcc >> "$log" 2>&1
echo "Mingw64 -> OK" >> "$inst"
else
echo -e $red "[ X ] Mingw-w64 -> not found "
#Powerstager requires mingw64 to work , mingw32 is required because powerfull.sh requires it for 32bit fud exe compiling
# In case mingw64 not found then remove any previously mingw32 & 64 bit faulty instalations and install mingw64 

xterm -T "☣ INSTALL MINGW64 COMPILLER ☣" -geometry 100x30 -e "sudo apt-get remove --purge mingw* -y && apt-get autoremove -y && apt-get install mingw* --force-yes -y"
which x86_64-w64-mingw32-gcc > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Mingw-64 Compiler..................[ found ]"
which x86_64-w64-mingw32-gcc >> "$log" 2>&1
echo "Mingw64 -> OK" >> "$inst"
else
echo "0" > "$stp"
echo "mingw-w64 -> Not OK" >> "$inst"
fi
fi

# check if ming32  
# Case not exists then reedirect to mingw instalation depending on arch

which i686-w64-mingw32-gcc >> /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Mingw-32 Compiler................[ found ]"
which i686-w64-mingw32-gcc >> "$log" 2>&1
echo "Mingw32 -> OK" >> "$inst"
else
echo -e $red "[ X ] Mingw-32 -> not found "
#Powerstager requires mingw64 to work , mingw32 is required because powerfull.sh requires it for 32bit fud exe compiling
# In case mingw64 not found then remove any previously mingw32 & 64 bit faulty instalations and install mingw64 

xterm -T "☣ INSTALL MINGW32 COMPILLER ☣" -geometry 100x30 -e "sudo apt-get remove --purge mingw* -y && apt-get autoremove -y && apt-get install mingw* --force-yes -y"
which i686-w64-mingw32-gcc > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Mingw-32 Compiler..................[ found ]"
which i686-w64-mingw32-gcc >> "$log" 2>&1
echo "Mingw32 -> OK" >> "$inst"
else
echo "0" > "$stp"
echo "mingw-32 -> Not OK" >> "$inst"
fi
fi

#Checking for DX and in case exists then check if it is version 1.8 used in fatrat (latest android sdk) 
which dx > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
dxg=`dx --version 2>&1 | tee temp/dx`
dxv=`cat temp/dx | awk '{print $3}'` 
case $dxv in
1.8)
#DX exists and it is version 1.8
rm -rf temp/dx >/dev/null 2>&1
which dx >> "$log" 2>&1
echo "dx" | tee -a "$config" >> /dev/null 2>&1
echo -e $green "[ ✔ ] DX 1.8"
echo "DX -> OK" >> "$inst"
;;
*)
#DX does not exists or is not 1.8 version
xterm -T "☣ Removing Your Current DX ☣" -geometry 100x30 -e "sudo apt-get remove --purge dx -y"
unlink "/usr/local/sbin/dx" > /dev/null 2>&1
ln -s "$path/tools/android-sdk/dx" "/usr/local/sbin/dx" > /dev/null 2>&1
which dx > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
which dx >> "$log" 2>&1
echo "dx" | tee -a "$config" >> /dev/null 2>&1
echo -e $green "[ ✔ ] DX 1.8"
echo "DX -> OK" >> "$inst"
else
echo -e $red "[ x ] DX 1.8"
echo "0" > "$stp"
echo "dx -> Not OK" >> "$inst"
fi
;;
esac
else
unlink "/usr/local/sbin/dx" > /dev/null 2>&1
ln -s "$path/tools/android-sdk/dx" "/usr/local/sbin/dx" > /dev/null 2>&1
which dx > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
which dx >> "$log" 2>&1
echo "dx" | tee -a "$config" >> /dev/null 2>&1
echo -e $green "[ ✔ ] DX 1.8"
echo "DX -> OK" >> "$inst"
else
echo -e $red "[ x ] DX 1.8"
echo "0" > "$stp"
echo "dx -> Not OK" >> "$inst"
fi
fi
# check if aapt exists and if it is version v0.2-3821160 used in fatrat (android sdk)
rm /usr/local/sbin/aapt >/dev/null 2>&1
which aapt > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
aptv=`aapt v | awk '{print $5}'`
case $aptv in
v0.2-3821160)
#exists and it is v0.2-3821160
which aapt >> "$log" 2>&1
echo "aapt" | tee -a "$config" >> /dev/null 2>&1
echo -e $green "[ ✔ ] Aapt v0.2-3821160"
echo "Aapt -> OK" >> "$inst"
;;
*)
#Aapt does not exists or is not the latest version used in fatrat (android sdk)
xterm -T "☣ Removing Your Current Aapt ☣" -geometry 100x30 -e "sudo apt-get remove --purge aapt -y"
unlink "/usr/local/sbin/aapt" > /dev/null 2>&1
ln -s "$path/tools/android-sdk/aapt" "/usr/local/sbin/aapt" > /dev/null 2>&1
which aapt > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
which aapt >> "$log" 2>&1
echo "aapt" | tee -a "$config" >> /dev/null 2>&1
echo -e $green "[ ✔ ] Aapt v0.2-3821160"
echo "Aapt -> OK" >> "$inst"
else
echo -e $red "[ x ] Aapt v0.2-3821160"
echo "0" > "$stp"
echo "aapt -> Not OK" >> "$inst"
fi
;;
esac
else
unlink "/usr/local/sbin/aapt" > /dev/null 2>&1
ln -s "$path/tools/android-sdk/aapt" "/usr/local/sbin/aapt" > /dev/null 2>&1
which aapt > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
which aapt >> "$log" 2>&1
echo "aapt" | tee -a "$config" >> /dev/null 2>&1
echo -e $green "[ ✔ ] Aapt v0.2-3821160"
echo "Aapt -> OK" >> "$inst"
else
echo -e $red "[ x ] Aapt v0.2-3821160"
echo "0" > "$stp"
echo "aapt -> Not OK" >> "$inst"
fi
fi

#Same procedure used for dx and aapt , but for apktool 2.2.2.
which apktool > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
apk=`apktool | sed -n 1p | awk '{print $2}'` > /dev/null 2>&1
case $apk in 
v.2.2.2)
which apktool >> "$log" 2>&1
echo "apktool" | tee -a "$config" >> /dev/null 2>&1
echo -e $green "[ ✔ ] Apktool v.2.2.2"
echo "Apktool -> OK" >> "$inst"
;;
*)
xterm -T "☣ REMOVE OLD APKTOOL ☣" -geometry 100x30 -e "sudo apt-get remove --purge apktool -y"
unlink "/usr/local/sbin/apktool" > /dev/null 2>&1
ln -s "$path/tools/apktool2.2.2/apktool" "/usr/local/sbin/apktool" > /dev/null 2>&1
which apktool > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Apktool v.2.2.2"
which apktool >> "$log" 2>&1
echo "apktool" | tee -a "$config" >> /dev/null 2>&1
echo "Apktool -> OK" >> "$inst"
else
echo -e $red "[ x ] Apktool v.2.2.2"
echo "0" > "$stp"
echo "apktool -> Not OK" >> "$inst"
fi
;;
esac
else
unlink "/usr/local/sbin/apktool" > /dev/null 2>&1
ln -s "$path/tools/apktool2.2.2/apktool" "/usr/local/sbin/apktool" > /dev/null 2>&1
which apktool > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
which apktool >> "$log" 2>&1
echo "apktool" | tee -a "$config" >> /dev/null 2>&1
echo -e $green "[ ✔ ] Apktool v.2.2.2"
echo "Apktool -> OK" >> "$inst"
else
echo -e $red "[ x ] Apktool v.2.2.2"
echo "0" > "$stp"
echo "apktool -> Not OK" >> "$inst"
fi
fi
#Same as others before , but dex2jar in this case will be installed directly to user OS , instead be working in fatrat tools
which d2j-dex2jar > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
dex=`d2j-dex2jar 2>&1 | tee temp/dex`
d2j=`cat temp/dex | sed -n 19p | awk '{print $2}' | cut -f1 -d','` 
case $d2j in
reader-2.0)
rm -rf temp/dex >/dev/null 2>&1
which d2j-dex2jar >> "$log" 2>&1
echo "d2j-dex2jar" | tee -a "$config" >> /dev/null 2>&1
echo -e $green "[ ✔ ] Dex2Jar 2.0"
echo "Dex2Jar -> OK" >> "$inst"
;;
*)
rm -rf temp/dex >/dev/null 2>&1
#Dex2jar does not exists or it is not the 2.0 version , so uninstall it & copy dex2jar from
#fatrat tools folder to /usr/local/sbin 
xterm -T "☣ Removing Your Current Dex2Jar ☣" -geometry 100x30 -e "sudo apt-get remove --purge dex2jar --force-yes -y" 
cp $path/tools/dex2jar/* /usr/local/sbin/ > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-baksmali > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-dex-recompute-checksum > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-dex2jar > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-dex2smali > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-jar2dex > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-jar2jasmin > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-jasmin2jar > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-smali > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-std-apk > /dev/null 2>&1
# remove any previous version files from dex2jar lib from /usr/local/share 
# and copy the new ones to there from fatrat tools dir
rm -rf /usr/local/share/dex2jar > /dev/null 2>&1
mkdir /usr/local/share/dex2jar > /dev/null 2>&1
cp -r $path/tools/dex2jar/lib /usr/local/share/dex2jar/lib > /dev/null 2>&1
which d2j-dex2jar > /dev/null 2>&1
#After new instalation , check if dex2jar is working
if [ "$?" -eq "0" ]; then
#Dex2jar was suceffully installed 
echo -e $green "[ ✔ ] Dex2Jar 2.0"
which d2j-dex2jar >> "$log" 2>&1
echo "d2j-dex2jar" | tee -a "$config" >> /dev/null 2>&1
echo "Dex2Jar -> OK" >> "$inst"
else
#After the instalation something did not worked , place the warnings in logs
echo -e $red "[ x ] Dex2Jar 2.0"
echo "0" > "$stp"
echo "dex2jar -> Not OK" >> "$inst"
fi
;;
esac
else
#dex2jar does not exist in user linux OS , proceed with a clean manual installation
cp $path/tools/dex2jar/* /usr/local/sbin/ > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-baksmali > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-dex-recompute-checksum > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-dex2jar > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-dex2smali > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-jar2dex > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-jar2jasmin > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-jasmin2jar > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-smali > /dev/null 2>&1
chmod +x /usr/local/sbin/d2j-std-apk > /dev/null 2>&1
rm -rf /usr/local/share/dex2jar > /dev/null 2>&1
mkdir /usr/local/share/dex2jar > /dev/null 2>&1
cp -r $path/tools/dex2jar/lib /usr/local/share/dex2jar/lib > /dev/null 2>&1
which d2j-dex2jar > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] Dex2Jar 2.0"
which d2j-dex2jar >> "$log" 2>&1
echo "d2j-dex2jar" | tee -a "$config" >> /dev/null 2>&1
echo "Dex2Jar -> OK" >> "$inst"
else
echo -e $red "[ x ] Dex2Jar 2.0"
echo "0" > "$stp"
echo "dex2jar -> Not OK" >> "$inst"
fi
fi
mtspl

################################
# rebackyo repo
################################
echo -e $blue "Reactivating your original repositories"
rm -f /etc/apt/sources.list
mv /etc/apt/sources.list.backup /etc/apt/sources.list
#now we can remove the emergency backup securely
rm -f /etc/apt/sources.list.fatrat
apt-get clean
xterm -T "☣ UPDATE YOUR REPO ☣" -geometry 100x30 -e "sudo apt-get update "
clear
echo -e $okegreen "Do you want to create a shortcut for fatrat in your system"
echo -e $okegreen "so you can run fatrat from anywhere in your terminal and desktop ?"
echo ""
echo -ne $cyan "Choose y/n : "
read cho
case $cho in

y|Y|Yes|yes|YES)
lnk=$?
if [ $lnk ==  "0" ];then
dir=`pwd` 
scrp="cd $dir && ./fatrat"
rm -f /usr/local/sbin/fatrat
touch /usr/local/sbin/fatrat
echo "#!/bin/bash" > /usr/local/sbin/fatrat
echo $scrp >> /usr/local/sbin/fatrat
cp $path/config/TheFatRat.desktop /usr/share/applications/TheFatRat.desktop
cp $path/icons/TheFatRat.ico /usr/share/icons/TheFatRat.ico
chmod +x /usr/local/sbin/fatrat
chmod +x fatrat
chmod +x update
chmod +x backdoor_apk
chmod +x $path/tools/power.py
chmod +x $path/tools/android-sdk/zipalign
chmod +x $path/tools/proguard5.3.2/lib/proguard
chmod +x $path/tools/android-sdk/dx
chmod +x $path/tools/android-sdk/aapt
chmod +x $path/tools/apktool2.2.2/apktool
which fatrat >> "$log" 2>&1
clear
echo ""
echo -e $green "Instalation completed , To execute fatrat write anywhere in your terminal (fatrat)"
fi
;;

n|no|No|NO)
chmod +x fatrat
chmod +x update
chmod +x backdoor_apk
chmod +x $path/tools/power.py
chmod +x $path/tools/android-sdk/zipalign
chmod +x $path/tools/proguard5.3.2/lib/proguard
chmod +x $path/tools/android-sdk/dx
chmod +x $path/tools/android-sdk/aapt
chmod +x $path/tools/apktool2.2.2/apktool
clear
echo ""
echo -e $green "Instalation completed , To execute fatrat write in fatrat directory (./fatrat)"
;;

*)
chmod +x fatrat
chmod +x update
chmod +x backdoor_apk
chmod +x $path/tools/power.py
chmod +x $path/tools/android-sdk/zipalign
chmod +x $path/tools/proguard5.3.2/lib/proguard
chmod +x $path/tools/android-sdk/dx
chmod +x $path/tools/android-sdk/aapt
chmod +x $path/tools/apktool2.2.2/apktool
clear
echo ""
echo -e $green "Instalation completed , To execute fatrat write in fatrat directory (./fatrat)"
;;
esac
exit 

}  
#Case ping goggle hostname fails , the this function will load to check what is happening 
function chknet() {
echo -e $red "[X] Your Internet is not working correctly!"
sleep 1
echo -e $cyan "[*] Checking ...."
#ping hostname failed , so now will test ping google ip dns server
ping -c 1 8.8.4.4 > /dev/null 2>&1
png="$?" 
 if [ $png == "0" ]
then
#Ping dns server worked , inform user what happened and proceed with setup
    echo -e $red "[X] Your linux OS is not able to resolve"
    echo -e $red "hostnames over terminal using ping !!"
    echo ""
    echo -e $yellow "Search on the web : (unable to resolve hostnames ping) to find a solution"
echo ""
echo -e $green "Setup will continue , but is not garantee that apt package management
may work properly , or even if it can resolve hostnames ."
echo ""
echo -e $cyan "Setup will continue because :"
echo -e $green "Ping google.com =$red Failed"
echo -e $green "Ping google DNS = Success"
echo ""
echo -e $green "Press [ENTER] key to continue"
read continue
cont
    sleep 1
elif [ $png == "1" ]
then
#user is only connected to lan and not to the web , abort setup
    echo -e $yellow "You are connected to your local network but not to the web ."
    echo -e $yellow "Check if your router/modem gateway is connected to the web ."
echo ""
echo -e $green "Setup will not continue , you are only connected to your local lan."
echo ""
echo -e $cyan "Setup will stop because :"
echo -e $green "Ping google.com =$red Failed"
echo -e $green "Ping google DNS =$red Failed"
echo ""
echo -e $green "Press [ENTER] key to continue"
read continue
exit 1
sleep 1
elif [ $png == "2" ]
then
# user is not connected to anywhere , web or lan , abort setup
echo -e $red "You are not connected to any network ."
echo ""
echo -e $cyan "Setup will stop because :"
echo -e $green "Ping google.com =$red Failed"
echo -e $green "Ping google DNS =$red Failed"
echo ""
echo -e $green "Press [ENTER] key to continue"
read continue
exit 1
    sleep 1
fi
}

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
echo -e $yellow ""
sudo apt-get clean && apt-get update -y
sleep 2
else
echo -e $green ""
fi 
#variables for logs and others
path=`pwd`
arch=`uname -m`
inst="$path/logs/install.log"
log="$path/logs/setup.log"
config="$path/config/config.path"
#Removing any previous setup log created
rm -rf "$log" > /dev/null 2>&1
rm -rf logs/check > /dev/null 2>&1

#terminal text colours code
cyan='\e[0;36m'
green='\e[0;32m'
lightgreen='\e[0;32m'
white='\e[0;37m'
red='\e[0;31m'
yellow='\e[0;33m'
blue='\e[0;34m'
purple='\e[0;35m'
orange='\e[38;5;166m'
path=`pwd`

#Check root dulu
if [ $(id -u) != "0" ]; then
echo -e $red [x]::[not root]: You need to be [root] to run this script.;
      echo ""
   	  sleep 1
exit 0
fi
#Many fresh installed linux distros do not come with sudo installed
which sudo > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo ""
else
apt-get install sudo -y
fi
echo ""
# Fixing any possible problems with packages missed/corrupted dependencies on user OS before proceed
echo -e $green "[ * ] Fixing any possible broken packages in apt management"
sleep 1
echo -e $white ""
sudo apt-get install -f -y && sudo apt-get autoremove -y
sleep 1
echo ""
echo -e $yellow "[ ✔ ] Done ! ....Proceeding with setup"
echo ""
sleep 2
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
echo -e $blue "         Setup Script for FATRAT 1.9.5       "
echo "------------------------------------------------------" > "$log"
echo "| Tools paths configured in (setup.sh) for TheFatRat |" >> "$log"
echo "------------------------------------------------------" >> "$log"
echo "                                                      " >> "$log"
echo ""
#Detect if user OS is 32Bit or 64bit
case $arch in
x86_64|aarch64) 
echo -e $yellow "              64Bit OS detected"
echo ""
;;
i386|i486|i586|i686)
echo -e $yellow "              32Bit OS detected"
echo ""
;;
*)
echo -e $red "Setup will not proceed because none of these archs were detected"
echo ""
echo -e $blue "x86_64|i386|i486|i586|i686|aarch64"
echo ""
echo -e $green "Your linux arch: $blue $arch $green is not supported"
echo ""
echo -e "Press any key to continue"
read abor
exit 0
;;
esac
echo -e $green "Checking type of shell ...."
sleep 1

#Check if user is using a remote shell or a local terminal
if [ -n "$SSH_CLIENT" ] || [ -n "$SSH_TTY" ]; then
  echo "[remote]"
echo ""
    echo -e $red "Fatrat & Setup does not work over a remote secure shell ."
    echo ""
echo -e $green "If you want to Install Fatrat on a remote computer then "
echo -e $green "use a remote desktop connection like (rdesktop) or (vnc) "
echo ""
echo -e $green "Press [ENTER] key to exit"
read abor
exit 1
else
echo [local]
  case $(ps -o comm= -p $PPID) in
    sshd|*/sshd) SESSION_TYPE=remote/ssh;;
  esac
fi

sleep 1
#First check of setup for internet connection by connecting to google over http
echo -e $green "[ * ] Checking for internet connection"
sleep 1
echo -e "GET http://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1
if [ $? -ne 0 ]; then
echo -e $red [ X ]::[Internet Connection]: OFFLINE!;
chknet
    sleep 1
else
echo -e $green [ ✔ ]::[Internet Connection]: CONNECTED!;
    sleep 1
    cont
fi

#ping -c 1 google.com > /dev/null 2>&1
#png="$?" 
# if [ $png == "0" ]
#then
#ping google hostname was succefully , then proceed with setup 
#    echo -e $green [ ✔ ]::[Internet Connection]: CONNECTED!;
#    sleep 1
#    cont
#elif [ $png == "1" ]
#then
#ping hostname failed , load chknet function
#    echo -e $yellow [ X ]::[Internet Connection]: LOCAL ONLY!;
#    chknet
#    sleep 1
#elif [ $png == "2" ]
#then
#ping hostname failed , load chknet function
#echo -e $red [ X ]::[Internet Connection]: OFFLINE!;
#chknet
#    sleep 1
#fi
