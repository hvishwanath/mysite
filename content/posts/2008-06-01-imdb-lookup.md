---
title: "IMDB Lookup"
date: 2008-06-01T17:05:00Z
lastmod: 2026-01-13T23:34:40.392Z
tags:
  - hack python
aliases:
  - /2008/06/imdb-lookup.html
---
I have this [amazing friend](http://www.orkut.co.in/Profile.aspx?uid=17999891040117016036) who has more data than a corporate data center can manage. If you give him a $ for every byte of data he owns, then he will figure in the 10 most richest Indians. Anyway, I got the privilege of copying a subset of his data onto my 500GB harddrive (Obviously, it ran out of space). But I now have over 100GB worth movies and I have a difficult time figuring out what to watch.

I had to do a IMDB search for every title I see and pretty soon I realized its a pain in the ass. I did a small hack to ease my burden and it is [**here**](http://www.esnips.com/doc/5150768b-1e27-4847-962d-da5b55e8e625/IMDBLookup). (http://www.esnips.com/doc/5150768b-1e27-4847-962d-da5b55e8e625/IMDBLookup) I had to put it on esnips because my so called personal website dream has managed to remain one. ([here](http://hvishwanath.info) and [here](http://hvishwanath.phpnet.us )).

The zip file has a registry hack, just double clicking will put required info in your registry. It manages to bring up a nice little "IMDB Lookup" menu when you right click on a file. Copy the imdb.py Python script to your c:\windows\system32 folder, so that its there in your system path. Now you are good to go, whenever you see a movie file on your computer, just right click on it and select IMDB Lookup. If the movie title is neat and clear, your favourite browser pops up with IMDB description of the movie. Thats all it is.
[![](http://pics.livejournal.com/harrysdiary/pic/00001cqf/s320x240)](http://pics.livejournal.com/harrysdiary/pic/00001cqf/)

[![](http://pics.livejournal.com/harrysdiary/pic/00002sx6/s320x240)](http://pics.livejournal.com/harrysdiary/pic/00002sx6/)

IMDB is unfortunately blocked at office, but you can see that URL is valid and perfect. Most probably it will work for you.

PS : You need [Python 2.4 and above](http://www.python.org/download/)( freely available) for this hack. A C exe could have done the job, but.. why bother.

\-- If everything else fail, try Python.
