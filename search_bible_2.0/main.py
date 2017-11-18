# ------------------------------------------------------------------------------------------------------------------------
def append_input_to_key(key_list, is_minus=False, is_lower=False):
    """
    검색을 위한 키워드를 담는 리스트인 key_list 를 인자로 받아
    input 함수를 실행해서 얻은 문자열을 key_list 에 추가하여 return

    :param key_list: 검색 키워드 리스트
    :param is_minus: (-)검색어 여부
    :param is_lower: Capital letter 무시 여부
    :return: (input 문자열이 추가된) key_list
    """

    # input 함수 실행시 출력될 문구. is_minus 여부에 따라 문자열이 달라진다.
    plus_string = '(+)keyword: '
    minus_string = '(-)keyword: '
    ask_string = plus_string if not is_minus else minus_string

    user_input = input(ask_string)
    if is_lower:
        user_input = user_input.lower()

    return key_list.append(user_input)


# ------------------------------------------------------------------------------------------------------------------------
def get_keyword_input(is_lower=False):
    """
    plus_keys = (+)키워드를 담는 리스트
    minus_keys = (-)키워드를 담는 리스트

    :param is_lower: Capital letter 무시 여부
    :return: plus_keys, minus_keys
    """

    # 키워드를 담을 리스트
    plus_keys = list()
    minus_keys = list()

    # 최초의 검색어를 받아서 plus_keys 에 넣는다
    append_input_to_key(plus_keys, is_lower=is_lower)

    # 사용자 입력에 따라 추가적인 (+)키워드 또는 (-)키워드를 각각의 리스트에 저장한다
    while True:
        stop_or_go = input('Type 1 to add (+)keyword, 2 for (-)keyword, 0 to search now: ')
        if stop_or_go == '0':
            break
        elif stop_or_go == '1':
            append_input_to_key(plus_keys, is_lower=is_lower)
        elif stop_or_go == '2':
            append_input_to_key(minus_keys, is_minus=True, is_lower=is_lower)
        else:
            print('Invalid value. Try again.')
    return plus_keys, minus_keys


# ------------------------------------------------------------------------------------------------------------------------
def cap_ignoring_script_search(script):
    """
    file type 의 script 객체를 받는다.
    대문자 여부에 상관없는 검색을 수행한다.

    :param script: 검색을 수행할 txt 파일 객체
    :return: None
    """
    plus_keys, minus_keys = get_keyword_input(is_lower=True)
    number_of_result = 0

    line = 'Bible_search_line_default'
    while line != '':
        line = script.readline()
        lower_line = line.lower()
        for i, plus_key in enumerate(plus_keys):
            if plus_key not in lower_line:
                break
            elif i == (len(plus_keys)-1):
                if not minus_keys:
                    number_of_result += 1
                    print(line)
                else:
                    for k, minus_key in enumerate(minus_keys):
                        if minus_key in lower_line:
                            break
                        elif k == (len(minus_keys)-1):
                            number_of_result += 1
                            print(line)
    print('------------------------------------------------')
    print('{} verses'.format(number_of_result))


# ------------------------------------------------------------------------------------------------------------------------
def script_search(script):
    """
    file type 의 script 객체를 받는다
    사용자에게서 검색어를 입력 받아 검색을 수행한다

    :param script: 검색을 수행할 txt 파일 객체
    :return: None
    """
    plus_keys, minus_keys = get_keyword_input()
    number_of_result = 0

    line = 'Bible_search_line_default'
    while line != '':
        line = script.readline()
        for i, plus_key in enumerate(plus_keys):
            if plus_key not in line:
                break
            elif i == (len(plus_keys)-1):
                if not minus_keys:
                    number_of_result += 1
                    print(line)
                else:
                    for k, minus_key in enumerate(minus_keys):
                        if minus_key in line:
                            break
                        elif k == (len(minus_keys)-1):
                            number_of_result += 1
                            print(line)
    print('------------------------------------------------')
    print('{} verses'.format(number_of_result))


