import io
import os

from .variables import *
from .bible_names_manage import ABBR_TO_FULL


__all__ = (
    'indexify_bible',
    'indexify_by_file',
    'indexify_by_line',
)


def indexify_bible(*versions, **version_to_filenames):
    """
    성경 version 또는, version 과 path 딕셔너리를 받아 해당 버전의 성경을 indexify 하는 함수
    :param versions: 성경 version 이름
    :param version_to_filenames: 성경 version 과 file path
    :return: None
    """
    for version in versions:
        if version.upper() not in VERSION_TO_PATH:
            raise ValueError('Inappropriate argument value in "indexify_bible()" '
                             'version information string must be included in VERSIONS_TO_PATH '
                             'in indexifier.variables')
        indexify_by_file(VERSION_TO_PATH[version], version)

    for version, path in version_to_filenames:
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

