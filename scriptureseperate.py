with open('relativity', 'rt') as f:
    for line in f:
        pass


def head(string):
    title_letters = []
    for letter in string:
        if letter in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
            break
        title_letters.append(letter)
    title = ''.join(title_letters)
    return title
