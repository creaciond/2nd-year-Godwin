import requests
import os
import re


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


# =============     New posts    =============
def clean_line(line):
    regTag = re.compile('<.*?>', flags=re.DOTALL)
    regLink = re.compile('https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,}', flags=re.DOTALL)
    line = regTag.sub('', line)
    line = regLink.sub('', line)
    return line


def get_new_posts(response):
    new_posts = set()
    for item in response.json()['response']:
        try:
            if item['post_type'] == 'post':
                # all text in one line instead of many lines
                item['text'] = item['text'].replace('\n', ' ')
                post = '%s,%d,%s' % (item['post_type'], item['id'], item['text'])
                new_posts.add(clean_line(post))
        except:
            post = ''
    return new_posts


def write_posts(groups_meta):
    parameters = {'version': '5.62', 'owner_id': '', 'count': '100'}
    for group in groups_meta:
        # posts retrieval
        parameters['owner_id'] = '-' + str(group['group_id'])
        response = requests.get('https://api.vk.com/method/wall.get', params=parameters)
        # work with posts:
        # 1. load older posts (if any)
        if os.path.exists(group['domain'] + '_posts.csv'):
            with open(group['domain']+'_posts.csv', 'r', encoding='utf-8') as f:
                old_posts = set(f.readlines())
        else:
            old_posts = set()
        # 2. add new posts to the older ones
        new_posts = get_new_posts(response)
        # 3. save posts
        if os.path.exists(group['domain'] + '_posts.csv'):
            with open(group['domain'] + '_posts.csv', 'a', encoding='utf-8') as f:
                for post in sorted(new_posts):
                    if post in old_posts:
                        new_posts.remove(post)
                f.write('\r\n'.join(sorted(new_posts)))
        else:
            # this is the first time we're writing something — no old_posts
            with open(group['domain'] + '_posts.csv', 'w', encoding='utf-8') as f:
                f.write('\r\n'.join(sorted(new_posts)))


def main():
    domains = ['meduzaproject', 'oldlentach', 'noolhistorical']
    # groups_meta — list with dictionaries containing metadata of groups
    groups_meta = []
    groups_meta = group_info(domains, groups_meta)
    write_posts(groups_meta)


if __name__ == '__main__':
    main()