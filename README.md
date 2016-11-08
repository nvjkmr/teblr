# **teblr** 

![Tumblr on Termanal](/teblr.png "teblr")

Have you ever asked, how do I use tumblr on terminal? So here we are with *teblr*, a terminal based tool written in Python. We all know that how much pathetic is Tumblr's OAuth, but we tried our best to get you comfort. Now post text, photo, quote, link, audio or video with just a single command from your terminal. Also edit and delete posts at breeze.

We give you three basic features with three sub-commands:
```
tumblr set
tumblr post
tumblr edit
tumblr delete
```

##`tumblr set` usage:
```
usage: tumblr set [-h] (-db | -su)

optional arguments:
  -h, --help           show this help message and exit
  -db, --default-blog  Set default blog for your actions
  -su, --setup         Use this to run fresh setup
```

##`tumblr post` usage:
```
usage: tumblr post [-h]
                   (--photo | --text | --quote | --link | --audio | --video)
                   [-u URL | -f FILE] [--private | --draft | --queue]
                   [-d DATE] [-c CAPTION] [-e] [-s SOURCE] [-q QUOTE_TEXT]
                   [-b BLOG]

optional arguments:
  -h, --help            show this help message and exit
  --photo               Post a photo to your blog
  --text                Post text to your blog
  --quote               Post a quote to your blog
  --link                Post a link to your blog
  --audio               Post an audio to your blog
  --video               Post a video to your blog
  -u URL, --url URL     URL of the data, if any. Available for: photo, audio,
                        video, link posts
  -f FILE, --file FILE  Path to the file, if any. Available for: photo, audio,
                        video posts
  --private             Set post visibility to only you
  --draft               Add post to drafts
  --queue               Add post to queue
  -d DATE, --date DATE  Custom post date: dd-mm-yyyy
  -c CAPTION, --caption CAPTION
                        Post caption, if any Available for: photo, audio,
                        video posts
  -e, --editor          Open default editor for writing your post. Available
                        for: text posts
  -s SOURCE, --source SOURCE
                        Source of the post, if any. Available for: quote posts
  -q QUOTE_TEXT, --quote-text QUOTE_TEXT
                        Add quote text as argument. Available for: quote posts
  -b BLOG, --blog BLOG  Mention blog to post content.
```

##`tumblr edit` usage:
```
usage: tumblr edit [-h] (-u PID | -p PID) [-e] [-b BLOG]

optional arguments:
  -h, --help            show this help message and exit
  -u PID, --url PID     URL of the post that has to be edited
  -p PID, --post-id PID
                        ID of the post that has to be edited
  -e, --editor          Open default editor for editing your post. Available
                        for: text posts
  -b BLOG, --blog BLOG  Mention blog to edit content.
```

##`tumblr delete` usage:
```
usage: tumblr delete [-h] (-u PID | -p PID) [-b BLOG]

optional arguments:
  -h, --help            show this help message and exit
  -u PID, --url PID     URL of the post that has to be edited
  -p PID, --post-id PID
                        ID of the post that has to be edited
  -b BLOG, --blog BLOG  Mention blog to delete content.

```

**NOTE:** Editor support (`-e`) is available for posting and editing text posts only.

# Installation

Install pip using the following commands:
```
$ sudo apt-get install python-pip python-dev build-essential 
$ sudo pip install --upgrade pip 
$ sudo pip install --upgrade virtualenv 
```
Install teblr using pip:
```
$ sudo pip install -e git+https://github.com/VijayKumarHackr/teblr.git#egg=teblr
```
Setting up teblr:
```
$ tumblr set --setup
```

# Contribution
Contributions to this project are very much welcome. Please fork the code!

# License
Copyright 2016 Vijay Kumar.

The file `/teblr/console.py` is taken from [here](https://github.com/tumblr/pytumblr/blob/master/interactive_console.py).
Licensed under the Apache License, Version 2.0. More at: http://www.apache.org/licenses/LICENSE-2.0
