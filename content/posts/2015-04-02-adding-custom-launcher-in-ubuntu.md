---
title: "Adding a custom launcher in Ubuntu"
date: 2015-04-02T06:35:00.001Z
lastmod: 2026-01-13T23:34:40.391Z
tags:
  - ubuntu
  - pycharm
  - linux
  - launcher
aliases:
  - /2015/04/adding-custom-launcher-in-ubuntu.html
---

It is not straightforward to have your favorite programs that are not installed via package manager appear on Ubuntu (14.04) launcher. Couple of ways to do that:

- Sometimes, when the program is up, you can just right click and say “add to launcher”. It would work for most programs. However, this will fail for editors such as PyCharm that maintain project state and the launcher added this way will point to the specific project.
- The right way to do is this:
  - Create a .desktop entry
  For instance, for pycharm, do :

```makefile
$ sudo nano /usr/share/applications/pycharm.desktop


[Desktop Entry]
Name=PyCharm
Type=Application
Exec=/home/hvishwanath/Downloads/pycharm-community-4.0.5/bin/pycharm.sh
Terminal=false
Icon=/home/hvishwanath/Downloads/pycharm-community-4.0.5/bin/pycharm.png
Comment=PyCharm community edition 4.0.5
NoDisplay=false
Categories=Development;IDE
Name[en]=pycharm.desktop
```

```
* You can then search for the entry in main “Search” in the launcher, and simply drag and drop the pycharm.desktop entry that you would find on to the launcher.
```

That is it.

