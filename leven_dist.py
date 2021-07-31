import numpy as np
import re


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y
    
    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )
        print(matrix)

    return matrix[size_x - 1, size_y - 1]


def check_name_set(db_name, dam_name):
    dam_name = dam_name.replace('(', '').lower()
    dam_name = dam_name.replace(')', '').lower()
    db_name = db_name.lower().strip()
    dam_name = re.sub('\s+', ' ', dam_name).strip()

    db_list = db_name.split(' ')
    dam_list = dam_name.split(' ')
    db_set = set(db_list)
    dam_set = set(dam_list)
    com = db_set & dam_set
    print(db_set.difference(dam_set))
    print(dam_set.difference(db_set))
    if len(com) != 0:
        if com == dam_set:
            print('{} {}'.format(com, dam_set))
            return db_name
        else:
            if len(db_set.difference(dam_set)) > 2 or len(dam_set.difference(db_set)) > 2:
                return 'no'
            else:
                return ''
    else:
        return ''


if __name__ == '__main__':
    r = check_name_set('subra nidhya vimal bin', 'nidhya subram imal bi')
    levenshtein_distance = levenshtein('subra nidhya', 'subram nidhya')

    print(f"{levenshtein_distance} number of changes are needed to make both string equal")
