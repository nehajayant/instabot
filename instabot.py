import requests     , urllib

APP_ACCESS_TOKEN = "5693142402.e0dc839.0b42eb38f2ae433abb97322121078d93"
BASE_URL ='https://api.instagram.com/v1/'
a=[]


def self_info():
    request_url=(BASE_URL + "users/self/?access_token=%s") % (APP_ACCESS_TOKEN)
    print 'GET request url:%s' % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username:%s' % (user_info['data']['username'])
            print 'No. of followers:%s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts:%s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'



def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url:%s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()



def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url :%s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username:%s' % (user_info['data']['username'])
            print 'No. of followers:%s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following:%s' % (user_info['data']['counts']['follows'])
            print 'No. of posts:%s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'



def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name= own_media['data'][0]['id'] + ".jpeg"
            image_url =  own_media['data'][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)
            print"your image has been downloaded"
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'



def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + ".jpeg"
            image_url = user_media['data'][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)

        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


def search_by_tag():
    tag = raw_input("Search by tags. Enter any tag:\n")
    print "Get request Url:" + ((BASE_URL + "tags/%s/media/recent?access_token=%s")) % (tag, APP_ACCESS_TOKEN)
    hashtag = requests.get(((BASE_URL + "tags/%s/media/recent?access_token=%s")) % (tag, APP_ACCESS_TOKEN)).json()
    if hashtag["meta"]["code"] == 200:
        if len(hashtag["data"]):
            for i,d in enumerate(hashtag["data"]):
                print d["id"]
                a.append(d["id"])
            return a
        else:
            print "there is no such hashtag"
    else:
        print "Recieved status code is not 200"


def post_a_comment_by_hashtag():
    media_id = search_by_tag()
    comment = raw_input("comment?:")
    data = {"access_token": APP_ACCESS_TOKEN, "text": comment}
    for i in media_id:
        request_for_comment= (BASE_URL + "media/%s/comments") % (i)
        print "POST request URL: %s" % (request_for_comment)
        comment_on_post=requests.post(request_for_comment,data).json()
        if comment_on_post["meta"]["code"] == 200:
            print "Comment done"
        else:
            print"Comment was unsuccessful"




def start_bot():
    while True:
        print '\n'
        print "Hey! Welcome to instaBot!\nHere are your menu options:\n" \
              "a.Get your own details\n\nb.Get details of a user by username\n\n" \
              "c.Get your recent post\n\nd.Get recent post of any user\ne.like a post\nf.comment on a post\n" \
              "g. Commenting by hashtags"
        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice== "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice == "g":
            post_a_comment_by_hashtag()

start_bot()