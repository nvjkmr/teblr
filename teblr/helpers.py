import argparse
import console
import datetime
import urllib
import urllib2
import json
import teblr
import yaml
import os, sys, tempfile
from subprocess import call

reload(sys)
sys.setdefaultencoding('utf-8')     # default to unicode encoding
global default_blog

def post_action(args):
    if args.blog:
        blog_name = args.blog
    else:
        blog_name = get_blog_name()

    data_req = dict()
    data_req['text'] = ['title', 'body']
    data_req['link'] = ['title', 'description']
    
    post_data = dict()
    post_data['state'] = args.state
    # post_data['tags'] = args.tags    # not supported
    post_data['date'] = args.date
    
    if args.text:
        post_type = 'text'
        if (args.editor):
            d = get_user_input(data_req['text'])
            post_data['title'] = d['title']
            post_data['body'] = d['body']
        else:
            console_input = get_post_data(data_req['text'])
            post_data['title'] = console_input['title']
            post_data['body'] = console_input['body']
    elif args.video:
        post_type = 'video'
        post_data['caption'] = args.caption
        post_data['embed'] = args.url
        post_data['data'] = args.file
    elif args.quote:
        post_type = 'quote'
        post_data['quote'] = args.quote_text
        post_data['source'] = args.source   # source of quote
    elif args.audio:
        post_type = 'audio'
        post_data['caption'] = args.caption
        post_data['external_url'] = args.url
        post_data['data'] = args.file
    elif args.link:
        post_type = 'link'
        post_data['url'] = args.url
        console_input = get_post_data(data_req['link'])
        post_data['title'] = console_input['title']
        post_data['description'] = console_input['description']
    elif args.photo:
        post_type = 'photo'
        post_data['source'] = args.url                  # link to file
        post_data['data'] = args.file
        post_data['caption'] = args.caption
    else:
        print "Unknown post type found!"

    # filter None/null elements
    post_data = {k: v for k, v in post_data.items() if v!=None}
    
    # create post
    r = teblr.make_post(blog_name, post_type, post_data)
    
    if 'meta' in r and 'errors' in r['response']:
        print str(r['meta']['status']) + " status code returned! "+ str(r['response']['errors'][0])
    else:
        print "Done... Your blog post has been pushed!"

def edit_action(args):
    if args.blog:
        blog_name = args.blog
    else:
        blog_name = get_blog_name()

    print "Fetching previous post"
    prevs_data = extract_post(blog_name, args.post_id) 
    post_type = prevs_data['type']
    data_req = dict()
    data_req['text'] = ['title', 'body']
    data_req['link'] = ['title', 'description', 'url']
    
    # print "Printing previous post data..."
    # for key, value in prevs_data.iteritems(): # dig deep
        # print value
    # print "==="*20
    
    post_data = {}      # holds new data
    post_data['type'] = post_type   # required in teblr.__init__.py
    post_data['id'] = args.post_id
    if post_type == 'text':
        if (args.editor):
            d = get_user_input(data_req['text'], prevs_data)
            post_data['title'] = d['title']
            post_data['body'] = d['body']
        else:
            console_input = get_post_data(data_req['text'])
            post_data['title'] = console_input['title']
            post_data['body'] = console_input['body']
    elif post_type == 'video':
        data_req = ['caption', 'url']
        console_input = get_post_data(data_req)
        post_data['caption'] = console_input['caption']
        post_data['embed'] = console_input['url']
    elif post_type == 'quote':
        data_req = ['quote', 'source']
        console_input = get_post_data(data_req)
        post_data['quote'] = console_input['quote_text']
        post_data['source'] = console_input['source']   # source of quote
    elif post_type == 'audio':
        data_req = ['caption', 'external_url']
        console_input = get_post_data(data_req)
        post_data['caption'] = console_input['caption']
        post_data['external_url'] = console_input['args.url']
    elif post_type == 'link':
        console_input = get_post_data(data_req['link'])
        post_data['url'] = console_input['url']
        post_data['title'] = console_input['title']
        post_data['description'] = console_input['description']
    elif post_type == 'photo':
        post_data['source'] = console_input['url']                  # link to file
        post_data['data'] = console_input['file']
        post_data['caption'] = console_input['caption']
    else:
        print "Unsupported post type found!"


    r = teblr.edit_post(blog_name, post_data)
    
    if 'meta' in r and 'errors' in r['response']:
        print str(r['meta']['status']) + " status code returned! "+ str(r['response']['errors'])
    else:
        print "Your post has been updated!"


