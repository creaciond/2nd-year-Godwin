import os
import re


def redo_csvs(csv_name):
    path = './' + csv_name
    new_entries = set()
    reg_post_id = re.compile('([0-9]+)?,', flags = re.DOTALL)
    reg_post = re.compile('[0-9]+?,(.*)?\n', flags = re.DOTALL)
    with open(path, 'r', encoding='utf-8') as csv:
        entries = csv.readlines()
        for entry in entries:
            try:
                post_id = str(re.search(reg_post_id, entry).group(1))
                post = str(re.search(reg_post, entry).group(1))
                new_entry = post_id + '\t' + post + '\n'
                if new_entry not in new_entries:
                    new_entries.add(new_entry)
            except:
                print(entry)
    new_path = path.replace('.csv', '.tsv')
    with open(new_path, 'w', encoding='utf-8') as new_file:
        for item in new_entries:
            new_file.write(item)


def main():
    for item in os. listdir('.'):
        if item.endswith('.csv'):
            redo_csvs(item)


if __name__ == '__main__':
    main()