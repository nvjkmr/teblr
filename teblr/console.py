#!/usr/bin/python

# https://github.com/tumblr/pytumblr/blob/master/interactive_console.py

import pytumblr
import yaml
import os
import urlparse
import code
import oauth2 as oauth
import teblr
import helpers

global key
TOTAL_TOKENS = 5

def new_oauth(yaml_path):
    '''
    Return the consumer and oauth tokens with three-legged OAuth process and
    save in a yaml file in the user's home directory.
    '''

    print "Please set up teblr before start using it. Don't worry, we will guide you through this!"
    print '''
    Go to http://www.tumblr.com/oauth/apps and click on 'Register application':
    ------------------------------------
    Register using the following details:
    ====================================
    Application name: Teblr
    Application Website: http://nvijaykumar.me/teblr
    Application Description: Tumblr on terminal written in Python
    Administrative contact email: <YOUR-EMAIL-ID>
    Default callback URL: http://nvijaykumar.me/teblr/
    ====================================
    '''
    print 'Retrieve OAuth Consumer Key and Secret Key in the application details'
    consumer_key = raw_input('Paste the consumer key here: ')
    consumer_secret = raw_input('Paste the consumer secret here: ')

    request_token_url = 'http://www.tumblr.com/oauth/request_token'
    authorize_url = 'http://www.tumblr.com/oauth/authorize'
    access_token_url = 'http://www.tumblr.com/oauth/access_token'

    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)

    # Get request token
    resp, content = client.request(request_token_url, "POST")
    request_token =  urlparse.parse_qs(content)

    # Redirect to authentication page
    print '\nPlease go here and authorize:\n%s?oauth_token=%s' % (authorize_url, request_token['oauth_token'][0])
    redirect_response = raw_input('Click on \'Allow\' then paste the full redirect URL here:\n')

    # Retrieve oauth verifier
    url = urlparse.urlparse(redirect_response)
    query_dict = urlparse.parse_qs(url.query)
    oauth_verifier = query_dict['oauth_verifier'][0]

    # Request access token
    token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'][0])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = urlparse.parse_qs(content)

    # default blog
    print "\nPlease select a default blog! All your changes will be made to your default blog.\nYou can change the default blog using '-db' flag or specify a blog with '-b' flag at every action.\nFor more, see --help.\n"

    teblr.client = pytumblr.TumblrRestClient(
            consumer_key,
            consumer_secret,
            access_token['oauth_token'][0],
            access_token['oauth_token_secret'][0]
            )

    helpers.default_blog = helpers.get_blog_name(True)

    tokens = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'oauth_token': access_token['oauth_token'][0],
        'oauth_token_secret': access_token['oauth_token_secret'][0],
        'default_blog' : helpers.default_blog.encode('ascii', 'ignore')
    }

    yaml_file = open(yaml_path, 'w+')
    yaml.dump(tokens, yaml_file, indent=2)
    yaml_file.close()

    return tokens

def setup():
    yaml_path = os.path.expanduser('~') + '/.tumblr'

    if not os.path.exists(yaml_path):
        try:
            tokens = new_oauth(yaml_path)
        except:
            exit("Unknown error occurred! Couldn't fetch tokens")
    else:
        yaml_file = open(yaml_path, "r")
        tokens = yaml.safe_load(yaml_file)
        yaml_file.close()

    # check availability of all tokens
    if (len(tokens) != TOTAL_TOKENS):
        try:
            tokens = new_oauth(yaml_path)
        except:
            exit("Unknown error occurred! Couldn't fetch tokens")

    client = pytumblr.TumblrRestClient(
        tokens['consumer_key'],
        tokens['consumer_secret'],
        tokens['oauth_token'],
        tokens['oauth_token_secret']
    )

    global key
    key = tokens['consumer_key']
    helpers.default_blog = tokens['default_blog']

    return client
