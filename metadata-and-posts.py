import requests
import os
import json


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


def main():
    domains = ['meduzaproject', 'oldlentach', 'noolhistorical']
    # groups_meta — list with dictionaries containing metadata of groups
    groups_meta = []
    groups_meta = group_info(domains, groups_meta)


if __name__ == '__main__':
    main()