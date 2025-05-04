# Topic: Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Author: Alexandru Cebotari

----

## Theory

In this lab we build on formal‐language theory to move from raw text and tokens to a hierarchical, semantic representation of program structure—an Abstract Syntax Tree (AST). We first review the role of parsing in compilation, then recall context‑free grammars (CFGs) as the basis for syntax, examine the difference between concrete parse trees and ASTs, and finally outline the recursive‑descent parsing technique used to construct an AST from a token stream.

### Syntactic Analysis (Parsing)  
Parsing—also called **syntax analysis**—is the process of analyzing a sequence of tokens to determine its grammatical structure according to the rules of a formal grammar. In compiler design it is the **second phase**, immediately following lexical analysis, which groups characters into tokens using regular expressions and finite automata. Whereas the lexer cannot enforce nested or recursive constructs (such as matching parentheses), parsing handles these context‑free patterns that lie beyond the power of regular expressions.

### Formal Grammars and Context‑Free Grammars  
A **formal grammar** is a set of production rules for generating strings in a language; in the Chomsky hierarchy, **context‑free grammars (CFGs)** occupy the level just above regular grammars and can express recursive, nested structures. A CFG is defined by the 4‑tuple (V, Σ, R, S), where:  
- V is a finite set of nonterminal symbols  
- Σ is a finite set of terminal symbols, disjoint from V  
- R is a finite set of production rules of the form A → α with A ∈ V and α ∈ (V ∪ Σ)*  
- S ∈ V is the start symbol  
CFGs thereby define the **syntax** of programming languages: they list exactly which token sequences form valid constructs.

### Parse Trees vs Abstract Syntax Trees  
When a parser applies CFG rules to tokens, it typically builds a **parse tree** (or concrete syntax tree) that shows every grammar production used. However, parse trees include every detail of the grammar—parentheses, punctuation, intermediate nonterminals—which can clutter later compiler stages. An **Abstract Syntax Tree (AST)** is a pruned, hierarchical representation that omits unneeded tokens and focuses on the essential syntactic constructs (literals, identifiers, operations). In an AST:  
- Parentheses and delimiters are implicit in tree structure, not separate nodes  
- Nodes correspond directly to language constructs (e.g. binary operations, function calls)  
- The hierarchy mirrors the nested, semantic structure of the code

### Recursive‑Descent Parsing  
One common way to build a parse tree or AST from tokens is **recursive‑descent parsing**, a top‑down method in which each nonterminal grammar rule is implemented as a (mutually) recursive function. Using a one‑token lookahead, each function matches the input tokens against its production’s right‑hand side, constructs the corresponding AST node, and returns it to its caller. This method directly mirrors the grammar in code, is easy to hand‑write for LL(1) grammars, and produces an AST suitable for subsequent semantic analysis and code generation.

## Objectives

The key objectives of this lab are to extend your Lab 3 lexer into a full syntax‑analysis pipeline that produces an Abstract Syntax Tree (AST) for a simple DSL of pipelined commands:

- **Define a `TokenType` enumeration**  
  Introduce a centralized `TokenType` enum to name and categorize every lexeme class (identifiers, literals, operators, keywords) using your existing regex‑based lexer :contentReference[oaicite:0]{index=0}.

- **Use regular expressions for token classification**  
  Leverage named‑group regular expressions to assign each scanned lexeme a `TokenType`, ensuring a single‑pass, finite‑automaton‑style lexer design :contentReference[oaicite:1]{index=1}.

- **Design AST data structures**  
  Create `@dataclass` node types—`Program`, `Pipeline`, `Command`, `Arg`—that capture the hierarchical, semantic structure of your input, omitting extraneous syntax :contentReference[oaicite:2]{index=2}.

- **Implement a recursive‑descent parser**  
  Write LL(1) parsing functions that mirror your grammar’s nonterminals (program, pipeline, command, arg), consume the token stream with one‑token lookahead, and construct the corresponding AST nodes :contentReference[oaicite:3]{index=3}.

- **Integrate lexer and parser**  
  Wire the Lab 3 lexer output into the parser input, produce a `Program` AST, and report syntax errors with informative messages (line and column) when the token sequence violates the grammar.

- **Verify AST correctness**  
  Print or pretty‑print the resulting AST to confirm that pipelines of commands and their arguments are represented with the intended nesting and ordering, laying the groundwork for later semantic analysis or code generation.

These objectives ensure you gain hands‑on experience with both lexical and syntactic analysis, understand how ASTs distill program structure, and practice building a simple compiler front‑end.
::contentReference[oaicite:4]{index=4}


