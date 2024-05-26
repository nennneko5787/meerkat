from lexer import lexer

# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token = None
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
            if self.token_index + 1 < len(self.tokens):
                self.next_token = self.tokens[self.token_index + 1]
            else:
                self.next_token = None
        else:
            self.current_token = None
            self.next_token = None

    def consume(self, token_type):
        if self.current_token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected {token_type}, found {self.current_token[0]}")

    def parse_expression(self):
        left = self.parse_term()

        while self.current_token[0] in ['ADD', 'SUBTRACT']:
            token_type = self.current_token[0]
            self.advance()
            right = self.parse_term()

            if token_type == 'ADD':
                left += right
            elif token_type == 'SUBTRACT':
                left -= right

        return left

    def parse_term(self):
        left = self.parse_factor()

        while self.current_token[0] in ['MULTIPLY', 'DIVIDE']:
            token_type = self.current_token[0]
            self.advance()
            right = self.parse_factor()

            if token_type == 'MULTIPLY':
                left *= right
            elif token_type == 'DIVIDE':
                if right == 0:
                    raise ValueError("Division by zero")
                left /= right

        return left

    def parse_factor(self):
        if self.current_token[0] == 'NUMBER':
            number = float(self.current_token[1])
            self.advance()
            return number
        elif self.current_token[0] == 'LEFT_PAREN':
            self.advance()
            result = self.parse_expression()
            self.consume('RIGHT_PAREN')
            return result
        else:
            raise SyntaxError("Invalid syntax")

# テスト用コード
if __name__ == "__main__":
    code = """
    public group HelloGroup {
        public func <@GroupEvent.Init> init(me: HelloGroup) {
            me.message = "Hello";
        }

        public func say(me: HelloGroup) {
            console.info(me.message);
        }
    }

    public group Replica<HelloGroup> ByeGroup {
        public func <@Replace.GroupEvent.Init> init(me: HelloGroup) {
            me.message = "Bye";
        }
    }

    public runner main() {
        hello = HelloGroup();
        bye = ByeGroup();

        hello.say(); # Hello
        bye.say(); # Bye
    }
    """

    # Lexerを使用してトークンを生成
    tokens = list(lexer(code))

    # Parserを使用して式を解析し、コードを実行
    parser = Parser(tokens)
    while parser.current_token:
        if parser.current_token[0] == 'RUNNER_KEYWORD':
            parser.consume('RUNNER_KEYWORD')
            parser.consume('IDENTIFIER')
            parser.consume('LEFT_PAREN')
            parser.consume('RIGHT_PAREN')
            parser.consume('LEFT_BRACE')
            while parser.current_token[0] != 'RIGHT_BRACE':
                if parser.current_token[0] == 'IDENTIFIER':
                    variable_name = parser.current_token[1]
                    parser.advance()
                    parser.consume('EQUALS')
                    result = parser.parse_expression()
                    print(f"{variable_name} = {result}")
                    parser.consume('SEMICOLON')
                else:
                    parser.advance()
            parser.consume('RIGHT_BRACE')
        else:
            parser.advance()