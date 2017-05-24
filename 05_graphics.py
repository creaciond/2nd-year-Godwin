import matplotlib.pyplot as plt
from matplotlib import style


def file_open(filename):
    posts_and_data = []
    lines = []
    with open(filename, 'r', encoding='utf-8') as f_read:
        lines = [line.strip('\n') for line in f_read.readlines()]
    for post in lines:
        data = post.split('\t')
        posts_and_data.append(data)
    # posts_and_data = [post.split('\t') for post in lines]
    return posts_and_data


def get_values(data, sex, age, city, country):
    for post in data:
        # sex
        if post[3] != 'NaN':
            if post[3] == '1':
                sex['female'] += 1
            else:
                sex['male'] += 1
        # age
        if post[4] != '':
            if post[4] not in set(age.keys()):
                age[post[4]] = 1
            else:
                age[post[4]] += 1
        # city
        if post[5] != 'NaN':
            if post[5] not in set(city.keys()):
                city[post[5]] = 1
            else:
                city[post[5]] += 1
        # country
        if post[6] != 'NaN':
            if post[6] not in set(country.keys()):
                city[post[6]] = 1
            else:
                city[post[6]] += 1
    return sex, age, city, country


def print_feature(feature_dict, type):
    keys = list(feature_dict.keys())
    values = list(feature_dict.values())
    rotation = 'vertical'
    plt.ylabel('Количество записей и комментариев')
    if type == 'sex':
        plt.title('Пол и закон Годвина')
        plt.xlabel('Пол: male — мужской, female — женский')
        rotation = 'horizontal'
    elif type == 'age':
        keys = sorted(list(feature_dict))
        values = [feature_dict[key] for key in keys]
        plt.title('Возраст и закон Годвина')
        plt.xlabel('Возраст оставивших запись/комментарий')
    elif type == 'city':
        keys = sorted(list(feature_dict))
        values = [feature_dict[key] for key in keys]
        plt.title('Город и закон Годвина')
        plt.xlabel('Родной город оставивших запись/комментарий')
    elif type == 'country':
        keys = sorted(list(feature_dict))
        values = [feature_dict[key] for key in keys]
        plt.title('Страна и закон Годвина')
        plt.xlabel('Родная страна оставивших запись/комментарий')
    plt.bar(range(len(keys)), values)
    plt.xticks(range(len(keys)), keys, rotation=rotation)
    plt.show()


def main():
    '''
        0) group_id  1) post_id 2) post    3)sex 4)age 5)city    6)country
        sex: NaN — not stated, 1 — female, 0 — male
        age: 0 — no age, else — int
        city: NaN — no city, else — str
        country: NaN — no country, else — str 
    '''
    data = file_open('./data/Godwins_lines.tsv')
    if data:
        # dictionaries for all possible values
        sex = {'male': 0, 'female': 0}
        age = {}
        city = {}
        country = {}
        sex, age, city, country = get_values(data, sex, age, city, country)
        print_feature(sex, 'sex')
        if len(list(age.keys())) > 1:
            print_feature(age, 'age')
        if city:
            print_feature(city, 'city')
        if country:
            print_feature(country, 'country')
    else:
        print('it ain\'t good')


if __name__ == '__main__':
    main()