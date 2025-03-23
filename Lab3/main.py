import re

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, {self.line}, {self.column})"

KEYWORDS = {
    'open', 'fade', 'trim', 'save', 'show', 'as', 'delay', 'volume', 'mix',
    'split', 'loop', 'join', 'overlay', 'overlayAudio', 'export', 'format',
    'resolution', 'bitrate', 'extract', 'cut', 'insert', 'rotate', 'blank',
    'overwrite', 'operlap'
}

TOKEN_SPECS = [
    ('COMMENT',   r'\#.*'),             # Comment
    ('PIPE',      r'\|\>'),             # Pipeline operator
    ('STRING',    r'"[^"\n]*"'),        # String literal
    ('TIME',      r'\d{2}:\d{2}'),      # Time format (e.g., 00:05, 01:00)
    ('NUMBER',    r'\d+(\.\d+)?[sx]?'), # Number (with optional decimal and suffix)
    ('IDENT',     r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifier (or keyword)
    ('NEWLINE',   r'\n'),               # Newline
    ('SKIP',      r'[ \t]+'),           # Skip spaces/tabs
    ('UNKNOWN',   r'.'),                # Any other character
]
TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECS)
GET_TOKEN = re.compile(TOKEN_REGEX).match

class Lexer:
    def __init__(self, text):
        self.text = text

    def tokenize(self):
        tokens = []
        line, pos = 1, 0
        mo = GET_TOKEN(self.text, pos)

        while mo:
            kind = mo.lastgroup
            value = mo.group(kind)
            column = mo.start() - self.text.rfind('\n', 0, mo.start())

            if kind == 'NEWLINE':
                line += 1
            elif kind == 'SKIP':
                pass 
            elif kind == 'IDENT' and value in KEYWORDS:
                kind = value.upper() 
            elif kind == 'UNKNOWN':
                kind = "UNKNOWN" 

            if kind not in {'NEWLINE', 'SKIP'}:
                tokens.append(Token(kind, value, line, column))

            pos = mo.end()
            mo = GET_TOKEN(self.text, pos)

        return tokens

if __name__ == '__main__':
    code = r'''
# creates file2 string
file2 "C:\Downloads\New video1.mp4"

# creates vid2
open vid2 file2

# creates vid1, edit and save
open vid1 "C:\Downloads\Video.mp4" |> blank |> save ".../../audio.mp3" |> show |> as audio1

# work with vid1 , save and download results
vid1 |> trim 5s |> as vid1 |> overwrite audio1 00:05 10s |> operlap vid2 01:00 |> show |> as vid6 |> save ".../../changed.mp4"
    '''

    lexer = Lexer(code)
    token_list = lexer.tokenize()
    for token in token_list:
        print(token)
