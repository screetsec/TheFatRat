
# TheFatRat 

[![Version](https://img.shields.io/badge/TheFatRat-1.9.8-brightgreen.svg?maxAge=259200)]()
[![Version](https://img.shields.io/badge/Codename-Target-red.svg?maxAge=259200)]()
[![Stage](https://img.shields.io/badge/Release-Testing-brightgreen.svg)]()
[![Build](https://img.shields.io/badge/Supported_OS-Linux-orange.svg)]()
[![Available](https://img.shields.io/badge/Available-BlackArch-red.svg?maxAge=259200)]()
[![Documentation](https://img.shields.io/badge/CEHv10-eccouncil-blue.svg?maxAge=259200)](https://github.com/ManhNho/CEHv10/tree/master/Slides)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-blue.svg?style=flat)]()


###  A Massive Exploiting Tool

![Banner](https://user-images.githubusercontent.com/17976841/65820028-6ae17e00-e24e-11e9-894f-35836481cc2c.png)

**TheFatRat** is an exploiting tool which compiles malware with famous payloads to be executed on Linux, Windows, Mac and Android. **TheFatRat** provides an easy way to create backdoors and payloads which can bypass most anti-viruses. 
 
 ## Information
 This tool is for educational purpose only, usage of TheFatRat for attacking targets without prior mutual consent is illegal.
Developers assume no liability and are not responsible for any misuse or damage cause by this program.

 ## Features!
- Fully automating msfvenom & Metasploit.
- Local or remote listener generation.
- Easily make backdoors with categorized operating systems.
- Generate payloads in various formats.
- Bypass anti-viruses.
- File pumper for increasing exploit file sizes.
- Detect external IP & interface addresses.
- Automatically create AutoRun files for USB / CDROM exploitation

### But it's shit! And your implementation sucks!
- Yes, you're probably correct. Feel free to not use it. And if you want to make it better create a pull request. 


# Installation
Instructions on how to install *TheFatRat*
```bash
git clone https://github.com/Screetsec/TheFatRat.git
cd TheFatRat
chmod +x setup.sh && ./setup.sh
```
### Updates
```bash
cd TheFatRat
./update && chmod +x setup.sh && ./setup.sh
```
### Troubleshooting on TheFatRat
Use the chk_tools script in case of problems on setting up TheFatRat using setup.sh.
This script will check if your packages are on their supported versions to run TheFatRat and will also provide you the solutions for your problems.
```
cd TheFatRat
chmod +x chk_tools 
./chk_tools
```

## Tools Overview
| Front View | Sample Feature	|
| ------------  | ------------ |
|![Index](https://cloud.githubusercontent.com/assets/17976841/25420100/9ee12cf6-2a80-11e7-8dfa-c2e3cfe71366.png)|![f](https://user-images.githubusercontent.com/17976841/65820886-91a4b200-e258-11e9-9a00-1e5905f6be16.jpg)

## Documentation
- Documentation available in modules CEH v9 and V10, download source here 
	- [CEHv10 Module 06 System Hacking.pdf](https://github.com/khanhnnvn/CEHv10/blob/master/Labs/CEHv10%20Module%2006%20System%20Hacking.pdf)
	- [CEHv10 Module 17 Hacking Mobile Platforms.pdf](https://github.com/khanhnnvn/CEHv10/blob/master/Labs/CEHv10%20Module%2017%20Hacking%20Mobile%20Platforms.pdf)
- Published in International Journal of Cyber-Security and Digital Forensics
	- [Malware Analysis Of Backdoor Creator : TheFatRat](https://www.researchgate.net/publication/323574673_MALWARE_ANALYSIS_OF_BACKDOOR_CREATOR_FATRAT)
- Youtube Videos 
	- [How To Download & Install TheFatRat](https://www.youtube.com/watch?v=FsSgJFxyzFQ)
	- [TheFatRat 1.9.6 - Trodebi ( Embed Trojan into Debian Package )](https://www.youtube.com/watch?v=NCsrcqhUBCc&feature=youtu.be&list=PLbyfDadg3caj6nc3KBk375lKWDOjiCmb8)
	- [hacking windows 10 with TheFatRat](https://www.youtube.com/watch?v=bFXVAXRXE9Q )
	- [Hacking Windows using TheFatRat + Apache2 Server + Ettercap + Metasploit](https://www.youtube.com/watch?v=FlXMslSjnGw)
	- [Hacking with a Microsoft Office Word Document from TheFatRat](https://www.youtube.com/watch?v=lglOXojT84M)
	- [XSS to powershell attack and bypass Antivirus using BeEF + TheFatRat + Metasploit](https://www.youtube.com/watch?v=pbvg7pgxVjo)
	- [TheFatRat - Hacking Over WAN - Embedding Payload in Original Android APK - Without Port Forwarding](https://www.youtube.com/watch?v=XLNigYZ5-fM)
	- [How To Automatically Embed Payloads In APK's - Evil-Droid, Thefatrat & Apkinjector](https://www.youtube.com/watch?v=C_Og6LnEZSg)
	- [Bind FUD Payload with JPG and Hack over WAN with TheFatRat](https://www.youtube.com/watch?v=VPl1TMCAIy8)


## Changelog
All notable changes to this project will be documented in this [file](https://github.com/Screetsec/thefatrat/blob/master/CHANGELOG.md).

### About issues
- Read [issues.md](https://github.com/Screetsec/TheFatRat/blob/master/issues.md) before making an issue

## Alternative Best Tool - Generating Backdoor & Bypass 
- [Veil-Framework /Veil](https://github.com/Veil-Framework/Veil) - Veil Framework 
- [Shellter](https://www.shellterproject.com/download/) - Shellter AV Evasion Artware
- [Unicorn](https://github.com/trustedsec/unicorn) - Trustedsec 
- [MSFvenom Payload Creator (MSFPC)](https://github.com/g0tmi1k/msfpc) - g0tmi1k
- [Venom](https://github.com/r00t-3xp10it/venom) - Pedro Ubuntu
- [Phantom-Evasion](https://github.com/oddcod3/Phantom-Evasion) - Diego Cornacchini


## Credits & Thanks
- [Offensive Security](https://www.offensive-security.com/) - Offensive Security
- [dracOs Linux](https://dracos-linux.org/) - Penetration Testing OS From Indonesia
- [peterpt](https://github.com/peterpt) - Maintainer & Contributor
- [Dana James Traversie](https://github.com/dana-at-cp/backdoor-apk) - backdoor_apk
- [z0noxz](https://github.com/z0noxz/powerstager) - Powerstager
- [TrustedSec](https://github.com/trustedsec/unicorn) - Unicorn
- [Raphael Mudge](https://github.com/rsmudge) - External Source
- [astr0baby](https://astr0baby.wordpress.com) - Reference Source
- [NgeSEC](https://ngesec.id/) Community
- [Gauli(dot)Net](https://gauli.net/) - Lab Penetration

## License
TheFatRat is made with 🖤 by Edo Maland & all [contributors](https://github.com/Screetsec/TheFatRat/graphs/contributors). See the **License** file for more details.


