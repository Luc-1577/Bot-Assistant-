def split_expression(expression):
    # Lista de operadores suportados
    operators = ['*', '/', '+', '-']

    # Inicializa as listas para armazenar valores e operadores
    values = []
    operators_found = []

    # Inicializa variáveis auxiliares
    current_value = ''
    
    for char in expression:
        if char.isdigit() or char == '.':
            # O caractere é um dígito ou ponto decimal, portanto, faz parte de um valor
            current_value += char
        elif char in operators:
            # O caractere é um operador, portanto, adiciona o valor atual à lista de valores
            if current_value:
                values.append(float(current_value))
                current_value = ''
            operators_found.append(char)

    # Adiciona o último valor, se houver
    if current_value:
        values.append(float(current_value))

    return values, operators_found

def calculate_expression(values, operators):
    # Verifica se há multiplicação ou divisão na lista de operadores
    multiplication_or_division = '*' in operators or '/' in operators

    # Primeiro, realizamos todas as multiplicações e divisões, se houver
    if multiplication_or_division:
        i = 0
        while i < len(operators):
            if operators[i] == '*':
                values[i] *= values[i + 1]
                del values[i + 1]
                del operators[i]
            elif operators[i] == '/':
                if values[i + 1] == 0:
                    print("Error: Division by zero.")
                    return None
                values[i] /= values[i + 1]
                del values[i + 1]
                del operators[i]
            else:
                i += 1

    # Agora, realizamos as adições e subtrações
    result = values[0]
    for i in range(1, len(values)):
        if operators[i - 1] == '+':
            result += values[i]
        elif operators[i - 1] == '-':
            result -= values[i]

    return result

def calculus(user_input):
    values, operators = split_expression(user_input)

    if not operators or len(values) != len(operators) + 1:
        print("Error: Invalid expression.")

    result = calculate_expression(values, operators)

    if result is not None:
        return result

if __name__ == "__main__":
    user_input = input('Type the expression: ')
    calculus(user_input)