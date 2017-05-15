import os
import re


def nazi_regex():
    # Nazi highest ranks regular expressions
    hitler_regex = re.compile('[Гг]итлер', flags=re.DOTALL)
    hebbels_regex = re.compile('[Гг]ебб?ельс]', flags=re.DOTALL)
    himmler_regex = re.compile('[Гг]имм?лер]', flags=re.DOTALL)
    nazi_regex = [hitler_regex, hebbels_regex, himmler_regex]
    # concentration camps regular expressions
    auschwitz_regex = re.compile('[Оо]свенцим', flags=re.DOTALL)
    buchenwald_regex = re.compile('[Бб]ухенвальд', flags=re.DOTALL)
    camps_regex = [auschwitz_regex, buchenwald_regex]
    return nazi_regex, camps_regex


def search_nazi(current_lines, lines, nazi_ar_regex, camps_ar_regex):
    for line in lines:
        line = line.strip('\n')
        # search for Nazi mentions
        has_nazi = any(re.search(regex, line) for regex in nazi_ar_regex)
        # search for concentration camps mentions
        has_camps = any(re.search(regex, line) for regex in camps_ar_regex)
        if has_nazi or has_camps:
            current_lines.add(line)
    return current_lines


def save_Godwins_lines(Godwins_lines):
    with open('./data/Godwins_lines.tsv', 'w', encoding='utf-8') as file_write:
        file_write.write('\n'.join(Godwins_lines))


def main():
    # generate regular expressions only once
    nazi, camps = nazi_regex()
    # matching lines will be stored here
    lines_Godwins_law = set()
    for file in os.listdir('./data'):
        if file.endswith('.tsv'):
            with open('./data/'+file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # the result stays in lines_Godwins_law (unique!)
                lines_Godwins_law = search_nazi(lines_Godwins_law, lines, nazi, camps)
    save_Godwins_lines(lines_Godwins_law)


if __name__ == '__main__':
    main()