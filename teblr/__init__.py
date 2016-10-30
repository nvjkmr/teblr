import helpers
 
def make_post(blog_name, post_type, post_data):
    global client

    if post_type == 'text':
        resp = client.create_text(blog_name, **post_data)
    elif post_type == 'video':
        resp = client.create_video(blog_name, **post_data)
    elif post_type == 'quote':
        resp = client.create_quote(blog_name, **post_data)
    elif post_type == 'audio':
        resp = client.create_audio(blog_name, **post_data)
    elif post_type == 'link':
        resp = client.create_link(blog_name, **post_data)
    elif post_type == 'photo':
        resp = client.create_photo(blog_name, **post_data)
    else: 
        print "Unknow Post Type Found!"
        
    return resp


def edit_post(blog_name, post_id, post_data):
    global client
    return client.edit_post(blog_name, post_data['type'], post_id);


def delete_post(blog_name, post_id):
    global client
    return client.delete_post(blog_name, post_id)
