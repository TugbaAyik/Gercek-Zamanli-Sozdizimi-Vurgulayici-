# Lexical analiz için transition tablo oluşturuyoruz.
transition_table = {
    'start': {
        'letter': 'id',
        'digit': 'number',
        '"': 'string_start',
        '=': 'equals',
        ';': 'semicolon',
        '(': 'lparen',
        ')': 'rparen',
        'whitespace': 'start',
    },
    'id': {
        'letter': 'id',
        'digit': 'id',
        'other': 'done'
    },
    'number': {
        'digit': 'number',
        'other': 'done'
    },
    'string_start': {
        'other': 'string',
        '"': 'string_end'
    },
    'string': {
        '"': 'string_end',
        'other': 'string'
    }
}

# Bu dil de tanımlı olan anahtar kelimeler:
keywords = {'var', 'print', 'if', 'else', 'while'}

def char_type(char):
    if char.isalpha():
        return 'letter'
    elif char.isdigit():
        return 'digit'
    elif char.isspace():
        return 'whitespace'
    elif char in ('=', ';', '(', ')'):
        return char
    elif char == '"':
        return '"'
    else:
        return 'other'
    
def lexer(code):
    tokens = []
    i = 0
    while i < len(code):
        c = code[i] # Girilen karakteri alıp ne olduğunu kontrol ediyoruz.
        if c.isspace():
            i += 1 # Karakter boşluksa geçiyoruz.
        elif c.isalpha():
            start = i
            while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                i += 1 
            word = code[start:i] # Karakterler harf ise kelime oluşturuyoruz.
            if word in keywords: # Kelimenin hangi keyword olduğunu buluyoruz.
                tokens.append(('KEYWORD', word))
            else:
                tokens.append(('IDENTIFIER', word))
        elif c.isdigit():
            start = i
            while i < len(code) and code[i].isdigit():
                i += 1
            tokens.append(('NUMBER', code[start:i]))# Karakterler sayı ise NUMBER oluyor.
        elif c == '"':
            i += 1
            start = i
            while i < len(code) and code[i] != '"':
                i += 1
            if i >= len(code):
                raise SyntaxError("Unterminated string literal")
            tokens.append(('STRING', code[start:i])) # Tırnak işareti ile başlıyorsa bu bir STRING demektir.
            i += 1  
        elif c in '=!<>+-*/;(){}':
            # Karakter operatör ise hangisi olduğunu buluyoruz.
            if c == '=':
                if i+1 < len(code) and code[i+1] == '=':
                    tokens.append(('OPERATOR', '=='))
                    i += 2
                else:
                    tokens.append(('OPERATOR', '='))
                    i += 1
            elif c == '!':
                if i+1 < len(code) and code[i+1] == '=':
                    tokens.append(('OPERATOR', '!='))
                    i += 2
                else:
                    raise SyntaxError(f"Unknown operator ! at position {i}")
            elif c == '<':
                if i+1 < len(code) and code[i+1] == '=':
                    tokens.append(('OPERATOR', '<='))
                    i += 2
                else:
                    tokens.append(('OPERATOR', '<'))
                    i += 1
            elif c == '>':
                if i+1 < len(code) and code[i+1] == '=':
                    tokens.append(('OPERATOR', '>='))
                    i += 2
                else:
                    tokens.append(('OPERATOR', '>'))
                    i += 1
            elif c in '+-*/':
                tokens.append(('OPERATOR', c))
                i += 1
            else:  # ; (noktalı virgül), parantezler, süslü parantezler
                tokens.append(('DELIMITER', c))
                i += 1
        else:
            i += 1  # tanımsız karakterleri atlıyoruz           

    return tokens
