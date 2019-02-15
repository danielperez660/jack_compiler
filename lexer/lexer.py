import string


class Lexer:

    def __init__(self, file):
        self.file = open(file, 'r', encoding="utf8")
        lexemes = self.__file_to_lexeme()

    # Checks the file and returns an array of the different lexemes
    def __file_to_lexeme(self):
        char_array = []
        lex_array = []
        temp = ""
        separator = ['(', ')', '{', '}', ';']

        # Checks to see if any lexemes are forming
        forming = False
        word = False
        comment = False
        multicomm = False

        # copies all characters into the char_array array
        for line in self.file:
            for char in line:
                    char_array.append(char)

        # creates an array of lexemes
        for i in range(len(char_array)):

            # checks if single line comments
            if char_array[i] == "/" and char_array[i + 1] == "/" or comment == True:
                comment = True
                if char_array[i] == "\n":
                    comment = False
                continue

            # checks if multi line comment
            if multicomm == True and (char_array[i-1] == "*" and char_array[i] == "/" ):
                multicomm = False
                continue
            elif (char_array[i] == "/" and char_array[i+1] == "*") or multicomm == True:
                multicomm = True
                continue

            # handles strings
            if word == True and char_array[i] != '"':
                temp += char_array[i]
                continue
            elif char_array[i] == '"':
                # checks if final or initial " in string
                if word == True:
                    lex_array.append(temp)

                word = not word
                temp = ""
                continue

            # checks if lexeme is in the making, if so, saves it to array
            if char_array[i] in string.whitespace and forming:
                forming = False
                lex_array.append(temp)
                temp = ""
            elif char_array[i] in string.whitespace and forming == False:
                # ignores collective white spaces
                continue
            elif char_array[i] == "\n":
                # makes sure not to sav next line chars
                continue
            elif char_array[i] in separator:
                # finds that next char is separator so adds old string to list and adds separator
                if forming == True:
                    forming = False
                    lex_array.append(temp)
                    temp = ""
                lex_array.append(char_array[i])
                continue
            elif char_array[i]:
                forming = True
                temp += char_array[i]

        for i in lex_array:
            print(i)

        return lex_array

    def __lex_to_tokens(self):
        # TODO make this
        print("")

    def get_next_token(self):
        print("TODO ", end="")

    def peek_next_token(self):
        print("TODO ", end="")
