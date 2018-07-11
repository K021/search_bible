import io
import os

from .variables import *
from .bible_names_manage import ABBR_TO_FULL


__all__ = (
    'indexify_bible',
    'indexify_by_file',
    'indexify_by_line',
)


def indexify_bible(versions):
    """
    *versions 에는 세가지 타입의 변수가 올 수 있다.
        1. 문자열
            'version'
        2. 문자열 리스트
            ['version1', 'version2', 'version3']
        3. 딕셔너리
            versions = {
                'version1': 'file name1'
                'version2': 'file name2'
                'version3': 'file name3'
            }
    딕셔너리 형태로 따로 파일 이름이 주어지지 않으면, utils.indexifier.variables 에 저장된 PATH_BIBLE_* 를 사용한다
    :return:
    """
    # 이 로직 *args 와 **kwargs 로 바꾸기
    if type(versions) is str:
        if versions not in VERSION_TO_PATH:
            raise ValueError('Inappropriate argument value in "indexify_bible()" '
                             'version information string must be included in VERSIONS_TO_PATH '
                             'in indexifier.variables')
        indexify_by_file(VERSION_TO_PATH[versions], versions)
    elif type(versions) is list:
        for version in versions:
            if version not in VERSION_TO_PATH:
                raise ValueError('Inappropriate argument value in "indexify_bible()" '
                                 'version information string must be included in VERSIONS_TO_PATH '
                                 'in indexifier.variables')
            indexify_by_file(VERSION_TO_PATH[versions], version)
    elif type(versions) is dict:
        for version, path in versions.items():
            indexify_by_file(path, version)


def indexify_by_file(path_or_file, version):
    if isinstance(path_or_file, str):
        if os.path.isfile(path_or_file):
            with open(path_or_file, 'rt') as f:
                for line in f:
                    indexify_by_line(line, version)
        else:
            raise FileNotFoundError(f'"{path_or_file}" does not exist.')
    elif isinstance(path_or_file, io.TextIOBase):
        for line in path_or_file:
            indexify_by_line(line, version)
    else:
        raise ValueError('Inappropriate argument value in "indexify_by_file()". '
                         'Only string(file path) or text file object.')


def indexify_by_line(line, version):
    from scripture.models import Verse

    m = PATTERN_LINE.match(line)
    if m:
        book_name = ABBR_TO_FULL[m.group('book')]
        chapter_number = int(m.group('chapter'))
        verse_number = int(m.group('verse'))
        content = m.group('content')

        if not Verse.objects.filter(version=version,
                                    book_name=book_name,
                                    chapter_number=chapter_number,
                                    number=verse_number).exists():
            Verse.objects.create(
                version=version,
                book_name=book_name,
                chapter_number=chapter_number,
                verse_number=verse_number,
                content=content,
            )
        else:
            print(book_name, chapter_number, verse_number, content)
    else:
        raise AttributeError(f'No match in this line {line}')

