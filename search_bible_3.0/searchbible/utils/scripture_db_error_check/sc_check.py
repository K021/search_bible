
from scripture.models import Book
from utils.indexifier import (
    NUMBER_OF_VERSES_PER_BOOK_EN,
    NUMBER_OF_CHAPTERS_PER_BOOK_EN,
    GROSS_NUMBER_OF_VERSES, GROSS_NUMBER_OF_CHAPTERS,
    VERSIONS,
)


def print_book_info(book):
    print(book)
    print(f'name: {book.name}')
    print(f'is_old: {book.is_old}')
    print(f'lang: {book.lang}')
    print(f'version: {book.version}')
    print(f'number_of_chapters: {book.number_of_chapters}')
    print(f'number_of_verses: {book.number_of_verses}')
    print()


def check_scripture(**versions):
    if not versions:
        versions = VERSIONS

    for version in versions:
        check_scripture_by_version(version)


def check_scripture_by_version(version):
    books = Book.objects.filter(version=version)
    if not books:
        print(f'No data found in the given condition, scripture version "{version}"')
        return

    errors_of_chapter = []
    errors_of_verse = []
    errors_in_func_1 = []
    errors_in_func_2 = []
    for book in books:
        if not check_number_of_chapters_by_book(book, NUMBER_OF_CHAPTERS_PER_BOOK_EN):
            errors_of_chapter.append(
                (book.version, book.name_en, book.number_of_chapters, NUMBER_OF_CHAPTERS_PER_BOOK_EN[book.name_en])
            )
        if not check_number_of_verses_by_book(book, NUMBER_OF_VERSES_PER_BOOK_EN):
            errors_of_verse.append(
                (book.version, book.name_en, book.number_of_verses, NUMBER_OF_VERSES_PER_BOOK_EN[book.name_en])
            )

        gross_number_of_chapters = book.get_gross_number_of_chapters()
        if not gross_number_of_chapters == book.number_of_chapters:
            errors_in_func_1.append(
                (book.version, book.name_en, book.number_of_chapters, gross_number_of_chapters)
            )
        gross_number_of_verses = book.get_gross_number_of_verses()
        if not gross_number_of_verses == book.number_of_verses:
            errors_in_func_2.append(
                (book.version, book.name_en, book.number_of_verses, gross_number_of_verses)
            )

    print()
    print(f'Scripture Database Error Check in version "{version}"')
    if len(books) == 66:
        print(f'Gross number of books: good')
    else:
        print(f'Gross number of books: {len(books)}, {66-len(books)} books are missing')

    if not errors_of_chapter:
        print(f'Number of chapters by book: good')
    else:
        print(f'Number of chapters by book: error')
        print(f'    Errors in number of chapters by book')
        for e in errors_of_chapter:
            print(f'    {e[0]}, {e[1]}, data:{e[2]}, real value:{e[3]}')

    if not errors_of_verse:
        print(f'Number of verses by book: good')
    else:
        print(f'Number of verses by book: error')
        print(f'    Errors in number of verses by book')
        for e in errors_of_verse:
            print(f'    {e[0]}, {e[1]}, data:{e[2]}, real value:{e[3]}')

    if not errors_in_func_1:
        print(f'Function #1, get_gross_number_of_chapters(): good')
    else:
        print('Function #1, get_gross_number_of_chapters(): error')
        print('    Errors in function #1, get_gross_number_of_chapters()')
        for e in errors_in_func_1:
            print(f'    {e[0]}, {e[1]}, data:{e[2]}, real value:{e[3]}')

    if not errors_in_func_2:
        print(f'Function #2, get_gross_number_of_verses(): good')
    else:
        print('Function #2, get_gross_number_of_verses(): error')
        print('    Errors in function #2, get_gross_number_of_verses()')
        for e in errors_in_func_2:
            print(f'    {e[0]}, {e[1]}, data:{e[2]}, real value:{e[3]}')


def check_number_of_verses_by_book(book, verses_per_book):
    if not verses_per_book[book.name_en] == book.number_of_verses:
        return False
    return True


def check_number_of_chapters_by_book(book, chapters_per_book):
    if not chapters_per_book[book.name_en] == book.number_of_chapters:
        return False
    return True


def check_number_of_verses_by_version(version):
    books = Book.objects.filter(version=version)
    if not books:
        print(f'No data found in the given condition, scripture version "{version}"')
        return

    summation = 0
    number_of_errors = 0
    for book in Book.objects.filter(version=version):
        is_correct = 'yes'
        if not NUMBER_OF_VERSES_PER_BOOK_EN[book.name_en] == book.number_of_verses:
            is_correct = 'noooooooooooooooo'
        if not book.get_gross_number_of_verses() == book.number_of_verses:
            is_correct = 'yes, no'

        if not is_correct == 'yes':
            number_of_errors += 1
        print(f'{book.name_en:<17}: {book.number_of_verses:>5} verses,   {is_correct}')
        summation += book.number_of_verses

    print()
    print(f'version: {version}')
    print(f'number of errors: {number_of_errors}')
    print(f'gross number of verses: {summation}, {GROSS_NUMBER_OF_VERSES == summation}')


def check_number_of_chapters_by_version(version):
    books = Book.objects.filter(version=version)
    if not books:
        print(f'No data found in the given condition, scripture version "{version}"')
        return

    summation = 0
    number_of_errors = 0
    for book in Book.objects.filter(version='KJV'):
        yes = 'yes'
        if not NUMBER_OF_CHAPTERS_PER_BOOK_EN[book.name_en] == book.number_of_chapters:
            yes = 'noooooooooooooooo'
            number_of_errors += 1

        print(f'{book.name_en:<17}: {book.number_of_chapters} chapters,   {yes}')
        summation += book.number_of_chapters

    print()
    print(f'version: {version}')
    print(f'number of errors: {number_of_errors}')
    print(f'\ngross number of chapters: {summation}, {GROSS_NUMBER_OF_CHAPTERS == summation}')