def delete_action(args):
    if args.blog:
        blog_name = args.blog
    else:
        blog_name = get_blog_name()
    
    print 'Deleting...'
    r = teblr.delete_post(blog_name, args.post_id)
    
    if 'meta' in r and 'errors' in r['response']:
        print str(r['meta']['status']) + " status code returned! "+ str(r['response']['errors'])
    else:
        print "Done. Deleted!"


def create_client():
    return console.setup()


def get_user_input(input_list, prevs=None):
    initial_msg = ""
    d = dict()
    LINE_LENGTH = 50

    for i in range(0, len(input_list)):
        if not prevs:
            initial_msg += input_list[i] + ": \n"
        else:
            initial_msg += input_list[i] + ": " + prevs[input_list[i]]
        # don't print the line after last element
        if i != len(input_list)-1:
            initial_msg += '-'*LINE_LENGTH + "\n"

    print "Choosing default editor from $EDITOR..."
    editor = os.environ.get('EDITOR', 'nano')

    if not editor:
        exit("Editor not found! Please set a default editor.")
    
    try:
        with tempfile.NamedTemporaryFile(suffix='.tmp') as tf:
            tf.write(initial_msg)
            tf.flush()
            call([editor, tf.name])
            tf.seek(0)
            edited_msg = tf.read()
    except:
        exit("Unknown problem occurred while processing temporary file!")

    edited_msg = edited_msg.split('-'*LINE_LENGTH)
    
    if len(edited_msg) != len(input_list):
        exit("Invalid file format!")
    
    for i in range(0, len(input_list)):
            edited_msg[i] = edited_msg[i][len(input_list[i])+2 :]
    for i in range(0, len(edited_msg)):
        d[input_list[i]] = edited_msg[i]

    return d


def get_post_data(details_list):
    data = {}   # dictionary for holding data
    for detail in details_list:
        data[detail] = raw_input("Enter " + detail + ": ")
    return data


def get_blog_name(no_defaults=False):
    global default_blog
    if not no_defaults:
        if default_blog != None:
            return default_blog

    print "Fetching blogs..."
    try:
        blogs = teblr.client.info()['user']['blogs']
        print('Please choose a blog')
        if len(blogs) > 1:
            # print the available blogs
            for i in range(0, len(blogs)):
                print str(i+1) + ". "  + str(blogs[i]['name']) + " ("+str(blogs[i]['url'])+")"
            # take the choice of blog to post
            choice = raw_input("Enter choice (default 1): ")
            if not choice:
                blog_num = 0
            else:
                blog_num = int(choice) - 1
        else:
            blog_num = 0
    except:
        exit("Blog details fetch failed. Check your internet connection!")
    
       
    return blogs[blog_num]['name']


def extract_post(blog, post_id):
    params = {}
    params['id'] = post_id
    params['api_key'] = console.key
    url = "https://api.tumblr.com/v2/blog/"+ blog +"/posts/text" 
    url = url + "?" + urllib.urlencode(params)
    try:
        response = urllib2.urlopen(url)
        parsed = json.load(response)
    except:
        exit("Post data extraction failed. Check your internet connection!")
    
    post_data = parsed['response']['posts'][0]
    # format if required post_data
    return post_data


def set_action(args):
    if args.default_blog:
        yaml_path = os.path.expanduser('~') + '/.tumblr'
        yaml_file = open(yaml_path, 'r')
        tokens = yaml.safe_load(yaml_file)
        yaml_file.close()
        default_blog = get_blog_name(True)
        tokens['default_blog'] = default_blog.encode('ascii', 'ignore')
        yaml_file = open(yaml_path, 'w+')
        yaml.dump(tokens, yaml_file, indent=2)
        yaml_file.close()
        print "Your default blog has been set!"
    if args.setup:
        print "Initializing fresh setup..."
        path = os.path.expanduser('~') + '/.tumblr'
        os.remove(path)
        console.setup()
        print "Setup finished!"


