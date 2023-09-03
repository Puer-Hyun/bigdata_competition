import copy
import re

def place_process(data, place):
    '''
    좌석 구분을 위한 함수. 새로운 칼럼을 만든 df를 반환한다.
    '''
    specific_show = data[data.place == place]
    specific_show = specific_show.reset_index()

    floors = []
    blocks = []
    rows = []
    numbers = []

    for seat in specific_show['seat']:
        parts = seat.split(' ')

        if place == '콘서트홀':
            N = 3
            floor = parts[0][0]
            if '합창석' in seat:
                floor = str(N + 1)
                block = parts[1][0]
                row = parts[1].split('블록')[1].split('열')[0]
                number = parts[2]
            elif 'BOX' in seat:
                block = 'BOX'
                row = parts[1][3:]
                number = parts[2]
            else:
                block = parts[1][0]
                row = parts[1].split('블록')[1].split('열')[0]
                number = parts[2]

        elif place == 'IBK챔버홀':
            if len(parts) == 3:
                floor = int(parts[0][0])
                block = parts[1][:-1]
                row = int(parts[1][-1])
                number = int(parts[2])
            elif len(parts) == 4:
                floor = int(parts[0][0])
                block = parts[1][0]
                row = int(parts[2][:-1])
                number = int(parts[3])

        else:  # '리사이틀홀'
            if len(parts) == 3:
                floor = int(parts[0][0])
                block = 0
                row = int(parts[1][:-1])
                number = int(parts[2])
            elif len(parts) == 4:
                floor = int(parts[0][0])
                block = parts[1][3:]
                row = int(parts[2][:-1])
                number = int(parts[3])

        floors.append(floor)
        blocks.append(block)
        rows.append(row)
        numbers.append(number)

    specific_show['층'] = floors
    specific_show['블록'] = blocks
    specific_show['열'] = rows
    specific_show['번호'] = numbers

    return specific_show


def extract_age(discount_type):
    '''
    age 결측치를 채우기 위한 함수. discount_type을 이용해서 채운다.
    '''
    if re.search('청소년|학생할인', discount_type):
        return 10
    elif re.search('초/중/고/대|청년', discount_type):
        return 20
    elif re.search('대 학생|대학교|대학생', discount_type):
        return 20
    elif re.search('경로|실버|65세', discount_type):
        return 70
    elif re.search('임산부', discount_type):
        return 35
    elif re.search('음악전공자', discount_type):
        return 30
    elif re.search('29세', discount_type):
        return 20
    elif re.search('예비군', discount_type):
        return 30
    else:
        return None