## Implementation Description

Below is a list of the key functions and methods in our lexer + parser pipeline, with a brief description of each. No code is shown here—you will drop in your existing implementations under each heading.

### Lexer

- **`Lexer.__init__(self, text)`**  
  Initializes a new lexer instance with the input text to be tokenized.

- **`Lexer.tokenize(self)`**  
  Scans the entire input string using the combined regex (one pass), classifies each lexeme into a token (including keywords, identifiers, literals, operators), tracks line/column positions, and returns the complete list of `Token` objects (ending with an EOF token).

### TokenType and Keyword Setup

- **`TokenType` enum**  
  Defines every possible token category (COMMENT, PIPE, STRING, TIME, NUMBER, IDENT, EOF, and each keyword) so that both lexer and parser share a single source of truth for token kinds.

- **`KEYWORD_TYPES` set**  
  A pre‑computed set of `TokenType` values corresponding to all DSL keywords, used by the parser to recognize command names.

### Parser

- **`Parser.__init__(self, tokens)`**  
  Converts raw token objects (with string‑typed kinds) into tokens whose `.type` is a `TokenType`, initializes the token list, position index, and current lookahead token.

- **`Parser.advance(self)`**  
  Moves the one‑token lookahead forward by incrementing the position and updating `self.current_token`.

- **`Parser.expect(self, ttype)`**  
  Verifies that the current lookahead has the expected `TokenType`; if so, consumes it (advances) and returns it; otherwise raises a `SyntaxError` with line/column info.

- **`Parser.parse(self)`**  
  Entry point for syntax analysis: repeatedly calls `parse_pipeline` until EOF is reached, collecting each resulting `Pipeline` node into a top‑level `Program` AST node.

- **`Parser.parse_pipeline(self)`**  
  Implements the grammar rule for a pipeline: parses the first command, then—while the lookahead is a PIPE token—consumes the PIPE and parses the next command, returning a `Pipeline` node containing the ordered list of `Command` nodes.

- **`Parser.parse_command(self)`**  
  Implements the grammar rule for a command: checks that the next token is either an identifier or one of the keyword token types, consumes it as the command name, then repeatedly collects all following argument tokens (STRING, TIME, NUMBER, IDENT) into `Arg` nodes, returning a `Command` AST node.

### AST Node “pretty” Methods

- **`Program.pretty(self)`**  
  Produces a multi‑line, indented string representation of the entire AST, starting from the list of pipelines.

- **`Pipeline.pretty(self, indent)`**  
  Produces an indented, multi‑line string for a single pipeline and its commands.

- **`Command.pretty(self, indent)`**  
  Produces an indented, multi‑line string for a single command and its arguments.

## Conclusions / Screenshots / Results

This project successfully implemented a lexer and parser for a domain-specific language designed around video and audio editing operations. Through clearly structured components—tokenization, parsing, and AST representation—the system translates high-level DSL commands into a structured and analyzable format.

The **lexer** effectively classifies tokens using a concise regex specification, while also recognizing keywords and preserving contextual information like line and column numbers. This forms a solid foundation for detailed parsing and error reporting.

The **parser** interprets the token stream into a well-defined abstract syntax tree (AST), organized into `Program`, `Pipeline`, and `Command` nodes. This layered structure enables modular processing of complex command chains and supports readable output through built-in `pretty()` methods.

Overall, this implementation demonstrates the power of separating lexical and syntactic concerns when building interpreters. The architecture is extensible—new commands or argument types can be added with minimal disruption. It also lays the groundwork for future features like semantic analysis, execution backends, or static verification of pipeline structures.

In conclusion, this project provided a clean and maintainable framework for parsing a structured DSL, with careful attention to correctness, clarity, and future extensibility.


Console Output:
```
Program(pipelines=[
  Pipeline(commands=[
    Command(name='open', args=[
        Arg(type=TokenType.IDENT, value='vid1'),
        Arg(type=TokenType.STRING, value='"file.mp4"'),
    ])
    Command(name='trim', args=[
        Arg(type=TokenType.NUMBER, value='5s'),
    ])
    Command(name='save', args=[
        Arg(type=TokenType.STRING, value='"out.mp4"'),
    ])
  ])
])
```

## References

[1] [A sample of a lexer implementation](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)

[2] [Lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis)

[3] [Formal Languages and Finite Automata, Guide for practical lessons](https://else.fcim.utm.md/pluginfile.php/110458/mod_resource/content/0/LFPC_Guide.pdf)
