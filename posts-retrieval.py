import requests
import os
import json


def getNewPosts(response, oldPosts):
    newPosts = []
    for item in response.json()['response']:
        try:
            if item['post_type'] == 'post':
                # all text in one line instead of many lines
                item['text'] = item['text'].replace('\n', ' ')
                post = '%s,%d,%s\r\n' % (item['post_type'], item['id'], item['text'])
        except:
            post = ''
        # if post is not already in newPosts, we append it
        if (post not in oldPosts) and (post):
            newPosts.append(post)
    return newPosts


def writePosts(groupIDs):
    parameters = {'version': '5.60', 'domain': '', 'count': '100'}
    for groupID in groupIDs:
        # posts retrieval
        parameters['domain'] = groupID
        response = requests.get('https://api.vk.com/method/wall.get', params=parameters)

        # work with posts
        # load older posts (if any)
        if os.path.exists(groupID+'_posts.csv'):
            with open(groupID+'_posts.csv', 'r', encoding='utf-8') as f:
                oldPosts = f.readlines()
        else:
            oldPosts = []
        # get new posts (those which are already in the file will be removed)
        newPosts = getNewPosts(response, oldPosts)
        # save new posts (if any)
        if newPosts:
            if os.path.exists(groupID+'_posts.csv'):
                with open(groupID+'_posts.csv', 'a', encoding='utf-8') as f:
                    for post in newPosts:
                        f.write(post)
            else:
                with open(groupID+'_posts.csv', 'w', encoding='utf-8') as f:
                    for post in newPosts:
                        f.write(post)

        # just in case: write JSON to file
        with open(groupID+'.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(response.json(), indent=4))



def main():
    groupIDs = ['meduzaproject', 'oldlentach', 'noolhistorical']
    writePosts(groupIDs)


if __name__ == '__main__':
    main()
