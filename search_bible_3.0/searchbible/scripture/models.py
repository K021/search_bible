from django.db import models

from utils.indexifier.bible_names_manage import (
    ENB_FULL_LIST, KRB_FULL_LIST,
    ENB_OLD_FULL_LIST, KRB_OLD_FULL_LIST,
    FULL_TO_ABBR,
)
from utils.indexifier.variables import (
    ENGLISH, KOREAN,
    KJV, HKJ, HJV,
)


class BookManager(models.Manager):
    def create(self, name, version):
        if name in ENB_FULL_LIST:
            lang = ENGLISH
            is_old = True if name in ENB_OLD_FULL_LIST else False
        elif name in KRB_FULL_LIST:
            lang = KOREAN
            is_old = True if name in KRB_OLD_FULL_LIST else False
        else:
            raise ValueError("Inappropriate 'name' value of Book class")

        book = self.model(
            name=name,
            lang=lang,
            is_old=is_old,
            version=version,
            number_of_chapters=0,
            number_of_verses=0,
        )
        book.save()

        return book


# 성경별 책 모델 (66권 각 정보 저장)
class Book(models.Model):
    BOOK_NAME_EN = tuple((x, y) for x, y in zip(ENB_FULL_LIST, ENB_FULL_LIST))
    BOOK_NAME_KR = tuple((x, y) for x, y in zip(KRB_FULL_LIST, KRB_FULL_LIST))
    BOOK_NAME = BOOK_NAME_EN + BOOK_NAME_KR
    LANGUAGE = (
        (KOREAN, 'Korean'),
        (ENGLISH, 'English'),
    )
    VERSION = (
        (KJV, KJV),
        (HKJ, HKJ),
        (HJV, HJV),
    )

    name = models.CharField(max_length=15, choices=BOOK_NAME, unique=True)  # 성경 이름
    is_old = models.BooleanField()  # 구약 신약
    lang = models.CharField(max_length=2, choices=LANGUAGE)  # 언어
    version = models.CharField(max_length=4, choices=VERSION)  # 번역본 버전
    number_of_chapters = models.IntegerField()  # 총 권 수
    number_of_verses = models.IntegerField()  # 총 구절 수

    objects = BookManager()

    def __str__(self):
        return f'{self.version}{self.name} ({self.get_gross_number_of_chapters()} chapters)'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_abbr = FULL_TO_ABBR[self.name]

    def get_gross_number_of_chapters(self):
        """해당 book 하위의 모든 chapter 갯수를 세서 반환한다"""
        return self.chapters.all().count()

    def get_gross_number_of_verses(self):
        """해당 book 하위의 모든 verse 갯수를 세서 반환한다"""
        return self.verses.all().count()


class ChapterManager(models.Manager):
    def create(self, book, number):
        chapter = self.model(
            book=book,
            number=number,
        )
        chapter.save()

        # chapter 생성할 때마다 book.number_of_chapters 증가
        book.number_of_chapters += 1

        return chapter


# 성경 장별 정보 저장
class Chapter(models.Model):
    book = models.ForeignKey('Book', related_name='chapters', on_delete=models.CASCADE)
    number = models.IntegerField()
    number_of_verses = models.IntegerField()  # gross number of verses

    objects = ChapterManager()

    def __str__(self):
        return f'{self.book.name} Chapter {self.number} ({self.get_gross_number_of_verses()} verses)'

    def get_gross_number_of_verses(self):
        return self.verses.all().count()


class VerseManager(models.Manager):
    def create(self, version, book_name, chapter_number, verse_number, content):
        """book 이나 chapter 를 따로 생성할 필요 없이 verse 생성할 때 같이 생성해 준다"""
        book = Book.objects.get_or_create(name=book_name, version=version)[0]
        chapter = Chapter.objects.get_or_create(book=book, number=chapter_number)[0]
        verse = self.model(
            book=book,
            chapter=chapter,
            chapter_number=chapter_number,
            number=verse_number,
            content=content,
        )
        verse.save()

        # verse 생성할 때마다 book.number_of_verse 증가
        book.number_of_verses += 1
        # verse 생성할 때마다 chapter.number_of_verse 증가
        chapter.number_of_verses += 1

        return verse


# 성경 구절별 정보 저장
class Verse(models.Model):
    book = models.ForeignKey('Book', related_name='verses', on_delete=models.CASCADE)  # bible book info
    chapter = models.ForeignKey('Chapter', related_name='verses', on_delete=models.CASCADE)  # bible chapter info
    chapter_number = models.CharField(max_length=3)  # bible chapter number
    number = models.IntegerField()  # verse number
    content = models.TextField()  # verse content

    objects = VerseManager()

    def __str__(self):
        return f'{self.book.name}{self.chapter_number}:{self.number} {self.content}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # verse location
        self.loc = [self.book.version, self.book.name, self.chapter_number, self.number]