# ------------------------------------------------------------------------------------------------------------------------
def search_scripture(scripture_path, sub_scripture_path=None, is_lower=True):
    """
    file type 의 scripture 객체를 받는다
    사용자에게서 검색어를 입력 받아 검색을 수행한다

    :param scripture_path: 검색을 수행할 txt 파일 path
    :param sub_scripture_path: scripture 와 비교할 파일 path
    :param is_lower: Capital letter 무시 여부
    :return: 검색 조건과 일치하는 line 의 index 리스트
    """
    scripture = open(scripture_path, 'r')

    plus_keys, minus_keys = get_keyword_input(is_lower=is_lower)
    number_of_result = 0

    line_index = 0
    line_index_list = list()

    for line in scripture:
        line_index += 1
        line = line.lower() if is_lower else line
        for i, plus_key in enumerate(plus_keys):
            if plus_key not in line:
                break
            elif i == (len(plus_keys) - 1):
                if not minus_keys:
                    number_of_result += 1
                    line_index_list.append(line_index)
                    print()
                    print(line, end='')
                    print_scripture_by_line(sub_scripture_path, line_index)
                else:
                    for k, minus_key in enumerate(minus_keys):
                        if minus_key in line:
                            break
                        elif k == (len(minus_keys) - 1):
                            number_of_result += 1
                            line_index_list.append(line_index)
                            print(line)
                            print_scripture_by_line(sub_scripture_path, line_index)
    print('------------------------------------------------')
    print('{} verses'.format(number_of_result))

    scripture.close()
    return line_index_list


# ------------------------------------------------------------------------------------------------------------------------
def print_scripture_by_line(scripture_path=None, linenos=None):
    """
    int 또는 list 형태의 line number 를 받아
    scripture 파일에서 해당하는 라인을 출력해주는 함수

    :param scripture_path: line number 가 linenos 와 일치하는 문자열을 출력할 파일 객체
    :param linenos: 출력하려는 line number 리스트
    :return: line number 인자 수, 출력된 줄 수 튜플
             scripture 가 없을 경우, None 출력
    """
    if not scripture_path:
        return False
    scripture = open(scripture_path, 'r')

    if type(linenos) not in [int, list]:
        raise ValueError('The argument "lineno" must be int or list type.')
    linenos = [linenos] if type(linenos) == int else list(linenos)

    scripture_lineno = 0
    num_of_printed_line = 0

    for verse in scripture:
        scripture_lineno += 1
        for lineno in linenos:
            if lineno == scripture_lineno:
                num_of_printed_line += 1
                print(verse, end='')
                linenos.remove(lineno)
                break
        if not linenos:
            break

    scripture.close()
    return len(linenos), num_of_printed_line

# ------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    kb_path = "./KoreanBible.txt"
    eb_path = "./EnglishBible.txt"

    while True:
        # 검색할 Scripture 선택
        scripture_type = input('Type 1 for KoreanBible, 2 for EnglishBible, or any other key to stop: ')
        if scripture_type in ['1', '2']:
            main_path, sub_path = (kb_path, eb_path) if scripture_type == '1' else (eb_path, kb_path)

            # 비교검색 여부
            while sub_path:
                is_sub_scripture = input('Type 1 for print another scripture to compare, 2 for no comparing: ')
                if is_sub_scripture in ['1', '2']:
                    sub_path = sub_path if is_sub_scripture == '1' else None
                    break
                else:
                    print('Invalid value. Try again.')

            # 대문자 무시 여부
            is_ignore_caps = True
            while main_path == eb_path:
                is_ignore_caps = input('Type 1 for ignore CAPITAL LETTER, 2 for normal search: ')
                if is_ignore_caps in ['1', '2']:
                    is_ignore_caps = True if is_ignore_caps == '1' else False
                    break
                else:
                    print('Invalid value. Try again.')

            search_scripture(scripture_path=main_path, sub_scripture_path=sub_path, is_lower=is_ignore_caps)

        elif scripture_type == '11':  # 한글 검색, 한영 비교
            search_scripture(scripture_path=kb_path, sub_scripture_path=eb_path)
        elif scripture_type == '12':  # 한글 검색, 한글만
            search_scripture(scripture_path=kb_path, sub_scripture_path=None)
        elif scripture_type == '211':  # 영어 검색, 영한 비교, 소문자
            search_scripture(scripture_path=eb_path, sub_scripture_path=kb_path, is_lower=True)
        else:
            break
