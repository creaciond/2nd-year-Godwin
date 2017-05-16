import os
import json
import re
import html


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


def get_data_from_file(file_path):
    path = './data/comments/' + file_path
    with open(path, 'r', encoding='utf-8')as f:
        return f.read()


def data_from_dict(comments_dict, file_path):
    comments = set()
    posts = set()
    group_id = re.search('[0-9]+?\.', file_path)
    for post_id in comments_dict:
        for i in range(1, len(comments_dict[post_id])):
            comment_array = comments_dict[post_id][i]
            for comment in comment_array:
                comment_to_add = '%s\t%s\t%s' % (group_id, comment['from_id'], clean_line(comment['text']))
                if clean_line(comment['text']):
                    comments.add(comment_to_add)
            if comments_dict[post_id][0]['text']:
                post = '%s\t%s' % (post_id, clean_line(comments_dict[post_id][0]['text']))
                if clean_line(comments_dict[post_id][0]['text']) and post not in posts:
                    posts.add(post)
    return posts, comments


def data_update(group_id, data, data_json):
    for item in data_json:
        if item not in data:
            data.add(group_id + '\t' + item)
    return data


def write_data(data, filename):
    file = './data/' + filename + '.tsv'
    with open(file, 'w', encoding='utf-8') as f:
        for item in data:
            line = '\t' + item + '\n'
            f.write(line)


def main():
    comments_total = set()
    posts_total = set()
    for file in os.listdir('./data/comments'):
        if file.endswith('.json'):
            group_id = file.split('_-')[1].strip('\.json')
            comments_dict = json.loads(get_data_from_file(file))
            posts_json, comments_json = data_from_dict(comments_dict, file)
            comments_total = data_update(group_id, comments_total, comments_json)
            posts_total = data_update(group_id, posts_total, posts_json)
    write_data(comments_total, 'comments')
    write_data(posts_total, 'posts')


if __name__ == '__main__':
    main()