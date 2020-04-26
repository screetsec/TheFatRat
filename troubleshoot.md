## Installation issues running fatrat

# Unable to install Mingw32 or mingw-w64

* 90% of the times this error happens because mingw was not correctly installed before in user desktop .
The best way to solve this issue is to completly remove mingw32 from system , clean any file directly to mingw32 
and execute an installation fix on your linux , so the symplinks and any other dependencies connected to mingw package
could be erased .

- For mingw32 as root user :
* apt-get remove --purge mingw32 -y && apt-get autoremove -y && apt-get install -f -y

- For mingw-w64 as root user :
* apt-get remove --purge mingw-w64 -y && apt-get autoremove -y && apt-get install -f -y

After this point and when finished , all the remains of your faulty mingw installation are already removed .

After this point , execute ./setup.sh on fatrat folder , so mingw packages could be correctly installed in your linux
from the Kali repositories .

- If you recently installed fatrat then you probably will have an issue with powerstager with error I/O when it tries to write the backdoor output file , to solve that issue you must add debian jessie repositories to your file /etc/apt/sources.list and deisable any new repository there , then uninstall and remove your current mingw instalation and run setup.sh from fatrat again .
* - look here https://github.com/Screetsec/TheFatRat/issues/391

Install mingw 4.9.1 version from Debian Repository

1st - add this line to /etc/apt/sources.list
deb http://ftp.debian.org/debian jessie main

2nd - remove all your mingw versions , write  this in your terminal
apt-get remove --purge \*mingw\* -y && apt-get autoremove -y

3rd - update your repositories and install mingw from jessie
apt-get update && apt-get install -t jessie \*mingw\* -f -y

## Manual install in parrot 

go to https://packages.debian.org/jessie/all/mingw32 and download the package at the bottom of the page. When it downloads, right click it and click Open with GDebi Package Installer, then install it. Do the same for https://packages.debian.org/jessie/all/mingw32-binutils

then run ./setup.py again. FatRat will install in Parrot.

## This procedure is the same for all other packages that may give an error on output as (Not OK) , except these ones :
- dx (from android sdk)
- aapt (from android sdk)
- apktool
* these packages come in fatrat instalation folder .
#-------------------------------------------------------------------------------------#

It is advised to have in your sources list the repository for your linux distribution , best way to check it is :

on your terminal : (cat /etc/apt/sources.list)

if everyline in this file have an (#) behind , then it means that is not activated .

The solution is to search on your official linux distribution the repository links and add them in sources.list .
You can use any text editor , if you are familiarized with nano editor , then run (nano /etc/apt/sources.list)
and paste the links from your linux distribution from official website in that file , and save it .
After that point , just do (apt-get update && apt-get upgrade) to upgrade your linux .

## Errors builing rat apks in fatrat .

All tools in fatrat were not made by us , this means that we are unable to help you on that .
backdoor-apk was denvelopen by : 
- Dana James Traversie at : https://github.com/dana-at-cp/backdoor-apk
- Powerstager was denveloped by Z0noxz at : https://github.com/z0noxz/powerstager


## Running powerstager you get he message (names not found)
The solution is to install names python module by running in your terminal ( pip install names)

## Running Powerstager you get the message (IOError: [Errno 2] No such file or directory: )
the solution for this problem is to downgrade your mingw packages , check this topic : 
https://github.com/Screetsec/TheFatRat/issues/391

## Package exact names installed by fatart during setup :

- exploitdb (search for vulnerabilities)
- backdoor-factory ( to merge backdoors in exe files)
- metasploit-framework (exploitation framework)
- xterm (Terminal emulator used in fatrat windows)
- dnsutils (To get your external ip address and dns)
- gcc (file compiler)
- apache2 (web server , used to create some exploits )
- gnome-terminal (terminal emulator used in some fatrat special features)
- upx-ucl (file compressor)
- ruby (To run ruby modules used in fatrat)
- openssl (To create certificates for the apks)
- zlib1g-dev libmagickwand-dev imagemagick lib32z1 lib32ncurses5 lib32stdc++6 python-pip python-dev build-essential (libraries dependencies for apk tools)
- Mono-MCS (file compiler for some backdoors in fatrat)
- openjdk-8-jdk and openjdk-8-jre (used by apk tools to sign the apks)
- unzip (zip extractor)
- mingw32 (32bit exe compiler for powerstager & others in fatrat)
- mingw-w64 (32bit exe compiler for powerstager & other in fatrat)



