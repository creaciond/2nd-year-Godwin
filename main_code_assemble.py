import os


def main():
    os.system('python ./01_metadata-and-posts.py')
    os.system('python ./02_get-data-from-json.py')
    os.system('./03_godwins-law-cases.py')
    os.system('./04_info-users.py')


if __name__ == '__main__':
    main()