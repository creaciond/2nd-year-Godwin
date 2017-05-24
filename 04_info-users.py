import requests

# ========== Read file with posts ==========
def read_file(filepath):
    posts = []
    posts_and_and_group_ids = []
    with open(filepath, 'r', encoding='utf-8') as f_posts:
        for post in f_posts.readlines():
            post_separated = post.split('\t')
            # post_separated[0] -- group_id, post_separated[1] -- from_id
            if len(post_separated) == 3:
                posts_and_and_group_id = [post_separated[0], post_separated[1]]
                posts_and_and_group_ids.append(posts_and_and_group_id)
                posts.append(post)
    return posts, posts_and_and_group_ids


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
    parameters = {'version': '5.64', 'user_ids': '', 'fields': 'bdate, sex, city, country, home_town, universities'}
    users_info = []
    for i in range(len(posts_and_group_ids)):
        parameters['user_ids'] = str(posts_and_group_ids[i][0])
        link = 'https://api.vk.com/method/users.get'
        response = requests.get(link, params=parameters)
        # sex
        try:
            sex = response.json()['response'][0]['sex']
        except:
            sex = 'NaN'
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
            city = 'NaN'
        # Country retrieval
        try:
            if response.json()['response'][0]['country']:
                country = city_and_country(response.json()['response'][0]['city'], 'country')
        except:
            country = 'NaN'
        # All together
        user_data = [str(sex), str(age), city, country]
        data = '\t'.join(user_data)
        users_info.append(data)
    return users_info


# =========== Add information to posts ==========
def add_user_info(post, data):
    data = [str(data[i]) for i in range(1, len(data))]
    line = '\t' + '\t'.join(data)
    post_line = '\t'.join(post) + line
    return post_line


def update_posts(posts_array, user_data, fname):
    new_posts = []
    if len(posts_array) == len(user_data):
        for i in range(len(posts_array)):
            post = posts_array[i].strip('\n') + '\t' + user_data[i]
            new_posts.append(post)
            print(post)
    else:
        print('i\'ve got a fuckup')
    with open(fname, 'w', encoding='utf-8') as file:
        file.write('\n'.join(new_posts))


# =========== MAIN ==========
def main():
    file = './data/Godwins_lines.tsv'
    posts_ar, posts_info = read_file(file)
    users_info = get_info_users(posts_info)
    update_posts(posts_ar, users_info, file)


if __name__ == '__main__':
    main()