# teblr 
**te**rminal tum**blr**

We all know that how much pathetic is Tumblr's OAuth, but we tried our best to get you comfort. Now post text, photo, quote, link, audio or video with just a single command from your terminal. Also edit and delete posts at breeze.

We give you three basic features with three sub-commands:
```
tumblr post
tumblr edit
tumblr delete
```

##`tumblr post` usage:
```
usage: tumblr post [-h]
                   (--photo | --text | --quote | --link | --audio | --video)
                   [-u URL | -f FILE] [--private | --draft | --queue]
                   [-d DATE] [-c CAPTION] [-e EDITOR] [-s SOURCE]
                   [-q QUOTE_TEXT]

optional arguments:
  -h, --help            show this help message and exit
  --photo               Post a photo to your blog
  --text                Post text to your blog
  --quote               Post a quote to your blog
  --link                Post a link to your blog
  --audio               Post an audio to your blog
  --video               Post a video to your blog
  -u URL, --url URL     URL of the data, if any. Available for: photo, audio,
                        video, link
  -f FILE, --file FILE  Path to the file, if any. Available for: photo, audio,
                        video
  --private             Set post visibility to only you
  --draft               Add post to drafts
  --queue               Add post to queue
  -d DATE, --date DATE  Custom post date: dd-mm-yyyy
  -c CAPTION, --caption CAPTION
                        Post caption, if any Available for: photo, audio,
                        video
  -e EDITOR, --editor EDITOR
                        Open default editor for writing your post, if any.
                        Available for: text
  -s SOURCE, --source SOURCE
                        Source of the post, if any. Available for: quote
  -q QUOTE_TEXT, --quote-text QUOTE_TEXT
                        Add quote text as argument. Available for: quote
```

##`tumblr edit` usage:
```
usage: tumblr edit [-h] -p POST_ID

optional arguments:
  -h, --help            show this help message and exit
  -p POST_ID, --post-id POST_ID
                        ID of the post that has to be edited
```

##`tumblr delete` usage:
```
usage: tumblr delete [-h] -p POST_ID

optional arguments:
  -h, --help            show this help message and exit
  -p POST_ID, --post-id POST_ID
                        ID of the post that has to be deleted
```

**NOTE:** Editor support (`-e`) and `tumblr edit` are still under work. Any suggestions are welcome!
