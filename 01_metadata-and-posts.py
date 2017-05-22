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
    # if file already existed
    if os.path.exists(old_route):
        with open(old_route, 'r', encoding='utf-8') as f_read:
            posts = set(f_read.readlines())
        with open(old_route, 'a', encoding='utf-8') as f_write:
            for post in new_posts:
                if not post in posts:
                    post = post + '\n'
                    f_write.write(post)
    # file doesn't exist
    else:
        with open(old_route, 'w', encoding='utf-8') as f_write:
                f_write.write('\n'.join(new_posts))


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
def get_new_posts(response, group_info):
    newPosts = set()
    for item in response.json()['response']:
        try:
            if item['post_type'] == 'post':
                # all text in one line instead of many lines
                item['text'] = item['text'].replace('\n', ' ')
                post = '$s\t%s\t%d\t%s' % (group_info['group_id'], item['post_type'], item['id'], clean_line(item['text']))
                if not post == '':
                    newPosts.add(clean_line(post))
        except:
            post = ''
    return newPosts


def api_posts(posts, parameters, offset):
    parameters['offset'] = offset
    link = 'https://api.vk.com/method/wall.get'
    response = requests.get(link, parameters)
    if response:
        for i in range(1, len(response.json()['response'])):
            post = response.json()['response'][i]
            if post['post_type'] == 'post':
                '''
                    group_id = parameters['owner_id'].strip('-')
                    post_id = post['id']
                '''
                line = '%s\t%d\t%s' % (parameters['owner_id'].strip('-'), post['id'], clean_line(post['text']))
                posts.add(line)
    return posts


def write_posts(group_meta):
    parameters = {'version': '5.62', 'owner_id': '', 'count': '100'}
    # 1) POSTS RETRIEVAL
    parameters['owner_id'] = '-' + str(group_meta['group_id'])
    response = requests.get('https://api.vk.com/method/wall.get', params=parameters)
    # 2) WORK WITH POSTS
    if response:
        posts = set()
        if response.json()['response'][0] > 100:
            for i in range(response.json()['response'][0] % 100 + 1):
                posts = api_posts(posts, parameters, i*100)
            else:
                posts = api_posts(posts, parameters, 0)
            # 3) SAVE POSTS (if any)
        with open('./data/' + group_meta['domain'] + '_posts.tsv', 'w', encoding='utf-8') as f:
           f.write('\n'.join(sorted(posts)))

'''
                    COMMENTS
'''


def get_post_ids(domain):
    path = './data/' + domain + '_posts.tsv'
    post_ids_ar = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for post in f.readlines():
                post_ids_ar.append(post.split('\t')[1])
    return post_ids_ar


def api_comments(set_comments, params, offset):
    params['offset'] = offset
    link = 'https://api.vk.com/method/wall.getComments'
    response = requests.get(link, params=params)
    if response:
        for i in range(1, len(response.json()['response'])):
            comment = response.json()['response'][i]
            '''
                group_id = params['owner_id']
                from whom is the comment — comment['from_id']
                text of the comment — comment['text']
            '''
            line = params['owner_id'] + '\t' + str(comment['from_id']) + '\t' + comment['text']
            set_comments.add(line)
    return set_comments


# for particular group
def get_comments(group_info):
    comments = set()
    owner_id = '-' + str(group_info['group_id'])
    parameters = {'version': '5.62', 'owner_id': owner_id, 'post_id': '', 'count': '100'}
    post_ids = get_post_ids(group_info['domain'])
    count = 0
    for post_id in post_ids:
        count += 1
        parameters['post_id'] = post_id
        response = requests.get('https://api.vk.com/method/wall.getComments', params=parameters)
        if response.json()['response'][0] > 100:
            for i in range(response.json()['response'][0] % 100 + 1):
                comments = api_comments(comments, parameters, i*100)
        else:
            # offset = 0
            comments = api_comments(comments, parameters, 0)
    save_new_info('./data/' + group_info['domain'] + '_comments.tsv', comments)


'''
                    MAIN
'''
def main():
    domains = ['meduzaproject', 'oldlentach', 'noolhistorical']
    # groups_meta — list with dictionaries containing metadata of groups
    groups_meta = []
    groups_meta = group_info(domains, groups_meta)
    for group_meta in groups_meta:
        write_posts(group_meta)
        get_comments(group_meta)


if __name__ == '__main__':
    main()