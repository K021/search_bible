import os
import re

from config import settings

from .bible_names import *

__all__ = (
    'FILE_DIR',
    'PATH_BIBLE_KJV',
    'PATH_BIBLE_HKJ',
    'PATH_BIBLE_HJV',

    'PATTERN_LINE',
    'ENP',
    'ENP_SPACE',
    'ENP_HEAD',
    'ENP_HEAD_SPACE',
    'ENM',
    'ENM_SPACE',
    'ENO',
    'ENO_SPACE',
    'KRP',
    'KRP_SPACE',
    'KRP_HEAD',
    'KRP_HEAD_SPACE',
    'KRM',
    'KRM_SPACE',
    'KRO',
    'KRO_SPACE',
    'PATTERN_VERSION',

    'ENGLISH',
    'KOREAN',

    'KJV',
    'HKJ',
    'HJV',
    'VERSIONS',
    'KJV_VERBOSE',
    'HKJ_VERBOSE',
    'HJV_VERBOSE',
    'VERSION_TO_LANG',
    'VERSION_TO_PATH',

    'GROSS_NUMBER_OF_BOOKS',
    'GROSS_NUMBER_OF_CHAPTERS',
    'GROSS_NUMBER_OF_VERSES',
    'NUMBER_OF_VERSES_PER_BOOK_EN',
    'NUMBER_OF_VERSES_PER_BOOK_KR',
    'NUMBER_OF_CHAPTERS_PER_BOOK_EN',
    'NUMBER_OF_CHAPTERS_PER_BOOK_KR',
)


# file paths
FILE_DIR = os.path.join(settings.STATIC_DIR, 'files')
PATH_BIBLE_KJV = os.path.join(FILE_DIR, 'kjv-the-holy-bible.txt')
PATH_BIBLE_HKJ = os.path.join(FILE_DIR, 'hkj-the-holy-bible.txt')
PATH_BIBLE_HJV = os.path.join(FILE_DIR, 'hjv-the-holy-bible.txt')


# indexing pattern
PATTERN_LINE = re.compile(r'^(?P<book>\d?\D+[.]?)(?P<chapter>\d{1,3}):(?P<verse>\d{1,3})[ ]+(?P<content>.+)')


# key word sorting patterns
ENP = re.compile(r'\+([a-zA-Z]+)')
ENP_SPACE = re.compile(r'\+[\'\"]([a-zA-Z ]+)[\'\"]')
ENP_HEAD = re.compile(r'^[ ]*([a-zA-Z]+)')
ENP_HEAD_SPACE = re.compile(r'^[ ]*[\'\"]([a-zA-Z ]+)[\'\"]')
ENM = re.compile(r'-([a-zA-Z]+)')
ENM_SPACE = re.compile(r'-[\'\"]([a-zA-Z ]+)[\'\"]')
ENO = re.compile(r'\\([a-zA-Z]+)')
ENO_SPACE = re.compile(r'\\[\'\"]([a-zA-Z ]+)[\'\"]')

KRP = re.compile(r'\+([가-힣]+)')
KRP_SPACE = re.compile(r'\+[\'\"]([가-힣 ]+)[\'\"]')
KRP_HEAD = re.compile(r'^[ ]*([가-힣]+)')
KRP_HEAD_SPACE = re.compile(r'^[ ]*[\'\"]([가-힣 ]+)[\'\"]')
KRM = re.compile(r'-([가-힣]+)')
KRM_SPACE = re.compile(r'-[\'\"]([가-힣 ]+)[\'\"]')
KRO = re.compile(r'\\([가-힣]+)')
KRO_SPACE = re.compile(r'\\[\'\"]([가-힣 ]+)[\'\"]')

PATTERN_VERSION = re.compile(r':in:([a-zA-Z]+)')

# scripture model attribute db input value
ENGLISH = 'en'
KOREAN = 'kr'


