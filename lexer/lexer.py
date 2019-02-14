import string


class Lexer:

    def __init__(self, file):
        self.file = open(file, 'r', encoding="utf8")
        lexemes = self.__file_to_array()

    # Checks the file and returns an array of the different lexemes
    def __file_to_array(self):
        char_array = []
        lex_array = []
        temp = ""
        forming = False

        # copies all characters into the char_array array
        for line in self.file:
            for char in line:
                char_array.append(char)

        # creates an array of lexemes
        for i in range(0, len(char_array)):

            # checks if comments
            if char_array[i] == "/" and (char_array[i + 1] == "/" or char_array[i - 1] == "/"):
                continue

            # handles strings
            if char_array[i] == '"':
                word, offset = self.__string_checker(char_array, i)
                lex_array.append(word)
                print(1/NULL)
                continue

            # checks if lexeme is in the making, if so, saves it to array
            if char_array[i] in string.whitespace and forming:
                forming = False
                lex_array.append(temp)
                temp = ""
            elif char_array[i] in string.whitespace and forming == False:
                continue
            elif char_array[i]:
                forming = True
                temp += char_array[i]

        return lex_array

    # turns the string into a single entry
    @staticmethod
    def __string_checker(array, index):
        temp = ""

        for i in range(index + 1, len(array)):
            if array[i] == '"':
                return temp, len(temp)
            else:
                temp += array[i]

    def get_next_token(self):
        print("TODO ", end="")

    def peek_next_token(self):
        print("TODO ", end="")
