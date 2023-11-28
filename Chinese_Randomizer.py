from random import sample

character_tones = ['ā', 'ó', 'ě', 'ì', 'u']

CHARACTERS = 0
TONES = 1
DEFINITIONS = 2

lessons = {}
with open('Vocabulary.txt', 'r', encoding='utf8') as f:
    lesson = min_lesson = 2
    line = f.readline().strip()
    while line:
        lessons[lesson] = ([], [], [])
        while line:
            lessons[lesson][CHARACTERS].extend(line.split())
            line = f.readline().strip()
        line = f.readline().strip()
        while line:
            lessons[lesson][TONES].append(line)
            line = f.readline().strip()
        num_characters = len(lessons[lesson][CHARACTERS])
        assert(len(lessons[lesson][TONES]) == num_characters)
        for _ in range(num_characters):
            line = f.readline().strip()
            if not line:
                break
            lessons[lesson][DEFINITIONS].append(line)
        assert(len(lessons[lesson][DEFINITIONS]) == num_characters)
        line = f.readline()
        lesson += 1
    max_lesson = lesson - 1

if __name__ == '__main__':
    EXIT = 'e'
    command = None
    lesson_range = f'{min_lesson}-{max_lesson}' if min_lesson != max_lesson else f'{min_lesson}'
    while command != EXIT:
        while command is None:
            command = input(f'Enter a lesson number [{lesson_range}] or \'e\' to exit: ')
            if command == EXIT:
                exit()
            else:
                try:
                    command = lesson = int(command)
                    if not (min_lesson <= lesson <= max_lesson):
                        raise ValueError
                except ValueError:
                    print('Invalid input.')
                    command = None

        num_characters = len(lessons[lesson][CHARACTERS])
        order = sample(range(1, num_characters + 1), num_characters)
        print('Write in this order: ' + str(order))
        print('====================================\nDefinitions\n====================================')
        print('Keep pressing enter to get next character:')
        for i in order:
            input()
            print(f'====================================\n\n{i}: ', end='')
            i -= 1
            print(lessons[lesson][DEFINITIONS][i])
        input()
        print('====================================\nAnswers\n====================================')
        for i in order:
            input()
            print(f'====================================\n\n{i}: ', end='')
            i -= 1
            print(lessons[lesson][CHARACTERS][i])
            print(lessons[lesson][TONES][i])
        print('\n====================================')
        command = None
