import os
import re

from config import settings

__all__ = (
    'FILE_DIR',
    'PATH_BIBLE_KJV',
    'PATH_BIBLE_HKJ',
    'PATTERN_LINE',
    'ENGLISH',
    'KOREAN',
    'KJV',
    'HKJ',
    'HJV',
    'KJV_VERBOSE',
    'HKJ_VERBOSE',
    'HJV_VERBOSE',
    'VERSION_TO_PATH',
)

# file paths
FILE_DIR = os.path.join(settings.STATIC_DIR, 'files')
PATH_BIBLE_KJV = os.path.join(FILE_DIR, 'kjv-the-holy-bible.txt')
PATH_BIBLE_HKJ = os.path.join(FILE_DIR, 'hkj-the-holy-bible.txt')
PATH_BIBLE_HJV = os.path.join(FILE_DIR, 'hjv-the-holy-bible.txt')

# indexing pattern
PATTERN_LINE = re.compile(r'^(?P<book>\D+)(?P<chapter>\d{1,3}):(?P<verse>\d{1,3})[ ]+(?P<content>.+)')

# scripture model attribute db input value
ENGLISH = 'en'
KOREAN = 'kr'

# scripture identification variables
KJV = 'KJV'
HKJ = 'HKJV'
HJV = 'HJV'

KJV_VERBOSE = 'King James Version'
HKJ_VERBOSE = '한글 킹제임스'
HJV_VERBOSE = '흠정역'

# Version to File Path Dictionary
VERSION_TO_PATH = {
    KJV: PATH_BIBLE_KJV,
    HKJ: PATH_BIBLE_HKJ,
    HJV: PATH_BIBLE_HJV,
}
