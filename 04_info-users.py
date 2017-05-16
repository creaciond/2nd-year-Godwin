import requests

# ========== Read file with posts ==========
def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f_posts:
        posts = f_posts.readlines()
    posts_and_and_group_ids = []
    for post in posts:
        post_separated = post.split('\t')
        # post_separated[0] -- group_id, post_separated[1] -- from_id
        posts_and_and_group_id = {post_separated[0]:post_separated[1].strip('\n')}
        posts_and_and_group_ids.append(posts_and_and_group_id)
    return posts_and_and_group_ids


# =========== Get info about things ==========
def group_info(domain):
    parameters = {'group_id': domain, 'version': '5.62', 'fields': 'members_count, screen_name'}
    # making a query to API
    response = requests.get('https://api.vk.com/method/groups.getById', params=parameters)
    group_json = response.json()['response'][0]
    # adding group information
    group_id = int(group_json['gid'])
    return group_id


def city_and_country(object_id, type):
    if object_id:
        # API link varies on city/country
        if type == 'city':
            link = 'https://api.vk.com/method/database.getCitiesById'
            parameters = {'version' : '5.64', 'city_ids' : object_id}
        else:
            link = 'https://api.vk.com/method/database.getCountriesById'
            parameters = {'version': '5.64', 'country_ids': object_id}
        # API query
        response = requests.get(link, params=parameters)
        # Query result
        result = response.json()['response'][0]['name']
    else:
        result = ''
    return result


def get_info_users(posts_and_group_ids):
    parameters = {'version': '5.64', 'user_ids': '', 'fields': 'bdate, city, country, home_town, universities'}
    users_info = {}
    for post in posts_and_group_ids:
        parameters['user_ids'] = str(posts_and_group_ids[post])
        link = 'https://api.vk.com/method/users.get'
        response = requests.get(link, params=parameters)
        # Age retrieval
        try:
            if len(response.json()['response'][0]['bdate'].split('.')) == 3:
                age = 2017 - int(response['response'][0]['bdate'].split('.')[2])
            else:
                age = 0
        except:
            age = 0
        # City retrieval
        try:
            if response.json()['response'][0]['city']:
                city = city_and_country(response.json()['response'][0]['city'], 'city')
        except:
            city = ''
        # Country retrieval
        try:
            if response.json()['response'][0]['country']:
                country = city_and_country(response.json()['response'][0]['city'], 'country')
        except:
            country = ''
        # All together
        data = [str(post[0]), age, city, country]
        users_info['\t'.join(post)] = data
    return users_info


# =========== Add information to posts ==========
def add_user_info(post, data):
    data = [str(data[i]) for i in range(1, len(data))]
    line = '\t' + '\t'.join(data)
    post_line = '\t'.join(post) + line
    return post_line


def update_posts(posts, user_data, fname):
    filename = './data/' + fname
    posts_string = []
    for i in range(len(posts)):
        if i < len(user_data):
            user = list(user_data.keys())[i]
            post_string = add_user_info(posts[i], user_data[user])
            posts_string.append(post_string)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join(posts_string))


# =========== MAIN ==========
def main():
    file = './data/Godwins_lines.tsv'
    posts = read_file(file)
    users_info = get_info_users(posts)
    update_posts(posts, users_info, './data/Godwins_lines.tsv')


if __name__ == '__main__':
    main()