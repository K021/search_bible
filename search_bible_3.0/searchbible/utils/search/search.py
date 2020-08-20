from django.db.models import Q

from scripture.models import Verse, Book, Scripture
from utils.indexifier import EN_FULL_TO_KR_FULL
from utils.indexifier.variables import (
    ENP, ENP_SPACE, ENP_HEAD, ENP_HEAD_SPACE,
    ENM, ENM_SPACE, ENO, ENO_SPACE,
    KRP, KRP_SPACE, KRP_HEAD, KRP_HEAD_SPACE,
    KRM, KRM_SPACE, KRO, KRO_SPACE,
    PATTERN_VERSION,
    KJV, HKJ,
    ENGLISH, KOREAN,
)

__all__ = (
    'search',
    'search_scripture',
    'print_by_verse_location',
    'get_keyword_string',
    'sort_keywords',
)


def search():
    keyword_string = get_keyword_string()
    keywords, version = sort_keywords(keyword_string)
    if keywords[0][0]:
        version = KJV if not version else version
        search_scripture(keywords[0], version, ENGLISH)
    elif keywords[1][0]:
        version = HKJ if not version else version
        search_scripture(keywords[1], version, KOREAN)


def search_scripture(keywords, version, lang):
    plus_words = keywords[0]
    minus_words = keywords[1]
    or_words = keywords[2]

    if not plus_words:
        print('플러스 검색어가 입력되지 않았습니다')
        return

    query = None
    for pword in plus_words:
        query = query & Q(content__icontains=pword) if query else Q(content__icontains=pword)
    for mword in minus_words:
        query = query & ~Q(content__icontains=mword)
    for oword in or_words:
        query = query | Q(content__icontains=oword)

    n = 0
    compare_version = HKJ if lang == ENGLISH else KJV
    print('==========================================================')
    print(f' - 검색어: ')
    print(f'    반드시 포함: {plus_words}')
    print(f'    반드시 제외: {minus_words if minus_words else "-"}')
    print(f'    하나라도 있으면 출력: {or_words if or_words else "-"}')
    print(f' - 검색 성경: {version}')
    print('==========================================================')
    for verse in Verse.objects.filter(Q(version=version), query):
        n += 1
        print(f'#{n}: {EN_FULL_TO_KR_FULL[verse.book_name_en]} {verse.chapter_number}:{verse.number}')
        print(verse.content)
        print_by_verse_location(compare_version, verse.book_name_en, verse.chapter_number, verse.number)
        print()
    print(f'총 {n} 개의 구절이 검색되었습니다.')
    print('==========================================================')


def print_by_verse_location(version, book_name_en, chapter_number, verse_number):
    print(
        Scripture.objects.get(
            version=version
        ).books.get(
            name_en=book_name_en
        ).chapters.get(
            number=chapter_number
        ).verses.get(
            number=verse_number
        ).content
    )


def get_keyword_string():
    while True:
        keyword_string = input('검색어를 입력하세요: ')
        if keyword_string:
            return keyword_string


def sort_keywords(string):
    enp = []
    enm = []
    eno = []
    krp = []
    krm = []
    kro = []
    for pattern in [ENP_HEAD, ENP_HEAD_SPACE, ENP, ENP_SPACE]:
        enp += pattern.findall(string)
    for pattern in [ENM, ENM_SPACE]:
        enm += pattern.findall(string)
    for pattern in [ENO, ENO_SPACE]:
        eno += pattern.findall(string)
    for pattern in [KRP_HEAD, KRP_HEAD_SPACE, KRP, KRP_SPACE]:
        krp += pattern.findall(string)
    for pattern in [KRM, KRM_SPACE]:
        krm += pattern.findall(string)
    for pattern in [KRO, KRO_SPACE]:
        kro += pattern.findall(string)

    m = PATTERN_VERSION.search(string)
    version = m.group(1).upper() if m else None
    keywords = [[enp, enm, eno], [krp, krm, kro]]
    return keywords, version


def sort_keywords_2(words):
    plus_words = []
    minus_words = []
    or_words = []
    versions = []
    for word in words:
        if 'in::' in word:
            versions.append(word[4:].upper())
        if not word[0] in '+-/':
            if not plus_words:
                plus_words.append(word)
            else:
                plus_words[-1] += ' ' + word
        elif word[0] == '+':
            plus_words.append(word[1:])
        elif word[0] == '-':
            minus_words.append(word[1:])
        elif word[0] == '/':
            or_words.append(word[1:])

    for word_list in [plus_words, minus_words, or_words]:
        while '' in word_list:
            word_list.remove('')

    plus_words_en = []
    plus_words_kr = []
    for word in plus_words:
        if word.isalpha():
            plus_words_en.append(word)
        else:
            plus_words_kr.append(word)

    minus_words_en = []
    minus_words_kr = []
    for word in minus_words:
        if word.isalpha():
            minus_words_en.append(word)
        else:
            minus_words_kr.append(word)

    or_words_en = []
    or_words_kr = []
    for word in or_words:
        if word.isalpha():
            or_words_en.append(word)
        else:
            or_words_kr.append(word)

    return plus_words_en, plus_words_kr, minus_words_en, minus_words_kr, or_words_en, or_words_kr
