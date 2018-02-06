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

## This procedure is the same for all other packages that may give an error on output as (Not OK) , except these ones :
- proguard
- dx (from android sdk)
- aapt (from android sdk)
- apktool
- dex2jar
* these packages come in fatrat instalation folder .
#-------------------------------------------------------------------------------------#

It is advised to have in your sources list the repository for your linux distribution , best way to check it is :

on your terminal : (cat /etc/apt/sources.list)

if everyline in this file have an (#) behind , then it means that is not activated .

The solution is to search on your official linux distribution the repository links and add them in sources.list .
You can use any text editor , if you are familiarized with nano editor , then run (nano /etc/apt/sources.list)
and paste the links from your linux distribution from official website in that file , and save it .
After that point , just do (apt-get update && apt-get upgrade) to upgrade your linux .

#----------------------------------------------------------------------#
Errors builing rat apks in fatrat .

All tools in fatrat were not made by us , this means that we are unable to help you on that .
backdoor-apk was denvelopen by Dana James Traversie at : https://github.com/dana-at-cp/backdoor-apk
Powerstager was denveloped by Z0noxz at : https://github.com/z0noxz/powerstager



