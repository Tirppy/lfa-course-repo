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

## Implementation description

In this section, we describe the implementation of the video processing DSL lexer and explain each part of the code separately.
The implementation is divided into several components: the definition of tokens, the reserved keywords set, the Lexer class initialization, the tokenize method which is the core of the lexer, and the testing section that demonstrates the lexer's functionality.

### Token Dataclass

The Token dataclass is defined to store information about each token generated by the lexer. The code for this part is written in plain text as follows:

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

This segment creates a simple data structure with four attributes: type, value, line, and column. The 'type' attribute holds the classification of the token, 'value' stores the exact lexeme, while 'line' and 'column' provide the positional information of the token within the source text. This structure is fundamental for later stages like error reporting and further syntactic analysis.

### Reserved Keywords Definition

The code defines a set of reserved keywords for the DSL that the lexer uses to differentiate identifiers from keywords. The snippet is as follows:

```
KEYWORDS = {
    'open', 'fade', 'trim', 'save', 'show', 'as', 'delay', 'volume', 'mix',
    'split', 'loop', 'join', 'overlay', 'overlayAudio', 'export', 'format',
    'resolution', 'bitrate', 'extract', 'cut', 'insert', 'rotate', 'blank',
    'overwrite', 'operlap'
}
```

This block initializes a Python set containing all reserved words for the video processing language. When the lexer identifies an identifier token, it checks if the token's value is in this set and, if it is, converts the token type to the uppercase version of the keyword. This mechanism ensures that reserved words are properly recognized and handled by the lexer.

### Lexer Class Initialization

The Lexer class encapsulates the lexing functionality. Its initialization method is designed to take the input text and store it for processing. The corresponding code is as follows:

```
class Lexer:
    def __init__(self, text: str):
        self.text = text
```

This constructor accepts a single argument, which is the text to be analyzed, and assigns it to an instance variable. This design allows the lexing functions to operate on the input text throughout the lifetime of the Lexer object, facilitating a clean and modular implementation.

### Tokenize Method

The tokenize method is the core of the lexer. It processes the input text and generates a list of tokens based on predefined regular expression patterns. The code for this method is as follows:

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

This method begins by initializing an empty list to store the tokens and defining a list of token specifications, where each specification pairs a token type with a corresponding regular expression pattern. The token specifications include patterns for comments, pipeline operators, string literals, time formats, numbers, identifiers, newlines, whitespace, and a fallback for any mismatches. A master regular expression is built by joining these patterns together. The method then uses the compiled regular expression to match tokens sequentially in the input text. As each token is identified, special cases are handled: newlines increment the line counter, whitespace is skipped, and identifiers are checked against the reserved keywords set. If an unexpected character is encountered, an error is raised. Finally, the method returns the complete list of tokens generated from the input text.

### Testing the Lexer

The final part of the code is a test harness that demonstrates the lexer's functionality. The code is as follows:

```
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
```

This section of the code provides a concrete example of how the lexer works. It defines a multiline string containing sample DSL code, creates an instance of the Lexer class with this code, and calls the tokenize method to generate the token stream. The resulting tokens are then printed to the console, allowing for verification of the lexer's correct operation. This test harness is crucial for ensuring that the lexer accurately processes and tokenizes the video processing DSL input.


## Conclusions / Screenshots / Results

The implementation of the lexer for the video processing DSL has proven to be effective and robust.
Through this project, we successfully developed a system that converts a raw input script into a well-structured stream of tokens, accurately categorizing keywords, identifiers, string literals, numbers, and various operators.
The lexer also preserves comments and tracks the position of each token, which is essential for debugging and further stages of language processing.

The results demonstrate that our lexer can handle complex input that includes multimedia commands and chained operations, as seen in our sample video processing DSL code.
The detailed token information, such as token types and their respective positions, confirms that the lexical analysis is performed correctly and that the foundational components are in place for building a full compiler or interpreter for the DSL.

Screenshots of the console output are provided below to illustrate the successful tokenization process.
These images capture the tokens as they are printed, validating that each element of the input script is correctly identified and processed.
At the end of this section, the actual output from the console will be appended to provide clear evidence of the lexer's performance and to facilitate further analysis.

