import random

operation = {'*': lambda x, y: x * y,
             '/': lambda x, y: x / y,
             '+': lambda x, y: x + y}


def create_expression(count: int) -> str:
    express = ''.join([str(random.randint(-20, 20)) +
                       str(random.choice(['+', '-', '*', '/'])) for _ in range(count)])[:-1]
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
            element = exp.pop(i)
            element = element.replace('-', ' + -').split()
            start, finish = exp[:i], exp[i:]
            exp = start + (element[1:] if element[0] == '+' else element) + finish
            i = 0
        i += 1
    exp = [int(char) if char.isdigit() or char[1:].isdigit() else char for char in exp]
    return exp[1:] if exp[0] == '+' else exp


def calculate(exp: list, accuracy: int = 2) -> int | float | str:
    while len(exp) > 1:
        if not calculate_operation(exp, ['*', '/']):
            return 'Ошибка! Деление на ноль!'
        calculate_operation(exp, ['+'])
    exp = exp[0]
    return int(exp) if exp == int(exp) else round(exp, accuracy)


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


def check_parentheses(exp: list) -> int | float:
    while '(' in exp and ')' in exp:
        deque_bracket = []
        for i, char in enumerate(exp):
            if char == '(':
                deque_bracket.insert(0, i)
            elif char == ')':
                start_index = deque_bracket.pop(0)
                buffered = calculate(exp[start_index + 1:i])
                if exp[start_index - 1] != '-':
                    exp = exp[:start_index] + [buffered] + exp[i + 1:]
                else:
                    exp = exp[:start_index - 1] + (
                        [-buffered] if isinstance(exp[start_index - 2],
                                                  str) else ['+', -buffered]) + exp[i + 1:]
                break
    return calculate(exp)


def self_eval(exp: str) -> int | float:
    exp_list = convert_to_list(exp)
    return check_parentheses(exp_list)


# for _ in range(20):
#     expression = create_expression(6)
#     print(expression)
#     eval(expression)
#     exp_list = convert_to_list(expression)
#     print(f'eval = {eval(expression)}')
#     print(f'{exp_list} = {calculate(exp_list, 5)}')

expres = "((2 * 3 - (20 - 5)) - ((3 * (10 - 2))) * (-1))"
print('eval')
print(eval(expres))
print('my_eval:')
print(f'{expres} = {self_eval(expres)}')
