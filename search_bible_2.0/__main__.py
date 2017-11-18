import os

from functions import search_scripture

base = os.path.dirname(__file__)
kb_path = os.path.join(base, "KoreanBible.txt")
eb_path = os.path.join(base, "EnglishBible.txt")
print(kb_path)

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
