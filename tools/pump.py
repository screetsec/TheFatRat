import sys
#python fpump.py [file] [size] [-mb/-kb]

if len(sys.argv) < 4:
 sys.exit('[-] Missing argument!\n[+] Usage: python pumper.py [file] [size] [-mb/-kb]')

fp = sys.argv[1]
size = int(sys.argv[2])
tp = sys.argv[3]

f = open(fp, 'ab')
if tp == '-kb':
    b_size = size * 1024
elif tp == '-mb':
    b_size = size * 1048576
else:
    sys.exit('[-] Use -mb or -kb!')

bufferSize = 256
for i in range(b_size/bufferSize):
    f.write(str('0' * bufferSize))

f.close()

print '[+] Finished pumping', fp, 'with', size, tp
