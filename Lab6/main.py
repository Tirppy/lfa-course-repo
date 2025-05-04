import re
from enum import Enum
from dataclasses import dataclass
from typing import List

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
    ('COMMENT',   r'\#.*'),
    ('PIPE',      r'\|\>'),
    ('STRING',    r'"[^"\n]*"'),
    ('TIME',      r'\d{2}:\d{2}'),
    ('NUMBER',    r'\d+(\.\d+)?[sx]?'),
    ('IDENT',     r'[A-Za-z_][A-Za-z0-9_]*'),
    ('NEWLINE',   r'\n'),
    ('SKIP',      r'[ \t]+'),
    ('UNKNOWN',   r'.'),
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
            else:
                if kind == 'IDENT' and value in KEYWORDS:
                    kind = value.upper()
                if kind == 'UNKNOWN':
                    kind = 'UNKNOWN'
                tokens.append(Token(kind, value, line, column))
            pos = mo.end()
            mo = GET_TOKEN(self.text, pos)
        tokens.append(Token('EOF', '', line, column))
        return tokens

class TokenType(Enum):
    COMMENT    = 'COMMENT'
    PIPE       = 'PIPE'
    STRING     = 'STRING'
    TIME       = 'TIME'
    NUMBER     = 'NUMBER'
    IDENT      = 'IDENT'
    UNKNOWN    = 'UNKNOWN'
    EOF        = 'EOF'
    OPEN       = 'OPEN'; FADE    = 'FADE'; TRIM    = 'TRIM'
    SAVE       = 'SAVE'; SHOW    = 'SHOW'; AS      = 'AS'
    DELAY      = 'DELAY'; VOLUME = 'VOLUME'; MIX    = 'MIX'
    SPLIT      = 'SPLIT'; LOOP    = 'LOOP'; JOIN    = 'JOIN'
    OVERLAY    = 'OVERLAY'; OVERLAYAUDIO='OVERLAYAUDIO'; EXPORT='EXPORT'
    FORMAT     = 'FORMAT'; RESOLUTION='RESOLUTION'; BITRATE='BITRATE'
    EXTRACT    = 'EXTRACT'; CUT     = 'CUT'; INSERT = 'INSERT'
    ROTATE     = 'ROTATE'; BLANK   = 'BLANK'; OVERWRITE='OVERWRITE'
    OPERLAP    = 'OPERLAP'

KEYWORD_TYPES = { TokenType[k.upper()] for k in KEYWORDS }

@dataclass
class Arg:
    type: TokenType
    value: str

    def __repr__(self):
        return f"Arg(type={self.type}, value={self.value!r})"

@dataclass
class Command:
    name: str
    args: List[Arg]

    def __repr__(self):
        return f"Command(name={self.name!r}, args={self.args})"

    def pretty(self, indent: int = 4) -> str:
        pad = ' ' * indent
        lines = [f"{pad}Command(name={self.name!r}, args=["]
        for a in self.args:
            lines.append(f"{pad*2}{a!r},")
        lines.append(f"{pad}])")
        return "\n".join(lines)

@dataclass
class Pipeline:
    commands: List[Command]

    def __repr__(self):
        return f"Pipeline(commands={self.commands})"

    def pretty(self, indent: int = 2) -> str:
        pad = ' ' * indent
        lines = [f"{pad}Pipeline(commands=["]
        for c in self.commands:
            lines.append(c.pretty(indent + 2))
        lines.append(f"{pad}])")
        return "\n".join(lines)

@dataclass
class Program:
    pipelines: List[Pipeline]

    def __repr__(self):
        return f"Program(pipelines={self.pipelines})"

    def pretty(self) -> str:
        lines = ["Program(pipelines=["]
        for p in self.pipelines:
            lines.append(p.pretty(2))
        lines.append("])")
        return "\n".join(lines)

class Parser:
    def __init__(self, tokens):
        self.tokens = [
            tok if isinstance(tok.type, TokenType)
            else Token(TokenType[tok.type], tok.value, tok.line, tok.column)
            for tok in tokens
        ]
        self.pos = 0
        self.current_token = self.tokens[0]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def expect(self, ttype):
        if self.current_token.type is ttype:
            tok = self.current_token
            self.advance()
            return tok
        raise SyntaxError(f"Expected {ttype}, got {self.current_token.type} at line {self.current_token.line}")

    def parse(self):
        pipelines = []
        while self.current_token.type != TokenType.EOF:
            pipelines.append(self.parse_pipeline())
        return Program(pipelines)

    def parse_pipeline(self):
        cmds = [self.parse_command()]
        while self.current_token.type == TokenType.PIPE:
            self.advance()
            cmds.append(self.parse_command())
        return Pipeline(cmds)

    def parse_command(self):
        name_tok = self.current_token
        if name_tok.type is TokenType.IDENT or name_tok.type in KEYWORD_TYPES:
            self.advance()
        else:
            raise SyntaxError(f"Unexpected token {name_tok.type} at command start")
        args = []
        while self.current_token.type in {TokenType.STRING, TokenType.TIME, TokenType.NUMBER, TokenType.IDENT}:
            tok = self.current_token
            args.append(Arg(tok.type, tok.value))
            self.advance()
        return Command(name_tok.value, args)

if __name__ == '__main__':
    code = r'''
        open vid1 "file.mp4" |> trim 5s |> save "out.mp4"
    '''
    lexer = Lexer(code)
    toks = lexer.tokenize()
    parser = Parser(toks)
    ast = parser.parse()
    print(ast.pretty())
