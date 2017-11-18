
def search_keys_generator():
    """
    plus_key: (+) 검색어 리스트
    minus_key: (-) 검색어 리스트
    반환 값: (plus_key, minus_key)
    """
    plus_key = list()
    minus_key = list()

    user_input = input('(+)keyword: ')
    plus_key.append(user_input)

    while True:
        stop_or_go = input('Type 1 to add (+)keyword, 2 for (-)keyword, 0 to search now: ')
        if stop_or_go == '0':
            break
        elif stop_or_go == '1':
            user_input = input('(+)keyword: ')
            plus_key.append(user_input)
        elif stop_or_go == '2':
            user_input = input('(-)keyword: ')
            minus_key.append(user_input)
        else:
            print('Invalid value. Try again.')

    return plus_key, minus_key


def scriptsearch_dual(main_bible, sub_bible):
    """
    file type의 bible 객체를 받는다.
    """

    number_of_line = 0

    plus_key, minus_key = search_keys_generator()

    line = 'Bible_search_line_default'

    for main_line, sub_line in zip(main_bible, sub_bible):
        for i, key in enumerate(plus_key):
            if key not in main_line:
                break
            elif i == (len(plus_key)-1):
                if not minus_key:
                    number_of_line += 1
                    print(main_line)
                    print(sub_line)

    while line != '':
        line = b.readline()
        for i, key in enumerate(plus_key):
            if key not in line:
                break
            elif i == (len(plus_key)-1):
                if not minus_key:
                    number_of_line += 1
                    print(line)
                else:
                    for k, key in enumerate(minus_key):
                        if key in line:
                            break
                        elif k == (len(minus_key)-1):
                            number_of_line += 1
                            print(line)
    print('------------------------------------------------')
    print('{} verses'.format(number_of_line))


# ------------------------------------------------------------------------------------------------------------------------
def cap_ignoring_script_search(bible):
    """
    file type의 bible 객체를 받는다.
    대문자 여부에 상관없는 검색을 수행한다.
    """
    plus_key = []
    minus_key = []

    user_input = input('(+)keyword: ')
    user_input = user_input.lower()
    plus_key.append(user_input)

    number_of_line = 0

    while True:
        stop_or_go = input('Type 1 to add (+)keyword, 2 for (-)keyword, 0 to search now: ')
        if stop_or_go == '0':
            break
        elif stop_or_go == '1':
            user_input = input('(+)keyword: ')
            user_input = user_input.lower()
            plus_key.append(user_input)
        elif stop_or_go == '2':
            user_input = input('(-)keyword: ')
            user_input = user_input.lower()
            minus_key.append(user_input)
        else:
            print('Invalid value. Try again.')

    line = 'Bible_search_line_default'

    while line != '':
        line = bible.readline()
        lower_line = line.lower()
        for i, key in enumerate(plus_key):
            if key not in lower_line:
                break
            elif i == (len(plus_key)-1):
                if not minus_key:
                    number_of_line += 1
                    print(line)
                else:
                    for k, key in enumerate(minus_key):
                        if key in lower_line:
                            break
                        elif k == (len(minus_key)-1):
                            number_of_line += 1
                            print(line)
    print('------------------------------------------------')
    print('{} verses'.format(number_of_line))


# ------------------------------------------------------------------------------------------------------------------------
def script_search(bible):
    """
    file type의 bible 객체를 받는다.
    """
    plus_key = []
    minus_key = []

    user_input = input('(+)keyword: ')
    plus_key.append(user_input)

    number_of_line = 0

    while True:
        stop_or_go = input('Type 1 to add (+)keyword, 2 for (-)keyword, 0 to search now: ')
        if stop_or_go == '0':
            break
        elif stop_or_go == '1':
            user_input = input('(+)keyword: ')
            plus_key.append(user_input)
        elif stop_or_go == '2':
            user_input = input('(-)keyword: ')
            minus_key.append(user_input)
        else:
            print('Invalid value. Try again.')

    line = 'Bible_search_line_default'

    while line != '':
        line = bible.readline()
        for i, key in enumerate(plus_key):
            if key not in line:
                break
            elif i == (len(plus_key)-1):
                if not minus_key:
                    number_of_line += 1
                    print(line)
                else:
                    for k, key in enumerate(minus_key):
                        if key in line:
                            break
                        elif k == (len(minus_key)-1):
                            number_of_line += 1
                            print(line)
    print('------------------------------------------------')
    print('{} verses'.format(number_of_line))
# ------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    kb = open("./KoreanBible.txt", 'r')
    eb = open("./EnglishBible.txt", 'r')

    while True:
        search_type = input('Type 1 for KoreanBible, 2 for EnglishBible: ')

        # 한국어 성경 검색
        if search_type == '1':
            b = kb
            script_search(b)
            break

        # 영어 성경 검색
        elif search_type == '2':
            b = eb
            while True:
                capital_type = input('Type 1 for ignore CAPITAL LETTER, 2 for normal search: ')
                # 대문자 무시 검색
                if capital_type == '1':
                    print('================================================')
                    cap_ignoring_script_search(b)
                    print('================================================')
                    break
                # 대문자 고려 검색
                elif capital_type == '2':
                    print('================================================')
                    script_search(b)
                    print('================================================')
                    break
                else:
                    print('Invalid value. Try again.')
            break

        else:
            print('Invalid value. Try again.')

    kb.close()
    eb.close()