# scripture identification variables
KJV = 'KJV'  # 영어 킹제임스
HKJ = 'HKJV'  # 한글킹제임스
HJV = 'HJV'  # 흠정역

VERSIONS = [KJV, HKJ, HJV]

KJV_VERBOSE = 'King James Version'
HKJ_VERBOSE = '한글 킹제임스'
HJV_VERBOSE = '흠정역'

VERSION_TO_LANG = {
    KJV: ENGLISH,
    HKJ: KOREAN,
    HJV: KOREAN,
}


# Version to File Path Dictionary
VERSION_TO_PATH = {
    KJV: PATH_BIBLE_KJV,
    HKJ: PATH_BIBLE_HKJ,
    HJV: PATH_BIBLE_HJV,
}


# Bible Information
GROSS_NUMBER_OF_BOOKS = 66
GROSS_NUMBER_OF_CHAPTERS = 1189
GROSS_NUMBER_OF_VERSES = 31102
NUMBER_OF_VERSES_PER_BOOK_EN = {
    GENESIS_FULL: 1533,
    EXODUS_FULL: 1213,
    LEVITICUS_FULL: 859,
    NUMBERS_FULL: 1288,
    DEUTERONOMY_FULL: 959,
    JOSHUA_FULL: 658,
    JUDGES_FULL: 618,
    RUTH_FULL: 85,
    SAMUEL_1_FULL: 810,
    SAMUEL_2_FULL: 695,
    KINGS_1_FULL: 816,
    KINGS_2_FULL: 719,
    CHRONICLES_1_FULL: 942,
    CHRONICLES_2_FULL: 822,
    EZRA_FULL: 280,
    NEHEMIAH_FULL: 406,
    ESTHER_FULL: 167,
    JOB_FULL: 1070,
    PSALMS_FULL: 2461,
    PROVERBS_FULL: 915,
    ECCLESIASTES_FULL: 222,
    SONG_OF_SOLOMON_FULL: 117,
    ISAIAH_FULL: 1292,
    JEREMIAH_FULL: 1364,
    LAMENTATIONS_FULL: 154,
    EZEKIEL_FULL: 1273,
    DANIEL_FULL: 357,
    HOSEA_FULL: 197,
    JOEL_FULL: 73,
    AMOS_FULL: 146,
    OBADIAH_FULL: 21,
    JONAH_FULL: 48,
    MICAH_FULL: 105,
    NAHUM_FULL: 47,
    HABAKKUK_FULL: 56,
    ZEPHANIAH_FULL: 53,
    HAGGAI_FULL: 38,
    ZECHARIAH_FULL: 211,
    MALACHI_FULL: 55,
    MATTHEW_FULL: 1071,
    MARK_FULL: 678,
    LUKE_FULL: 1151,
    JOHN_FULL: 879,
    ACTS_FULL: 1007,
    ROMANS_FULL: 433,
    CORINTHIANS_1_FULL: 437,
    CORINTHIANS_2_FULL: 257,
    GALATIANS_FULL: 149,
    EPHESIANS_FULL: 155,
    PHILIPPIANS_FULL: 104,
    COLOSSIANS_FULL: 95,
    THESSALONIANS_1_FULL: 89,
    THESSALONIANS_2_FULL: 47,
    TIMOTHY_1_FULL: 113,
    TIMOTHY_2_FULL: 83,
    TITUS_FULL: 46,
    PHILEMON_FULL: 25,
    HEBREWS_FULL: 303,
    JAMES_FULL: 108,
    PETER_1_FULL: 105,
    PETER_2_FULL: 61,
    JOHN_1_FULL: 105,
    JOHN_2_FULL: 13,
    JOHN_3_FULL: 14,
    JUDE_FULL: 25,
    REVELATION_FULL: 404,
}
NUMBER_OF_VERSES_PER_BOOK_KR = {
    GENESIS_KR: 1533,
    EXODUS_KR: 1213,
    LEVITICUS_KR: 859,
    NUMBERS_KR: 1288,
    DEUTERONOMY_KR: 959,
    JOSHUA_KR: 658,
    JUDGES_KR: 618,
    RUTH_KR: 85,
    SAMUEL_1_KR: 810,
    SAMUEL_2_KR: 695,
    KINGS_1_KR: 816,
    KINGS_2_KR: 719,
    CHRONICLES_1_KR: 942,
    CHRONICLES_2_KR: 822,
    EZRA_KR: 280,
    NEHEMIAH_KR: 406,
    ESTHER_KR: 167,
    JOB_KR: 1070,
    PSALMS_KR: 2461,
    PROVERBS_KR: 915,
    ECCLESIASTES_KR: 222,
    SONG_OF_SOLOMON_KR: 117,
    ISAIAH_KR: 1292,
    JEREMIAH_KR: 1364,
    LAMENTATIONS_KR: 154,
    EZEKIEL_KR: 1273,
    DANIEL_KR: 357,
    HOSEA_KR: 197,
    JOEL_KR: 73,
    AMOS_KR: 146,
    OBADIAH_KR: 21,
    JONAH_KR: 48,
    MICAH_KR: 105,
    NAHUM_KR: 47,
    HABAKKUK_KR: 56,
    ZEPHANIAH_KR: 53,
    HAGGAI_KR: 38,
    ZECHARIAH_KR: 211,
    MALACHI_KR: 55,
    MATTHEW_KR: 1071,
    MARK_KR: 678,
    LUKE_KR: 1151,
    JOHN_KR: 879,
    ACTS_KR: 1007,
    ROMANS_KR: 433,
    CORINTHIANS_1_KR: 437,
    CORINTHIANS_2_KR: 257,
    GALATIANS_KR: 149,
    EPHESIANS_KR: 155,
    PHILIPPIANS_KR: 104,
    COLOSSIANS_KR: 95,
    THESSALONIANS_1_KR: 89,
    THESSALONIANS_2_KR: 47,
    TIMOTHY_1_KR: 113,
    TIMOTHY_2_KR: 83,
    TITUS_KR: 46,
    PHILEMON_KR: 25,
    HEBREWS_KR: 303,
    JAMES_KR: 108,
    PETER_1_KR: 105,
    PETER_2_KR: 61,
    JOHN_1_KR: 105,
    JOHN_2_KR: 13,
    JOHN_3_KR: 14,
    JUDE_KR: 25,
    REVELATION_KR: 404,
}
NUMBER_OF_CHAPTERS_PER_BOOK_EN = {
    GENESIS_FULL: 50,
    EXODUS_FULL: 40,
    LEVITICUS_FULL: 27,
    NUMBERS_FULL: 36,
    DEUTERONOMY_FULL: 34,
    JOSHUA_FULL: 24,
    JUDGES_FULL: 21,
    RUTH_FULL: 4,
    SAMUEL_1_FULL: 31,
    SAMUEL_2_FULL: 24,
    KINGS_1_FULL: 22,
    KINGS_2_FULL: 25,
    CHRONICLES_1_FULL: 29,
    CHRONICLES_2_FULL: 36,
    EZRA_FULL: 10,
    NEHEMIAH_FULL: 13,
    ESTHER_FULL: 10,
    JOB_FULL: 42,
    PSALMS_FULL: 150,
    PROVERBS_FULL: 31,
    ECCLESIASTES_FULL: 12,
    SONG_OF_SOLOMON_FULL: 8,
    ISAIAH_FULL: 66,
    JEREMIAH_FULL: 52,
    LAMENTATIONS_FULL: 5,
    EZEKIEL_FULL: 48,
    DANIEL_FULL: 12,
    HOSEA_FULL: 14,
    JOEL_FULL: 3,
    AMOS_FULL: 9,
    OBADIAH_FULL: 1,
    JONAH_FULL: 4,
    MICAH_FULL: 7,
    NAHUM_FULL: 3,
    HABAKKUK_FULL: 3,
    ZEPHANIAH_FULL: 3,
    HAGGAI_FULL: 2,
    ZECHARIAH_FULL: 14,
    MALACHI_FULL: 4,
    MATTHEW_FULL: 28,
    MARK_FULL: 16,
    LUKE_FULL: 24,
    JOHN_FULL: 21,
    ACTS_FULL: 28,
    ROMANS_FULL: 16,
    CORINTHIANS_1_FULL: 16,
    CORINTHIANS_2_FULL: 13,
    GALATIANS_FULL: 6,
    EPHESIANS_FULL: 6,
    PHILIPPIANS_FULL: 4,
    COLOSSIANS_FULL: 4,
    THESSALONIANS_1_FULL: 5,
    THESSALONIANS_2_FULL: 3,
    TIMOTHY_1_FULL: 6,
    TIMOTHY_2_FULL: 4,
    TITUS_FULL: 3,
    PHILEMON_FULL: 1,
    HEBREWS_FULL: 13,
    JAMES_FULL: 5,
    PETER_1_FULL: 5,
    PETER_2_FULL: 3,
    JOHN_1_FULL: 5,
    JOHN_2_FULL: 1,
    JOHN_3_FULL: 1,
    JUDE_FULL: 1,
    REVELATION_FULL: 22,
}
NUMBER_OF_CHAPTERS_PER_BOOK_KR = {
    GENESIS_KR: 50,
    EXODUS_KR: 40,
    LEVITICUS_KR: 27,
    NUMBERS_KR: 36,
    DEUTERONOMY_KR: 34,
    JOSHUA_KR: 24,
    JUDGES_KR: 21,
    RUTH_KR: 4,
    SAMUEL_1_KR: 31,
    SAMUEL_2_KR: 24,
    KINGS_1_KR: 22,
    KINGS_2_KR: 25,
    CHRONICLES_1_KR: 29,
    CHRONICLES_2_KR: 36,
    EZRA_KR: 10,
    NEHEMIAH_KR: 13,
    ESTHER_KR: 10,
    JOB_KR: 42,
    PSALMS_KR: 150,
    PROVERBS_KR: 31,
    ECCLESIASTES_KR: 12,
    SONG_OF_SOLOMON_KR: 8,
    ISAIAH_KR: 66,
    JEREMIAH_KR: 52,
    LAMENTATIONS_KR: 5,
    EZEKIEL_KR: 48,
    DANIEL_KR: 12,
    HOSEA_KR: 14,
    JOEL_KR: 3,
    AMOS_KR: 9,
    OBADIAH_KR: 1,
    JONAH_KR: 4,
    MICAH_KR: 7,
    NAHUM_KR: 3,
    HABAKKUK_KR: 3,
    ZEPHANIAH_KR: 3,
    HAGGAI_KR: 2,
    ZECHARIAH_KR: 14,
    MALACHI_KR: 4,
    MATTHEW_KR: 28,
    MARK_KR: 16,
    LUKE_KR: 24,
    JOHN_KR: 21,
    ACTS_KR: 28,
    ROMANS_KR: 16,
    CORINTHIANS_1_KR: 16,
    CORINTHIANS_2_KR: 13,
    GALATIANS_KR: 6,
    EPHESIANS_KR: 6,
    PHILIPPIANS_KR: 4,
    COLOSSIANS_KR: 4,
    THESSALONIANS_1_KR: 5,
    THESSALONIANS_2_KR: 3,
    TIMOTHY_1_KR: 6,
    TIMOTHY_2_KR: 4,
    TITUS_KR: 3,
    PHILEMON_KR: 1,
    HEBREWS_KR: 13,
    JAMES_KR: 5,
    PETER_1_KR: 5,
    PETER_2_KR: 3,
    JOHN_1_KR: 5,
    JOHN_2_KR: 1,
    JOHN_3_KR: 1,
    JUDE_KR: 1,
    REVELATION_KR: 22,
}
