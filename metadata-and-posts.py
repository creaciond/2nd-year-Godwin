import requests
import os
import re
import html

'''
                COMMON METHODS
'''
# clean lines from junk
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
    if os.path.exists(old_route):
        with open(old_route, 'a', encoding='utf-8') as f_write:
            for post in new_posts:
                if not post in posts:
                    post = post + '\n'
                    f_write.write(post)
    else:
        with open(old_route, 'w', encoding='utf-8') as f_write:
            for post in new_posts:
                if not post in posts:
                    post = post + '\n'
                    f_write.write(post)


# metadata retrieval
def group_info(domains, group_meta):
    params = {'group_id': '', 'version': '5.62', 'fields': 'members_count, screen_name'}
    for domain in domains:
        # making a query to API
        params['group_id'] = domain
        response = requests.get('https://api.vk.com/method/groups.getById', params=params)
        group_json = response.json()['response'][0]
        # adding group information
        group_dict = {'domain': domain, 'group_id': int(group_json['gid']), 'members_count': int(group_json['members_count'])}
        # adding information to list of group_dicts
        group_meta.append(group_dict)
    return group_meta

'''
                    POSTS
'''
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
    # print('I\'m writing posts')
    parameters = {'version': '5.62', 'owner_id': '', 'count': '100'}
    for group in groups_meta:
        # posts retrieval
        parameters['owner_id'] = '-' + str(group['group_id'])
        response = requests.get('https://api.vk.com/method/wall.get', params=parameters)
        # work with posts:
        new_posts = get_new_posts(response)
        # save posts
        if os.path.exists(group['domain'] + '_posts.csv'):
            save_new_info(group['domain'] + '_posts.csv', new_posts)
        else:
            # this is the first time we're writing something — no old_posts
            with open(group['domain'] + '_posts.csv', 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted(new_posts)))

'''
                    COMMENTS
'''
# =============     Information about commentators      =============
def get_user_info(user_id):
    print('I\'m getting user info!')
    parameters = {'version': '5.62', 'user_ids': user_id, 'fields': 'bdate, city, country, home_town, universities'}
    response = requests.get('https://api.vk.com/method/wall.users.get', params=parameters)
    if response:
        try:
            print(response.json())
        except:
            user_data = ''


# =============     Comments    =============
def get_comments(group_info):
    # for particular group
    comments = set()
    owner_id = '-' + str(group_info['group_id'])
    parameters = {'version': '5.62', 'owner_id': owner_id, 'post_id': '', 'count': '100'}
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
                            comment_array = response.json()['response']
                            # comment_array[0] — comment total count
                            for i in range(1, comment_array[0]):
                                if not clean_line(comment_array[i]['text']) == '':
                                    comment = post_id + ',' + clean_line(comment_array[i]['text'])
                                    comments.add(comment)
                    except:
                        comments = set()
                save_new_info(group_info['domain'] + '_comments.csv', comments)
    except:
        comments = []


'''
                    MAIN
'''
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