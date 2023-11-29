from random import sample
import os
import csv

character_tones = ['ā', 'ó', 'ě', 'ì', 'u']

CHARACTERS = 0
TRADITIONAL_CHARS = 1
TONES = 2
DEFINITIONS = 3

CSV_ID = 'ID'
CSV_SIMP = 'Chinese'
CSV_TRAD = 'Trad.'
CSV_PINYIN = 'Pinyin'
CSV_DEF = 'Definition'


def read_lesson(lesson_num):
    try:
        with open(f'Lesson_{lesson_num}_Vocab.csv', 'r', encoding='utf8') as f:
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
            return characters, traditional_chars, tones, definitions
    except FileNotFoundError:
        return


if __name__ == '__main__':
    os.system('chcp 936')
    EXIT = 'e'
    command = None
    lesson = None
    while command != EXIT:
        while command is None:
            command = input(f'Enter a lesson number (>=2) or \'e\' to exit: ')
            if command == EXIT:
                exit()
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