![image](https://github.com/user-attachments/assets/e2d35b33-1c83-4bca-a18a-9cc373b8ccae)

Console Output:

```
Token(type='COMMENT', value='# creates file2 string', line=2, column=1)
Token(type='IDENT', value='file2', line=3, column=1)
Token(type='STRING', value='"C:\\Downloads\\New video1.mp4"', line=3, column=7)
Token(type='COMMENT', value='# creates vid2', line=5, column=1)
Token(type='OPEN', value='open', line=6, column=1)
Token(type='IDENT', value='vid2', line=6, column=6)
Token(type='IDENT', value='file2', line=6, column=11)
Token(type='COMMENT', value='# creates vid1, edit and save', line=8, column=1)
Token(type='OPEN', value='open', line=9, column=1)
Token(type='IDENT', value='vid1', line=9, column=6)
Token(type='STRING', value='"C:\\Downloads\\Video.mp4"', line=9, column=11)
Token(type='PIPE', value='|>', line=9, column=36)
Token(type='BLANK', value='blank', line=9, column=39)
Token(type='PIPE', value='|>', line=9, column=45)
Token(type='SAVE', value='save', line=9, column=48)
Token(type='STRING', value='".../../audio.mp3"', line=9, column=53)
Token(type='PIPE', value='|>', line=9, column=72)
Token(type='SHOW', value='show', line=9, column=75)
Token(type='PIPE', value='|>', line=9, column=80)
Token(type='AS', value='as', line=9, column=83)
Token(type='IDENT', value='audio1', line=9, column=86)
Token(type='COMMENT', value='# work with vid1 , save and download results', line=11, column=1)
Token(type='IDENT', value='vid1', line=12, column=1)
Token(type='PIPE', value='|>', line=12, column=6)
Token(type='TRIM', value='trim', line=12, column=9)
Token(type='NUMBER', value='5s', line=12, column=14)
Token(type='PIPE', value='|>', line=12, column=17)
Token(type='AS', value='as', line=12, column=20)
Token(type='IDENT', value='vid1', line=12, column=23)
Token(type='PIPE', value='|>', line=12, column=28)
Token(type='OVERWRITE', value='overwrite', line=12, column=31)
Token(type='IDENT', value='audio1', line=12, column=41)
Token(type='TIME', value='00:05', line=12, column=48)
Token(type='NUMBER', value='10s', line=12, column=54)
Token(type='PIPE', value='|>', line=12, column=58)
Token(type='OPERLAP', value='operlap', line=12, column=61)
Token(type='IDENT', value='vid2', line=12, column=69)
Token(type='TIME', value='01:00', line=12, column=74)
Token(type='PIPE', value='|>', line=12, column=80)
Token(type='SHOW', value='show', line=12, column=83)
Token(type='PIPE', value='|>', line=12, column=88)
Token(type='AS', value='as', line=12, column=91)
Token(type='IDENT', value='vid6', line=12, column=94)
Token(type='PIPE', value='|>', line=12, column=99)
Token(type='SAVE', value='save', line=12, column=102)
Token(type='STRING', value='".../../changed.mp4"', line=12, column=107)
```

## Results

The lexer's output from processing the provided DSL input confirmed that all components of the lexer functioned correctly.
The tokens were accurately identified and classified, with each token corresponding to specific elements of the video processing language.
Reserved keywords such as OPEN, TRIM, SHOW, and AS were successfully recognized and differentiated from identifiers, while string literals representing file paths, numeric values for times and durations, and the pipeline operator were all correctly tokenized.
Additionally, comments were preserved and included in the token stream, which is useful for debugging and future processing.

A detailed inspection of the output showed that the lexer maintained accurate tracking of line and column numbers, ensuring precise error localization if needed.
The token stream reflected the intended structure of the input DSL code, demonstrating that the regular expression patterns and state management within the lexer are robust and reliable.
Overall, these results indicate that the lexer meets the lab requirements and establishes a strong foundation for further development of a full compiler or interpreter for the video processing DSL.

## References

[1] [A sample of a lexer implementation](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)

[2] [Lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis)

[3] [Formal Languages and Finite Automata, Guide for practical lessons](https://else.fcim.utm.md/pluginfile.php/110458/mod_resource/content/0/LFPC_Guide.pdf)
