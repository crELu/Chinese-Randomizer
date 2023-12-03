from random import sample
import os
import csv

CHARACTERS = 0
TRADITIONAL_CHARS = 1
TONES = 2
DEFINITIONS = 3

CSV_ID = 'ID'
CSV_SIMP = 'Chinese'
CSV_TRAD = 'Trad.'
CSV_PINYIN = 'Pinyin'
CSV_DEF = 'Definition'

EXIT = 'e'
COMBINE = 'c'

lessons_cache = {}


def combine():
    directory_name = 'Vocab'
    combined_name = f'{directory_name}/Lesson_Combined_Vocab.csv'
    directory = os.listdir(directory_name)
    has_header = False
    rows = []
    lesson = 2
    with open(combined_name, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        for file_name in directory:
            if file_name != combined_name:
                with open(f'{directory_name}/{file_name}', encoding='utf8') as data:
                    reader = csv.reader(data, delimiter=',')
                    if not has_header:
                        has_header = True
                    else:
                        headers = next(reader, None)
                    for row in reader:
                        rows.append([str(lesson)] + row)
                    lesson += 1
        rows[0].insert(0, '\ufeffLesson')
        writer.writerows(rows)


def read_lesson(lesson_num):
    if lesson_num in lessons_cache:
        return lessons_cache[lesson_num]
    try:
        with open(f'Vocab/Lesson_{lesson_num}_Vocab.csv', 'r', encoding='utf8') as f:
            reader = csv.DictReader(f, delimiter=',')
            characters = []
            traditional_chars = []
            tones = []
            definitions = []
            for row in reader:
                characters.append(row[CSV_SIMP])
                traditional_chars.append(row[CSV_TRAD])
                tones.append(row[CSV_PINYIN])
                definitions.append(row[CSV_DEF])
            lessons_cache[lesson_num] = (characters, traditional_chars, tones, definitions)
            return lessons_cache[lesson_num]
    except FileNotFoundError:
        return


if __name__ == '__main__':
    # Set Windows terminal to be able to display Chinese Characters
    os.system('chcp 936')
    command = None
    lesson = None
    while command != EXIT:
        while command is None:
            command = input(f'Enter a lesson number (>=2) or \'c\' to combine vocab files or \'e\' to exit: ')
            if command == EXIT:
                exit()
            elif command == COMBINE:
                combine()
                command = None
            else:
                try:
                    command = lesson_num = int(command)
                    lesson = read_lesson(lesson_num)
                    if lesson is None:
                        raise ValueError
                except ValueError:
                    print('Invalid input. Lesson does not exist.')
                    command = None

        num_characters = len(lesson[CHARACTERS])
        order = sample(range(1, num_characters + 1), num_characters)
        print('Write in this order: ' + str(order))
        print('====================================\nDefinitions\n====================================')
        print('Keep pressing enter to get next character:')
        for i in order:
            input()
            print(f'====================================\n\n{i}: ', end='')
            i -= 1
            print(lesson[DEFINITIONS][i])
        input()
        print('====================================\nAnswers\n====================================')
        for i in order:
            input()
            print(f'====================================\n\n{i}: ', end='')
            i -= 1
            character = lesson[CHARACTERS][i]
            if character != lesson[TRADITIONAL_CHARS][i]:
                character += ' [' + lesson[TRADITIONAL_CHARS][i] + ']'
            print(character)
            print(lesson[TONES][i])
        print('\n====================================')
        command = None
