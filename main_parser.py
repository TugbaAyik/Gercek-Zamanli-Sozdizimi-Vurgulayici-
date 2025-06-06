import sys
sys.stdout.reconfigure(encoding='utf-8')

from lexer_module import lexer  
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '')

    def eat(self, expected_type, expected_value=None):
        actual_type, actual_value = self.current_token()
        if actual_type == expected_type:
            if expected_value is None:
                # Eğer OPERATOR ise izin verilenler dışındakiler kabul edilmeyecek
                if expected_type == 'OPERATOR':
                    allowed_ops = ['+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>=', '=','++','--']
                    if actual_value not in allowed_ops:
                        raise SyntaxError(f"❌ Geçersiz operatör: '{actual_value}'")
                self.pos += 1
                print(f"✔️ Matched: {actual_type} -> {actual_value}")
            else:
                if actual_value == expected_value:
                    self.pos += 1
                    print(f"✔️ Matched: {actual_type} -> {actual_value}")
                else:
                    raise SyntaxError(f"❌ Syntax Error: Expected {expected_type} ('{expected_value}'), got {actual_type} ('{actual_value}')")
        else:
            raise SyntaxError(f"❌ Syntax Error: Expected {expected_type} ('{expected_value}'), got {actual_type} ('{actual_value}')")

    def parse(self):
        self.program()
        if self.pos < len(self.tokens):
            raise SyntaxError(f"❌ Extra input after valid program: {self.tokens[self.pos:]}")

    def program(self):
        self.statement_list()

    def statement_list(self):
        while self.pos < len(self.tokens) and self.current_token()[0] in ('KEYWORD',):
            self.statement()

    def statement(self): #Hangi keyword ile uyuşursa o bloğa girecek.
        tok_type, tok_val = self.current_token()
        if tok_val == 'var':
            self.var_declaration()
        elif tok_val == 'print':
            self.print_statement()
        elif tok_val == 'if':
            self.if_statement()
        elif tok_val=='while':
            self.while_statement()
        elif tok_val=='else':
            self.else_statement()
        else:
            raise SyntaxError(f"❌ Unknown statement start: {tok_val}")
    # Her statement için kendi uygun yapılarını tanımladım.
    def var_declaration(self):
        self.eat('KEYWORD', 'var')
        self.eat('IDENTIFIER')
        self.eat('OPERATOR', '=')
        self.expression()
        self.eat('DELIMITER', ';')

    def print_statement(self):
        self.eat('KEYWORD', 'print')
        self.eat('DELIMITER', '(')
        self.expression()
        self.eat('DELIMITER', ')')
        self.eat('DELIMITER', ';')

    def if_statement(self):
        self.eat('KEYWORD', 'if')
        self.eat('DELIMITER', '(')
        self.expression()
        self.eat('DELIMITER', ')')
        self.eat('DELIMITER', '{')
        self.statement_list()
        self.eat('DELIMITER', '}')
        if self.current_token() == ('DELIMITER', ';'):
            self.eat('DELIMITER', ';')
    def else_statement(self):
        self.eat('KEYWORD', 'else')
        self.eat('DELIMITER', '{')
        self.statement_list()
        self.eat('DELIMITER', '}')

    def while_statement(self):
        self.eat('KEYWORD', 'while')
        self.eat('DELIMITER', '(')
        self.expression()
        self.eat('DELIMITER', ')')
        self.eat('DELIMITER', '{')
        self.statement_list()
        self.eat('DELIMITER', '}')  

    def expression(self):
        self.comparison()

    def comparison(self):
        self.term()
        while self.current_token() in [
            ('OPERATOR', '=='), ('OPERATOR', '!='), ('OPERATOR', '<'),
            ('OPERATOR', '>'), ('OPERATOR', '<='), ('OPERATOR', '>=')
        ]:
            op = self.current_token()[1]
            self.eat('OPERATOR', op)
            self.term()

    def term(self):
        self.factor()
        while self.current_token() in [('OPERATOR', '+'), ('OPERATOR', '-')]:
            op = self.current_token()[1]
            self.eat('OPERATOR', op)
            self.factor()

    def factor(self):
        self.primary()
        while self.current_token() in [('OPERATOR', '*'), ('OPERATOR', '/')]:
            op = self.current_token()[1]
            self.eat('OPERATOR', op)
            self.primary()

    def primary(self):
        tok_type, tok_val = self.current_token()
        if tok_type in ('IDENTIFIER', 'NUMBER', 'STRING'):
            self.eat(tok_type)
        elif tok_type == 'DELIMITER' and tok_val == '(':
            self.eat('DELIMITER', '(')
            self.expression()
            self.eat('DELIMITER', ')')
        else:
            raise SyntaxError(f"❌ Invalid expression start: {self.current_token()}")


#Burada bir tane örnekle kodun doğru çalışıp çalışmadığını test ettim.
if __name__ == "__main__":
    code = '''
var a = 3 + 4 * (2 - 1);
if (a >= 7) {
    print("Merhaba Dünya");
};
'''
    tokens = lexer(code)
    print("Tokens:", tokens)

    parser = Parser(tokens)
    try:
        parser.parse()
    except SyntaxError as e:
        print(e)
