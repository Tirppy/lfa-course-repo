import re
from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

KEYWORDS = {
    'open', 'fade', 'trim', 'save', 'show', 'as', 'delay', 'volume', 'mix',
    'split', 'loop', 'join', 'overlay', 'overlayAudio', 'export', 'format',
    'resolution', 'bitrate', 'extract', 'cut', 'insert', 'rotate', 'blank',
    'overwrite', 'operlap'
}

class Lexer:
    def __init__(self, text: str):
        self.text = text

    def tokenize(self) -> List[Token]:
        tokens = []
        token_specification = [
            ('COMMENT',   r'\#.*'),                         # Comment from '#' to end of line
            ('PIPE',      r'\|\>'),                         # Pipeline operator
            ('STRING',    r'"[^"\n]*"'),                    # String literal (simplified, no escaped quotes)
            ('TIME',      r'\d{2}:\d{2}'),                   # Time format e.g., 00:05, 01:00
            ('NUMBER',    r'\d+(\.\d+)?([sx])?'),            # Number, with optional decimal and suffix (s, x)
            ('IDENT',     r'[A-Za-z_][A-Za-z0-9_]*'),        # Identifier (or keyword)
            ('NEWLINE',   r'\n'),                           # Newline
            ('SKIP',      r'[ \t]+'),                       # Skip over spaces and tabs
            ('MISMATCH',  r'.'),                            # Any other character (error)
        ]
        tok_regex = '|'.join(f'(?P<{tok_type}>{pattern})'
                             for tok_type, pattern in token_specification)
        get_token = re.compile(tok_regex).match

        line = 1
        pos = 0
        mo = get_token(self.text, pos)
        while mo is not None:
            kind = mo.lastgroup
            value = mo.group(kind)
            column = mo.start() - self.text.rfind('\n', 0, mo.start())
            if kind == 'NEWLINE':
                line += 1
                pos = mo.end()
                mo = get_token(self.text, pos)
                continue
            elif kind == 'SKIP':
                pos = mo.end()
                mo = get_token(self.text, pos)
                continue
            elif kind == 'IDENT':
                if value in KEYWORDS:
                    kind = value.upper()
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected character {value!r} on line {line} column {column}')
            tokens.append(Token(kind, value, line, column))
            pos = mo.end()
            mo = get_token(self.text, pos)
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
