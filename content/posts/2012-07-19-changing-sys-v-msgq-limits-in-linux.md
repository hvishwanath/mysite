---
title: "Changing SYS V MSGQ Limits in Linux / Ubuntu"
date: 2012-07-19T14:17:00.003Z
lastmod: 2026-01-13T23:34:40.392Z
tags:
  - ubuntu linux msgq tech
aliases:
  - /2012/07/changing-sys-v-msgq-limits-in-linux.html
---
I keep discovering lot of stuff at work but never document it. I have decided to document them on the blog so that it stays, and will probably be useful for somebody who is after the same thing.

SYS V IPC limits are governed by the following kernel parameters.

Use sysctl to view and update these parameters.

```
root@ubuntu:/home/hvishwanath# sysctl -a | grep kernel.msg
error: permission denied on key 'vm.compact_memory'
kernel.msgmax = 8192
kernel.msgmni = 1655
kernel.msgmnb = 1024000
```

Same is also mounted on /proc

```
root@ubuntu:/home/hvishwanath# ll /proc/sys/kernel/msgm*
-rw-r--r-- 1 root root 0 Jul 19 12:50 /proc/sys/kernel/msgmax
-rw-r--r-- 1 root root 0 Jul 19 12:51 /proc/sys/kernel/msgmnb
-rw-r--r-- 1 root root 0 Jul 19 12:46 /proc/sys/kernel/msgmni
```

This are the default values on my system (Ubuntu 12.04).

```
root@ubuntu:/home/hvishwanath# ipcs -l

------ Shared Memory Limits --------
max number of segments = 4096
max seg size (kbytes) = 32768
max total shared memory (kbytes) = 8388608
min seg size (bytes) = 1

------ Semaphore Limits --------
max number of arrays = 128
max semaphores per array = 250
max semaphores system wide = 32000
max ops per semop call = 32
semaphore max value = 32767

------ Messages Limits --------
max queues system wide = 1655
max size of message (bytes) = 8192
default max size of queue (bytes) = 102400
```

I am using SYSV Message queue as a Message Broker, mainly because it provides APIs to read/write messages using a "Message ID". If you assign a unique message to every process that you have in your software, the Message Queue can be leveraged as a message broker. More on that in a different post.

Now, to cut the long story short, the default 16K size of the message queue was disheartening for me. To increase the size, and make it more useful for my application, I just had to add the following lines in /etc/sysctl.conf.

```
root@ubuntu:/home/hvishwanath# nano /etc/sysctl.conf
kernel.msgmax=8192
kernel.msgmni=1655
#Increase the msgq size to 5MB from 16K
kernel.msgmnb=5242880
```

Update the system using the conf file.

```
root@ubuntu:/home/hvishwanath# sysctl -p /etc/sysctl.conf
kernel.msgmax = 8192
kernel.msgmni = 1655
kernel.msgmnb = 5242880
```

You can verify it using ipcs.

```
root@ubuntu:/home/hvishwanath# ipcs -l

------ Shared Memory Limits --------
max number of segments = 4096
max seg size (kbytes) = 32768
max total shared memory (kbytes) = 8388608
min seg size (bytes) = 1

------ Semaphore Limits --------
max number of arrays = 128
max semaphores per array = 250
max semaphores system wide = 32000
max ops per semop call = 32
semaphore max value = 32767

------ Messages Limits --------
max queues system wide = 1655
max size of message (bytes) = 8192
default max size of queue (bytes) = 5242880
```

Since we have modified in sysctl.conf, this will preserved across reboots.
