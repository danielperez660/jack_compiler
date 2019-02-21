import string


class Token:

    def __init__(self, file):
        self.file = open(file, 'r', encoding="utf8")
        self.lexemes = self.__file_to_lexeme()
        self.tokens = self.__lex_to_tokens()

    # Checks the file and returns an array of the different lexemes
    def __file_to_lexeme(self):
        char_array = []
        line_no = []
        lex_array = []
        temp = ""
        line = 0
        separator = ['(', ')', '{', '}', ';', '.', ',']

        # Checks to see if any lexemes are forming
        forming = False
        word = False
        comment = False
        multicomm = False

        # copies all characters into the char_array array
        for lines in self.file:
            line += 1
            for char in lines:
                    char_array.append(char)
                    line_no.append(line)

        # creates an array of lexemes
        for i in range(len(char_array)):

            # checks if single line comments
            if char_array[i] == "/" and char_array[i + 1] == "/" or comment:
                comment = True
                if char_array[i] == "\n":
                    comment = False
                continue

            # checks if multi line comment
            if multicomm and (char_array[i-1] == "*" and char_array[i] == "/" ):
                multicomm = False
                continue
            elif (char_array[i] == "/" and char_array[i+1] == "*") or multicomm:
                multicomm = True
                continue

            # handles strings
            if word and char_array[i] != '"':
                temp += char_array[i]
                continue
            elif char_array[i] == '"':
                # checks if final or initial " in string
                if word:
                    lex_array.append(('string', temp, line_no[i]))

                word = not word
                temp = ""
                continue

            # checks if lexeme is in the making, if so, saves it to array
            if char_array[i] in string.whitespace and forming:
                forming = False
                lex_array.append((temp, line_no[i]))
                temp = ""
            elif char_array[i] in string.whitespace and not forming:
                # ignores collective white spaces
                continue
            elif char_array[i] == "\n":
                # makes sure not to sav next line chars
                continue
            elif char_array[i] in separator:
                # finds that next char is separator so adds old string to list and adds separator
                if forming:
                    forming = False
                    lex_array.append((temp, line_no[i]))
                    temp = ""
                lex_array.append((char_array[i], line_no[i]))
                continue
            elif char_array[i]:
                forming = True
                temp += char_array[i]

        lex_array.append(("EOF", line_no[i]))

        return lex_array

    def __lex_to_tokens(self):
        tokens = []

        keyword = ['if', 'let', 'do', 'else', 'while', 'return']
        symbol = ['(', ')', '{', '}', ';', '.', ',']
        components = ['class', 'constructor', 'function', 'method']
        types = ['void', 'int', 'boolean', 'char']
        declar = ['var', 'static', 'field']
        constant = ['true', 'false', 'null']

        ops = {
            "+": 'addop',
            "*": 'mullop',
            "-": 'subop',
            "|": 'orop',
            "~": 'complimentop',
            "/": 'divop',
            "=": 'assignop',
            "&": 'andop',
            "%": 'modop',
            "<": 'lessop',
            ">": 'moreop'
            }

        for i in self.lexemes:

            if i[0] in keyword:
                tokens.append((i[0], i[1], "keyword"))
                continue
            elif i[0] in constant:
                tokens.append((i[0], i[1], "constant"))
                continue
            elif i[0] == "string":
                tokens.append((i[1], i[2], "string"))
                continue
            elif i[0] in "this":
                tokens.append((i[0], i[1], "reference"))
                continue
            elif i[0] in types:
                tokens.append((i[0], i[1], "type"))
                continue
            elif i[0] in symbol:
                tokens.append((i[0], i[1], "symbol"))
            elif i[0] in ops:
                tokens.append((i[0], i[1], ops[i[0]]))
            elif i[0] in components:
                tokens.append((i[0], i[1], "component"))
            elif i[0] in declar:
                tokens.append((i[0], i[1], "declaration"))
            elif i[0] == "EOF":
                tokens.append((i[0], i[1], "EOF"))
            elif i[0].isalpha() or i[0][0] == "_":
                tokens.append((i[0], i[1], "identifier"))
            elif i[0].isnumeric():
                tokens.append((i[0], i[1], "num"))

        return tokens

    def get_next_token(self):
        temp = self.tokens[0]
        del self.tokens[0]
        return temp

    def peek_next_token(self):
        return self.tokens[0]
