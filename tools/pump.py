"""
File pumper. Increase file size with null byte(s) at the end of the file.
"""

import sys
import os

# python pump.py [file] [size] [-mb/-kb]

# Also refer to KiB/MiB
KB = 1024
MB = KB * 1024

if len(sys.argv) < 4:
    sys.stderr.write('[-] Missing argument!\n')
    sys.stderr.write('[+] Usage: python pumper.py [file] [size] [-mb/-kb]\n')
    exit(1)

fileName = sys.argv[1]
size = int(sys.argv[2])
unit = sys.argv[3]

if not os.path.exists(fileName):
    sys.stderr.write('[-] File {!r} is not exists!\n'.format(fileName))
    exit(1)

if unit != '-mb' and unit != '-kb':
    sys.stderr.write('[-] Use -mb or -kb!\n')
    exit(1)

with open(fileName, 'ab') as fp:
    if unit == '-kb':
        blockSize = size * KB
    elif unit == '-mb':
        blockSize = size * MB

    bufferSize = 256
    for i in range(blockSize // bufferSize):
        fp.write(('\0' * bufferSize).encode('utf-8'))

print('[+] Finished pumping {!r} with {}{}'.format(fileName, size, unit[1:]))