def args_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='ACTION help', metavar='ACTION')

    # set command arguments
    parser_set = subparsers.add_parser('set', help='set help')
    set_group = parser_set.add_mutually_exclusive_group(required=True)
    set_group.add_argument('-db', '--default-blog', action='store_true',
            help='Set default blog for your actions')
    set_group.add_argument('-su', '--setup', action='store_true',
            help='Use this to run fresh setup')
    parser_set.set_defaults(func=set_action)

    # post command arguments
    parser_post = subparsers.add_parser('post', help='post help')
    post_group = parser_post.add_mutually_exclusive_group(required=True)
    post_group.add_argument('--photo', action='store_true',
            help='Post a photo to your blog')
    post_group.add_argument('--text', action='store_true',
            help='Post text to your blog')
    post_group.add_argument('--quote', action='store_true',
            help='Post a quote to your blog')
    post_group.add_argument('--link', action='store_true',
            help='Post a link to your blog')
    post_group.add_argument('--audio', action='store_true',
            help='Post an audio to your blog')
    post_group.add_argument('--video', action='store_true',
            help='Post a video to your blog')

    # post option - file source 
    file_source_group = parser_post.add_mutually_exclusive_group()
    file_source_group.add_argument('-u','--url', 
            help='URL of the data, if any. Available for: photo, audio, video, link posts')
    file_source_group.add_argument('-f','--file', 
            help='Path to the file, if any. Available for: photo, audio, video posts')

    # post option = post state
    post_state_group = parser_post.add_mutually_exclusive_group()
    post_state_group.add_argument('--private', action='store_const', help='Set post visibility to only you', dest='state', const='private')
    post_state_group.add_argument('--draft', action='store_const', const='draft', help='Add post to drafts', dest='state')
    post_state_group.add_argument('--queue', action='store_const', const='queue', help='Add post to queue', dest='state')

    # post options
    parser_post.add_argument('-d','--date', 
            help='Custom post date: dd-mm-yyyy')
    parser_post.add_argument('-c','--caption',
            help='Post caption, if any Available for: photo, audio, video posts')
    parser_post.add_argument('-e','--editor', action='store_true',
            help='Open default editor for writing your post. Available for: text posts')
    parser_post.add_argument('-s','--source',
            help='Source of the post, if any. Available for: quote posts')
    parser_post.add_argument('-q','--quote-text',
            help='Add quote text as argument. Available for: quote posts')
    parser_post.add_argument('-b', '--blog', help='Mention blog to post content.')
    parser_post.set_defaults(func=post_action)

    # edit command arguments
    parser_edit = subparsers.add_parser('edit',
            help='edit help')
    parser_edit.add_argument('-p', '--post-id', required=True,
            help='ID of the post that has to be edited')
    parser_edit.add_argument('-e','--editor', action='store_true',
            help='Open default editor for editing your post. Available for: text posts')
    parser_edit.add_argument('-b', '--blog', help='Mention blog to edit content.')
    parser_edit.set_defaults(func=edit_action)

    # delete command arguments
    parser_delete = subparsers.add_parser('delete',
            help='delete help')
    parser_delete.add_argument('-p','--post-id', required=True,
            help='ID of the post that has to be deleted')
    parser_delete.add_argument('-b', '--blog', help='Mention blog to delete content.')
    parser_delete.set_defaults(func=delete_action)

    return parser.parse_args()

def parse_date(date):
    try:
        datetime.datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        raise ValueError("Incorrect date format, should be dd-mm-yyyy")

    # minyear = 1900
    # maxyear = datetime.date.today().year

    date = date.split('-')
    if len(date) == 3 and len(date[2]) == 4 and len(date[0]) == 2 and len(date[1] == 2):
        return date

