original_string = '10* 54 * (9+2)/5*10 +25'

operations = {'+': lambda x, y: x + y,
              '-': lambda x, y: x - y,
              '*': lambda x, y: x * y,
              '/': lambda x, y: x / y}


def str_to_list(example: str) -> list:
    signs = '+*/()[]'
    example = example.replace(' ', '')
    example = example.replace('-(', '-1*(').replace('(-', '(0-')
    for sign in signs:
        example = example.replace(f'{sign}', f' {sign} ').replace(f'{sign}-', f' {sign} -')
    example = example.replace('-', ' + -')
    example = example.split()
    example = list(map(lambda x: float(x) if x.replace('.', '').replace('-', '').isdigit() else x, example))
    return example


def calculate(expression: list) -> int | float:
    while len(expression) > 1:
        simple_calculate(expression, ['*', '/'])
        simple_calculate(expression, ['+'])
    return expression[0]


def simple_calculate(expression: list, oper: list) -> list:
    i = 0
    while any(list(map(lambda x: x in oper, expression))):
        if expression[i] in oper:
            expression[i - 1] = operations.get(expression[i])(expression[i - 1], expression[i + 1])
            expression.pop(i)
            expression.pop(i)
            i = 0
        i += 1
    return expression


def check_parentheses(expression: list) -> int | float:
    while len(expression) > 1:
        k = 0
        while any(list(map(lambda x: x in ['(', ')', '[', ']'], expression))):
            if expression[k] in ['(', '[']:
                start_index = k
            if expression[k] in [')', ']']:
                finish_index = k
                expression = expression[:start_index] + [
                    calculate(expression[start_index + 1:finish_index])] + expression[finish_index + 1:]
                k = 0
                continue

            k += 1
        calculate(expression)
    return int(expression[0]) if int(expression[0]) == expression[0] else expression[0]


tst_bunch = ["123.3 +      123 + 123 - 46 * 87566 / 98765 + 9087",
             "123.3",
             "4 * 4 * 4 * 4",
             "4 * 4 / 4 * 4",
             "((2 * 3 - (20 - 5)) - (3 * (10 - 2))) * (-1)",
             "((2 * 3 - (20 - 5)) - ((3 * (10 - 2)))) * (-1)",
             "14 + ((2 * 3 - (20 - 5)) - ((3 * (10 - 2)))) * (-1)"]


def my_eval(expression: str) -> int | float:
    str_exp = str_to_list(expression)
    return check_parentheses(str_exp)


for exp in tst_bunch:
    print(my_eval(exp))
    # print(eval(exp) == my_eval(exp))
