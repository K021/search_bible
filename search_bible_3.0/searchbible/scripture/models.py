from django.db import models

from utils.indexifier.bible_names_manage import (
    ENB_FULL_LIST, KRB_FULL_LIST,
    ENB_OLD_FULL_LIST, KRB_OLD_FULL_LIST,
    FULL_TO_ABBR, KR_FULL_TO_EN_FULL,
)
from utils.indexifier.variables import (
    ENGLISH, KOREAN,
    KJV, HKJ, HJV, VERSIONS, VERSION_TO_LANG,
    KJV_VERBOSE, HKJ_VERBOSE, HJV_VERBOSE,
)


class CustomManager(models.Manager):
    def get_or_create(self, **kwargs):
        try:
            return self.get(**kwargs), False
        except self.model.DoesNotExist:
            return self.create(**kwargs), True


class ScriptureManager(CustomManager):
    def create(self, version):
        if version not in VERSIONS:
            raise ValueError("Inappropriate 'version' value of Scripture class. "
                             f'given version:{version} is not in Scripture.VERSION')

        scripture = self.model(
            version=version,
        )
        scripture.save()

        return scripture


class Scripture(models.Model):
    LANGUAGE = (
        (KOREAN, 'Korean'),
        (ENGLISH, 'English'),
    )
    VERSION = (
        (KJV, KJV_VERBOSE),
        (HKJ, HKJ_VERBOSE),
        (HJV, HJV_VERBOSE),
    )

    version = models.CharField(max_length=4, choices=VERSION)
    lang = models.CharField(max_length=2, choices=LANGUAGE)

    objects = ScriptureManager()

    def __str__(self):
        return f'{self.version}, {self.lang}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lang = VERSION_TO_LANG[self.version]


class BookManager(CustomManager):
    def create(self, scripture, name, version):
        if name in ENB_FULL_LIST:
            lang = ENGLISH
            is_old = True if name in ENB_OLD_FULL_LIST else False
        elif name in KRB_FULL_LIST:
            lang = KOREAN
            is_old = True if name in KRB_OLD_FULL_LIST else False
        else:
            raise ValueError("Inappropriate 'name' value of Book class")

        book = self.model(
            scripture=scripture,
            name=name,
            lang=lang,
            is_old=is_old,
            version=version,
            number_of_chapters=0,
            number_of_verses=0,
        )
        book.save()

        book_number = book.pk % 66
        book_number = 66 if book_number == 0 else book_number
        print(f'The {name} of {version} had been created. ({book_number}, {book.pk})')
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
        (KJV, KJV_VERBOSE),
        (HKJ, HKJ_VERBOSE),
        (HJV, HJV_VERBOSE),
    )

    # name 은 기본적으로 FULL 로 저장한다
    scripture = models.ForeignKey('Scripture', related_name='books', on_delete=models.CASCADE)
    name = models.CharField(max_length=15, choices=BOOK_NAME)  # 성경 이름
    name_en = models.CharField(max_length=15)
    is_old = models.BooleanField()  # 구약 신약
    lang = models.CharField(max_length=2, choices=LANGUAGE)  # 언어
    version = models.CharField(max_length=4, choices=VERSION)  # 번역본 버전
    number_of_chapters = models.IntegerField(default=0)  # 총 권 수
    number_of_verses = models.IntegerField(default=0)  # 총 구절 수

    objects = BookManager()

    def __str__(self):
        return f'{self.version} {self.name} ({self.get_gross_number_of_chapters()} chapters)'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_abbr = FULL_TO_ABBR[self.name]
        self.name_en = KR_FULL_TO_EN_FULL[self.name] if self.lang == KOREAN else self.name

    def get_gross_number_of_chapters(self):
        """해당 book 하위의 모든 chapter 갯수를 세서 반환한다"""
        return self.chapters.all().count()

    def get_gross_number_of_verses(self):
        """해당 book 하위의 모든 verse 갯수를 세서 반환한다"""
        return self.verses.all().count()


class ChapterManager(CustomManager):
    def create(self, scripture, book, number):
        chapter = self.model(
            scripture=scripture,
            book=book,
            number=number,
        )
        chapter.save()

        # chapter 생성할 때마다 book.number_of_chapters 증가
        book.number_of_chapters += 1
        book.save()

        return chapter


# 성경 장별 정보 저장
class Chapter(models.Model):
    scripture = models.ForeignKey('Scripture', related_name='chapters', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', related_name='chapters', on_delete=models.CASCADE)
    number = models.IntegerField()
    number_of_verses = models.IntegerField(default=0)  # gross number of verses

    objects = ChapterManager()

    def __str__(self):
        return f'{self.book.version} {self.book.name} ' \
               f'Chapter {self.number} ({self.get_gross_number_of_verses()} verses)'

    def get_gross_number_of_verses(self):
        return self.verses.all().count()


class VerseManager(CustomManager):
    def create(self, version, book_name, chapter_number, verse_number, content):
        """book 이나 chapter 를 따로 생성할 필요 없이 verse 생성할 때 같이 생성해 준다"""
        scripture = Scripture.objects.get_or_create(version=version)[0]
        book = Book.objects.get_or_create(scripture=scripture, name=book_name, version=version)[0]
        chapter = Chapter.objects.get_or_create(scripture=scripture, book=book, number=chapter_number)[0]
        verse = self.model(
            scripture=scripture,
            version=version,
            book=book,
            chapter=chapter,
            book_name=book_name,
            chapter_number=chapter_number,
            number=verse_number,
            content=content,
        )
        verse.save()

        # verse 생성할 때마다 book.number_of_verse 증가
        book.number_of_verses += 1
        book.save()
        # verse 생성할 때마다 chapter.number_of_verse 증가
        chapter.number_of_verses += 1
        chapter.save()

        return verse


# 성경 구절별 정보 저장
class Verse(models.Model):
    VERSION = (
        (KJV, KJV_VERBOSE),
        (HKJ, HKJ_VERBOSE),
        (HJV, HJV_VERBOSE),
    )
    scripture = models.ForeignKey('Scripture', related_name='verses', on_delete=models.CASCADE)
    version = models.CharField(max_length=4, choices=VERSION)  # 번역본 버전
    book = models.ForeignKey('Book', related_name='verses', on_delete=models.CASCADE)  # bible book info
    book_name = models.CharField(max_length=20)  # book_name 은 기본적으로 FULL 로 저장한다.
    book_name_abbr = models.CharField(max_length=10)  # book_name abbreviation
    book_name_en = models.CharField(max_length=20)
    chapter = models.ForeignKey('Chapter', related_name='verses', on_delete=models.CASCADE)  # bible chapter info
    chapter_number = models.CharField(max_length=3)  # bible chapter number
    number = models.IntegerField()  # verse number
    content = models.TextField()  # verse content
    loc = models.CharField(max_length=30)

    objects = VerseManager()

    def __str__(self):
        return f'{self.book_name}{self.chapter_number}:{self.number} {self.content} ({self.version})'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # verse location
        self.book_name_en = self.book.name_en
        self.book_name_abbr = FULL_TO_ABBR[self.book_name]
        self.loc_list = [self.book.version, self.book_name, self.chapter_number, self.number]
        self.loc = f'{self.version}{self.book_name_en}{self.chapter_number}:{self.number}'
