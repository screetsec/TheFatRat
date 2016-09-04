
 

#TheFatRat ( Unit for bypass av )
 

##Update: Version 1.5 , Codename Unity 

What is FatRat ?? 

Easy tool for generate backdoor with msfvenom ( part of metasploit framework ) and program compiles a C program with a meterpreter reverse_tcp payload In it that can then be executed on a windows host Program to create a C program after it is compiled that will bypass most AV . 
#Screenshot
<img src="https://cloud.githubusercontent.com/assets/17976841/18155659/f28f3912-7039-11e6-8d5d-7d0ed85dbdda.png" width="70%"></img> 
#------------------------------------------------------------------

<img src="https://cloud.githubusercontent.com/assets/17976841/18156182/937271d8-703e-11e6-8d5a-c922f645e7f1.png" width="23%"></img>
<img src="https://cloud.githubusercontent.com/assets/17976841/18156184/93762206-703e-11e6-8076-ac4865516933.png" width="23%"></img> <img src="https://cloud.githubusercontent.com/assets/17976841/18156183/9374bef2-703e-11e6-94f2-6ec4682525d2.png" width="23%"></img> <img src="https://cloud.githubusercontent.com/assets/17976841/18156214/d6a6d61a-703e-11e6-83f4-db3253cac6e7.png" width="23%"></img> <img src="https://cloud.githubusercontent.com/assets/17976841/17238517/85cda976-5586-11e6-8655-baed407be58d.png" width="23%"></img> 
#Automating metasploit functions 

- Checks for metasploit service and starts if not present

- Easily craft meterpreter reverse_tcp payloads for Windows, Linux, Android and Mac and another

- Start multiple meterpreter reverse_tcp listners 

- Fast Search in searchsploit

- Bypass AV

- Create backdoor with another techniq

- Autorunscript for listeners ( easy to use )

- Drop into Msfconsole

- Some other fun stuff :)



#Autorun Backdoor

- Autorun work if the victim disabled uac ( user acces control ) or low uac ( WINDOWS ) 
- What is uac ? you can visit ( http://www.digitalcitizen.life/uac-why-you-should-never-turn-it-off ) 
- I have also created 3 AutoRun files
- Simply copy these files to a CD or USB
- You can change the icon autorun file or exe in folder icon ( replace your another ico and replace name with autorun.ico )


#HOW CHANGE THE ICONS ? 

- Copy your icon picture to folder /TheFatrat/icons
- Change the name into autorun.ico 
- And Replace 
- Done 


## :scroll: Changelog
Be sure to check out the [Changelog] and Read CHANGELOG.md


## Getting Started
1. ```git clone https://github.com/Screetsec/TheFatRat.git```
2. ```cd Fatrat```
3. ```apt-get update``` 
4. ```apt-get install mingw32 backdoor-factory```

##In kali linux 2016.2 if failed install mingw or Unable to locate package , do this`
1. ``` echo 'deb http://http.kali.org/kali sana main non-free contrib' >> /etc/apt/sources.list```
2. ``` apt-get update  ```
3. ``` apt-get install mingw32 ``


 
## :book: How it works

* Extract The lalin-master to your home or another folder
* chmod +x fatrat
* chmod +x powerfull.sh
* And run the tools ( ./fatrat )
* Easy to Use just input your number


##  :heavy_exclamation_mark: Requirements

- A linux operating system. We recommend Kali Linux 2 or Kali 2016.1 rolling / Cyborg / Parrot / Dracos / BackTrack / Backbox / and another operating system ( linux ) 

- Must install metasploit framework 

- required gcc program , i586-mingw32msvc-gcc or i686-w64-mingw32-gcc ( apt-get install mingw32 ) for fix error


##  :heavy_exclamation_mark: READ
- if prog.c file to large when create backdoor with powerfull.sh , you can use prog.c.backup and create another backup when you running option 2


## Tutorial ? 

you can visit my channel  : https://www.youtube.com/channel/UCpK9IXzLMfVFp9NUfDzxFfw



## :octocat: Credits

- Thanks to allah and Screetsec [ Edo -maland- ] <Me> 
- Dracos Linux from Scratch Indonesia ( Penetration os ) Thanksyou , you can see in http://dracos-linux.org/ 
- Offensive Security for the awesome OS ( http://www.offensive-security.com/ )
- http://www.kali.org/"   
- Jack Wilder admin in http://www.linuxsec.org
- And another open sources tool in github
- Uptodate new tools hacking visit http://www.kitploit.com

## Disclaimer

***Note: modifications, changes, or alterations to this sourcecode is acceptable, however,any public releases utilizing this code must be approved by writen this tool ( Edo -m- ).***

