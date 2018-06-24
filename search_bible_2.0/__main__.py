
import os

from functions import search_scripture

base = os.path.dirname(__file__)
kb_path = os.path.join(base, "KoreanBible.txt")
eb_path = os.path.join(base, "EnglishBible.txt")

old_kr = os.path.join(base, 'TheOldTestamentKR.txt')
old_en = os.path.join(base, 'TheOldTestamentEN.txt')
new_kr = os.path.join(base, 'TheNewTestamentKR.txt')
new_en = os.path.join(base, 'TheNewTestamentEN.txt')

print('======================================================')
print('=           SearchBible 2.0 by Joo-eon Kim           =')
print('======================================================')

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

        # 프린트 줄 수
        # 3 이 입력되면, 검색된 구절부터 3 절을 프린트한다.
        number_of_lines_to_print = 1
        while number_of_lines_to_print:
            number_of_lines_to_print = input('How many line do you want to type from the searched verse? (max 10):')
            if number_of_lines_to_print in [str(x) for x in range(1, 11)]:
                number_of_lines_to_print = int(number_of_lines_to_print)
                break
            else:
                print('Invalid value. Try again')

        search_scripture(
            scripture_path=main_path,
            sub_scripture_path=sub_path,
            is_lower=is_ignore_caps,
            number_of_lines_to_print=number_of_lines_to_print,
        )

    elif scripture_type == '311':   # 한국어 구약
        search_scripture(scripture_path=old_kr, sub_scripture_path=old_en)
    elif scripture_type == '312':   # 한국어 신약
        search_scripture(scripture_path=new_kr, sub_scripture_path=new_en)
    elif scripture_type == '321':   # 영어 구약
        search_scripture(scripture_path=old_en, sub_scripture_path=old_kr)
    elif scripture_type == '322':   # 영어 신약
        search_scripture(scripture_path=new_en, sub_scripture_path=new_kr)
    elif scripture_type == '321c':  # 영어 구약, 대문자 검사
        search_scripture(scripture_path=old_en, sub_scripture_path=old_kr, is_lower=False)
    elif scripture_type == '322c':  # 영어 산약, 대무자 검사
        search_scripture(scripture_path=new_en, sub_scripture_path=new_kr, is_lower=False)

    elif scripture_type == '11':    # 한글 검색, 한영 비교
        search_scripture(scripture_path=kb_path, sub_scripture_path=eb_path)
    elif scripture_type == '12':    # 한글 검색, 한글만
        search_scripture(scripture_path=kb_path, sub_scripture_path=None)
    elif scripture_type == '211':   # 영어 검색, 영한 비교, 소문자
        search_scripture(scripture_path=eb_path, sub_scripture_path=kb_path, is_lower=True)
    else:
        break
