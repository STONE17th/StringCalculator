import random

operation = {'*': lambda x, y: x * y,
             '/': lambda x, y: x / y,
             '+': lambda x, y: x + y}


def create_expression(count: int) -> str:
    express = ''.join([str(random.randint(-20, 20)) + str(random.choice(['+', '-', '*', '/'])) for _ in range(count)])[
              :-1]
    return express.replace('--', '+').replace('+-', '-')


def convert_to_list(exp: str) -> list:
    exp = exp.replace(' ', '')
    signs = '+/*()'
    for sign in signs:
        exp = exp.replace(f'{sign}', f' {sign} ')
        exp = exp.replace(f'{sign}-', f' {sign} -')
    exp = exp.split()
    i = 0
    while i < len(exp):
        if '-' in exp[i][1:]:
            element = exp.pop(i).replace('-', ' + -').split()
            start, finish = exp[:i], exp[i:]
            exp = start + (element[1:] if element[0] == '+' else element) + finish
            i = 0
        i += 1
    exp = [int(char) if char.isdigit() or char[1:].isdigit() else char for char in exp]
    return exp[1:] if exp[0] == '+' else exp


def calculate(exp: list) -> int | float:
    while len(exp) > 1:
        if not calculate_operation(exp, ['*', '/']):
            return 'Ошибка! Деление на ноль!'
        calculate_operation(exp, ['+'])
    exp = exp[0]
    return int(exp) if exp == int(exp) else exp


def calculate_operation(exp: list, opers: list):
    while any(list(map(lambda x: x in opers, exp))):
        for i, char in enumerate(exp):
            if char in opers:
                if char == '/' and exp[i + 1] == 0:
                    return False
                exp[i - 1] = operation.get(char)(exp[i - 1], exp[i + 1])
                exp.pop(i)
                exp.pop(i)
                break
    return True


for _ in range(20):
    expression = create_expression(6)
    eval(expression)
    exp_list = convert_to_list(expression)
    print(f'eval = {eval(expression)}')
    print(f'{exp_list} = {calculate(exp_list)}')
