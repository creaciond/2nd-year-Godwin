import requests
import os
import re
import html


# ============= Metadata retrieval =============
def group_info(domains, group_meta):
    params = {'group_id': '', 'version': '5.62', 'fields': 'members_count, screen_name'}
    for domain in domains:
        # making a query to API
        params['group_id'] = domain
        response = requests.get('https://api.vk.com/method/groups.getById', params=params)
        group_json = response.json()['response'][0]
        # adding group information
        group_dict = {'domain': '', 'group_id': 0, 'members_count': 0}
        group_dict['domain'] = domain
        group_dict['group_id'] = int(group_json['gid'])
        group_dict['members_count'] = int(group_json['members_count'])
        # adding information to list of group_dicts
        group_meta.append(group_dict)
    return group_meta


def clean_line(line):
    regTag = re.compile('<.*?>', flags=re.DOTALL)
    regLink = re.compile('https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,}', flags=re.DOTALL)
    regName = re.compile('\[id[0-9]+?|.*?\], ', flags=re.DOTALL)
    regHashtag = re.compile('#.? ', flags=re.DOTALL)
    line = regTag.sub('', line)
    line = regLink.sub('', line)
    line = regName.sub('', line)
    line = regHashtag.sub('', line)
    line = html.unescape(line)
    return line


def save_new_info(old_route, new_posts):
    with open(old_route, 'r', encoding='utf-8') as f_read:
        posts = set(f_read.readlines())
    with open(old_route, 'a', encoding='utf-8') as f_write:
        for post in new_posts:
            if not post in posts:
                f_write.write(post)


# =============     New posts    =============
def get_new_posts(response):
    newPosts = set()
    for item in response.json()['response']:
        try:
            if item['post_type'] == 'post':
                # all text in one line instead of many lines
                item['text'] = item['text'].replace('\n', ' ')
                post = '%s,%d,%s' % (item['post_type'], item['id'], item['text'])
                if not post == '':
                    newPosts.add(clean_line(post))
        except:
            post = ''
    return newPosts


def write_posts(groups_meta):
    parameters = {'version': '5.62', 'owner_id': '', 'count': '100'}
    for group in groups_meta:
        # posts retrieval
        parameters['owner_id'] = '-' + str(group['group_id'])
        response = requests.get('https://api.vk.com/method/wall.get', params=parameters)
        # work with posts:
        new_posts = get_new_posts(response)
        # 3. save posts
        if os.path.exists(group['domain'] + '_posts.csv'):
            save_new_info(group['domain'] + '_posts.csv', new_posts)
        else:
            # this is the first time we're writing something — no old_posts
            with open(group['domain'] + '_posts.csv', 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted(new_posts)))


# =============     Information about commentators      =============
def get_user_info(user_id):
    parameters = {'version': '5.62', 'user_ids': user_id, 'fields': 'bdate, city, country, home_town, universities'}
    response = requests.get('https://api.vk.com/method/wall.users.get', params=parameters)
    if response:
        try:
            print(response.json())
        except:
            user_data = ''


# =============     Comments    =============
def save_comments(comments, group_id):
    if os.path.exists(group_id + '_comments.csv'):
        save_new_info(group_id + '_comments.csv', comments)
    else:
        with open(group_id + '_comments.csv', 'w', encoding='utf-8') as f:
            for comment in comments:
                f.write(comment)



def get_comments(group_info):
    comments = []
    group_id = '-'+str(group_info['group_id'])
    parameters = {'version': '5.62', 'owner_id': group_id, 'post_id': '', 'count': '100'}
    try:
        if os.path.exists(group_info['domain'] + '_posts.csv'):
            with open(group_info['domain'] + '_posts.csv', 'r', encoding='utf-8') as f:
                posts = f.readlines()
                for post in posts:
                    post_id = post.split(',')[1]
                    try:
                        parameters['post_id'] = post_id
                        response = requests.get('https://api.vk.com/method/wall.getComments', params=parameters)
                        if response:
                        # if response.status_code() == 200:
                            comment_array = response.json()['response']
                            # comment_array[0] -- comment total count
                            for i in range(1, comment_array[0]):
                                print('%d, %s' % (post_id, clean_line(comment_array[i]['text'])))
                                comments.append(comment_array[i]['text'])
                    except:
                        print('no comments :C')
                    save_comments(comments, group_info['domain'])
    except:
        comments = ''



def main():
    domains = ['meduzaproject', 'oldlentach', 'noolhistorical']
    # groups_meta — list with dictionaries containing metadata of groups
    groups_meta = []
    groups_meta = group_info(domains, groups_meta)
    # write_posts(groups_meta)
    for group_meta in groups_meta:
        get_comments(group_meta)


if __name__ == '__main__':
    main()