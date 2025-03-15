### Course: Formal Languages & Finite Automata
### Author: Alexandru Cebotari

----

## Theory

### Lexical Analysis and Formal Language Theory Overview

Lexical analysis is the process of converting a sequence of characters into a sequence of tokens—an essential step in the compilation or interpretation of any language, be it programming, markup, or a domain-specific language (DSL).
This stage, often implemented via a lexer (or scanner/tokenizer), bridges the gap between raw text input and the structured data required for subsequent stages such as parsing and semantic analysis.

At its core, **lexical analysis** involves:
- **Input Processing:** Scanning the entire input text, reading it character by character.
- **Lexeme Identification:** Recognizing meaningful sequences of characters, known as lexemes, based on predefined patterns.
- **Token Generation:** Mapping these lexemes to token types (e.g., keywords, identifiers, literals, operators) which abstract the underlying content into a structured form for further analysis.

### Role of Regular Languages and Finite Automata

Lexical analyzers heavily rely on the principles of formal language theory:
- **Regular Languages:** The patterns that define valid tokens in a language can be expressed as regular expressions. Regular languages, recognized by finite automata, provide a rigorous mathematical framework to describe these patterns.
- **Finite Automata (FA):** There are two main types:
  - **Deterministic Finite Automata (DFA):** In DFAs, every state has exactly one transition for each input symbol. DFAs are efficient for tokenization because they guarantee a unique transition path for any given input, making them predictable and fast.
  - **Non-Deterministic Finite Automata (NFA):** NFAs allow multiple transitions for a single input symbol. Though conceptually simpler to design, NFAs are typically converted into DFAs for actual implementation in lexical analysis due to their efficiency in processing.

### Lexical Analysis in DSLs

When developing a lexer for a DSL—such as the video processing language described in this project—the following aspects are fundamental:
- **Token Patterns:** The lexer uses regular expressions to define patterns for various tokens such as keywords (e.g., `open`, `trim`, `save`), identifiers, string literals, numeric values (including integers and floats), and operators (like the pipeline operator `|>`).
- **State Transition:** As the lexer reads input characters, it transitions between states defined by the DFA, effectively categorizing input sequences into tokens. This state-driven approach ensures that each segment of the input is analyzed according to the specific rules of the DSL.
- **Error Handling:** Lexers must also address invalid inputs or unexpected symbols by signaling errors, which is crucial for maintaining robustness in any language processing system.

### Integrating Theory into Practice

Understanding the theoretical foundations—regular languages, finite automata, and formal grammar—empowers developers to design efficient lexers. For our video processing DSL:
- The lexer translates raw editing scripts into a structured token stream.
- This structured approach facilitates further processing such as parsing, where the token stream is transformed into an abstract syntax tree (AST) for subsequent operations like semantic analysis or code generation.
- Embracing these theoretical principles ensures that the language remains scalable, maintainable, and precise in its interpretation of complex editing commands.

By leveraging these well-established concepts from automata theory and formal languages, the lexer not only fulfills its role in tokenizing the input but also lays a robust foundation for building more advanced features in language processing and compiler design.

## Objectives

The primary objectives of this lab are to:

1. **Understand Lexical Analysis in the Context of a DSL:**
   - Gain a deep understanding of how lexical analysis converts raw text into a structured sequence of tokens.
   - Recognize the importance of lexers in the process of compiling or interpreting domain-specific languages, such as our video processing language.

2. **Design and Implement a Lexer for the Video Processing DSL:**
   - Develop a lexer that can process input scripts written in the video processing language.
   - Define token types for keywords, identifiers, string literals, numeric values, and operators (e.g., the pipeline operator `|>`).

3. **Support Complex Editing Commands:**
   - Ensure the lexer handles a wide range of commands specific to video editing, such as `open`, `trim`, `save`, `fade`, `overlay`, and `export`.
   - Allow for chaining of operations using a pipeline syntax to reflect the sequential processing of media editing tasks.

4. **Handle and Preserve Comments and Whitespace:**
   - Accurately capture and output comments as tokens, ensuring they are preserved in the token stream.
   - Properly skip irrelevant whitespace while maintaining positional information for error reporting.

5. **Integrate Robust Error Handling:**
   - Implement mechanisms to identify and report unrecognized characters or malformed tokens.
   - Ensure that the lexer can gracefully handle invalid input and provide informative error messages.

6. **Document and Test the Lexer Implementation:**
   - Create comprehensive documentation that explains the design decisions, token patterns, and overall functionality of the lexer.
   - Include sample input scripts and their corresponding token outputs to validate the correctness and robustness of the implementation.

## Implementation description

### 1. Token Data Structure

```
import re
from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int
```



### 2. Reserved Keywords

```
KEYWORDS = {
    'open', 'fade', 'trim', 'save', 'show', 'as', 'delay', 'volume', 'mix',
    'split', 'loop', 'join', 'overlay', 'overlayAudio', 'export', 'format',
    'resolution', 'bitrate', 'extract', 'cut', 'insert', 'rotate', 'blank',
    'overwrite', 'operlap'
}
```



### 3. Lexer Class and Initialization

```
class Lexer:
    def __init__(self, text: str):
        self.text = text
```



### 4. The Tokenize Function

```
def tokenize(self) -> List[Token]:
    tokens = []
    token_specification = [
        ('COMMENT',   r'\#.*'),
        ('PIPE',      r'\|\>'),
        ('STRING',    r'"[^"\n]*"'),
        ('TIME',      r'\d{2}:\d{2}'),
        ('NUMBER',    r'\d+(\.\d+)?([sx])?'),
        ('IDENT',     r'[A-Za-z_][A-Za-z0-9_]*'),
        ('NEWLINE',   r'\n'),
        ('SKIP',      r'[ \t]+'),
        ('MISMATCH',  r'.'),
    ]
    tok_regex = '|'.join(f'(?P<{tok_type}>{pattern})' for tok_type, pattern in token_specification)
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
```



### 5. Error Handling

```
elif kind == 'MISMATCH':
    raise RuntimeError(f'Unexpected character {value!r} on line {line} column {column}')
```

## Conclusions / Screenshots / Results

## Results

## References

[1] [A sample of a lexer implementation](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)

[2] [Lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis)

[3] [Formal Languages and Finite Automata, Guide for practical lessons](https://else.fcim.utm.md/pluginfile.php/110458/mod_resource/content/0/LFPC_Guide.pdf)
