### Course: Formal Languages & Finite Automata
### Author: Alexandru Cebotari

----

## Theory

Regular expressions, commonly known as regexes, are formal patterns used to describe and match sequences of characters within strings. They originate from formal language theory and play a vital role in computer science, particularly in text processing and data validation.

### Foundations in Formal Language Theory

- **Regular Languages:**  
  Regexes represent regular languages, which are defined by the simplest class of automata—finite automata. This theoretical basis ensures that patterns described by regexes can be processed efficiently.

- **Finite Automata:**  
  Regular expressions can be transformed into finite automata (either deterministic or nondeterministic), which are used to determine if a string belongs to the language defined by the regex.

### Core Components of Regular Expressions

- **Literal Characters:**  
  These are the basic elements that represent themselves (e.g., `A`, `B`, `1`).

- **Character Classes:**  
  Sets of characters defined within brackets (e.g., `[abc]`) match any single character within the set.

- **Repetition Quantifiers:**  
  Symbols that specify the number of times a character or group should repeat:
  - `*` matches zero or more occurrences.
  - `+` matches one or more occurrences.
  - `?` matches zero or one occurrence.

- **Grouping and Alternation:**  
  - Parentheses `()` are used for grouping parts of a regex.
  - The vertical bar `|` is used for alternation, allowing a match for any one of the separated options (e.g., `(S|T)` matches either `S` or `T`).

### Applications and Uses

Regular expressions are widely employed in various fields:
- **Text Searching and Processing:**  
  Tools such as `grep`, `sed`, and many text editors use regexes to search and manipulate text efficiently.
  
- **Input Validation:**  
  Regexes help validate the format of inputs like email addresses, phone numbers, and other standardized data.
  
- **Data Extraction:**  
  They are used to extract meaningful information from logs, structured text, and large datasets.
  
- **Lexical Analysis:**  
  Compilers use regex-based techniques to tokenize source code during the parsing phase.

### Relevance to Implementation

In our project, we leverage these theoretical principles to build a dynamic string generator based on regexes. The implementation involves:
- **Parsing:** Breaking down a custom regex into tokens (literals and groups) with associated repetition rules.
- **Generation:** Using these tokens to generate valid strings that conform to the defined patterns, demonstrating practical application of regular expressions.

## Objectives

The goal of this project is to develop a program that dynamically interprets and generates valid strings based on a given set of complex regular expressions. The key objectives are:

- **Dynamic Regex Interpretation:** Implement a system that processes regular expressions without hardcoding specific patterns, ensuring flexibility in string generation.
- **Valid String Generation:** Generate valid symbol combinations conforming to the provided regex patterns.
- **Handling Repetition Constraints:** Limit indefinite repetitions to a maximum of 5 occurrences to prevent excessively long outputs.
- **Processing Sequence Visualization (Bonus):** Implement a function that traces the sequence of processing steps involved in parsing and generating a string from a regex.

This ensures that the program can correctly analyze, interpret, and construct valid outputs from various regex structures while maintaining readability and efficiency.

## Implementation description

### Token Class and Constants

```
import random

DEFAULT_MIN = 1
DEFAULT_MAX = 5
ZERO_MIN = 0

class Token:
    def __init__(self, kind, value, repeat=(1, 1)):
        self.kind = kind      
        self.value = value    
        self.repeat = repeat  

    def __repr__(self):
        return f"Token({self.kind!r}, {self.value!r}, repeat={self.repeat})"
```

The implementation starts by defining some constants to manage repetition limits: `DEFAULT_MIN`, `DEFAULT_MAX`, and `ZERO_MIN`, which help constrain the number of times characters can repeat.
Then, the `Token` class is created, which represents individual components of a regular expression.
A token can be a literal character or a grouped sequence of choices. It also stores repetition constraints, allowing dynamic generation of valid strings.

### RegexParser Class

```
class RegexParser:
    def __init__(self, pattern):
        self.pattern = pattern
        self.index = 0

    def parse(self):
        tokens = self.parse_sequence()
        return tokens
```

The `RegexParser` class is responsible for parsing the given regular expression into a structured format.
It takes a regex pattern as input and initializes an index to track parsing progress.
The main `parse()` method calls `parse_sequence()`, which iterates through the pattern, recognizing and extracting tokens until it reaches the end or encounters a closing parenthesis.

### Token Parsing Methods

```
def parse_sequence(self):
    tokens = []
    while self.index < len(self.pattern):
        if self.pattern[self.index] == ')':
            break
        token = self.parse_token()
        if token:
            tokens.append(token)
    return tokens

def parse_token(self):
    char = self.pattern[self.index]
    if char == '(':
        token = self.parse_group()
    else:
        token = self.parse_literal()

    if self.index < len(self.pattern) and self.pattern[self.index] == '^':
        self.index += 1  
        rep_min, rep_max = self.parse_repetition()
        token.repeat = (rep_min, rep_max)
    return token
```

The `parse_token()` method determines whether the current part of the regex is a literal character or a grouped expression.
If it detects a group (enclosed in parentheses), it calls `parse_group()`, which handles alternative choices inside `( )`.
When encountering a repetition indicator (`^`), it moves to `parse_repetition()`, which extracts the specified repetition constraints.
The `parse_literal()` method processes simple character sequences.

### Group Handling and Alternatives

```
def parse_group(self):
    self.index += 1  
    alternatives = []
    current_tokens = []
    while self.index < len(self.pattern):
        if self.pattern[self.index] == ')':
            self.index += 1
            break
        elif self.pattern[self.index] == '|':
            self.index += 1
            alternatives.append(current_tokens)
            current_tokens = []
        else:
            token = self.parse_token()
            current_tokens.append(token)
    alternatives.append(current_tokens)
    return Token("group", alternatives)
```

When parsing groups, the `parse_group()` method scans through the expression, collecting alternatives separated by `|`.
Each alternative is stored as a sequence of tokens, allowing the program to later randomly select one during string generation.

### Handling Repetition Constraints

```
def parse_repetition(self):
    if self.pattern[self.index] != '(':
        raise ValueError("Expected '(' after '^'")
    self.index += 1  
    rep_str = ""
    while self.index < len(self.pattern) and self.pattern[self.index] != ')':
        rep_str += self.pattern[self.index]
        self.index += 1
    if self.index >= len(self.pattern):
        raise ValueError("Unclosed repetition parenthesis")
    self.index += 1  
    rep_str = rep_str.strip()
    if rep_str.isdigit():
        n = int(rep_str)
        return (n, n)
    elif rep_str == "*":
        return (ZERO_MIN, DEFAULT_MAX)
    elif rep_str == "+":
        return (DEFAULT_MIN, DEFAULT_MAX)
    elif rep_str == "":
        return (DEFAULT_MIN, DEFAULT_MAX)
    else:
        raise ValueError(f"Unknown repetition specifier: {rep_str}")
```

The `parse_repetition()` method is responsible for interpreting repetition constraints within the regex pattern.
For example, the `^*` operator indicates that the preceding token can repeat zero or more times, while `^+` means it can repeat one or more times.
The method processes these repetition operators and converts them into a range of possible repetitions, which are then stored in the token.
These constraints help control how many times a particular token or group can appear in the final generated string.

### Displaying Tokens

```
def display_token(token):
    """Return a simplified string representation of a token."""
    if token.kind == "literal":
        return f"'{token.value}'"
    elif token.kind == "group":
        alternatives = []
        for alt in token.value:
            alt_str = ''.join(display_token(t) for t in alt)
            alternatives.append(alt_str)
        return f"({'|'.join(alternatives)})"
    else:
        return "UnknownToken"
```

The `display_token()` function converts tokens into a readable format, showing literals as they are and groups as their possible choices.
This function is useful for debugging and tracing how the regular expression is being processed.

### Random String Generation

```
def generate_random_from_tokens(tokens, trace):
    result = []
    for token in tokens:
        result.append(generate_random_from_token(token, trace))
    return ''.join(result)

def generate_random_from_token(token, trace):
    token_str = display_token(token)
    trace.append(f"Processing token: {token_str}")
    
    if token.kind == "literal":
        base = token.value
    elif token.kind == "group":
        alt_index = random.randrange(len(token.value))
        base = generate_random_from_tokens(token.value[alt_index], trace)
        trace.append(f"Group token: Chose alternative {alt_index + 1} of {len(token.value)}")
    else:
        raise ValueError("Unknown token type.")
    
    rep_min, rep_max = token.repeat
    count = random.randint(rep_min, rep_max)
    trace.append(f"Repeating {token_str} {count} time(s) (range {rep_min}-{rep_max})")
    return base * count
```

To generate random strings based on the parsed tokens, the `generate_random_from_tokens()` function iterates through the list of tokens and constructs a string.
Each token is processed using `generate_random_from_token()`, which randomly selects group alternatives and determines how many times to repeat a token within its allowed range.

### Execution and Output

```
if __name__ == "__main__":
    regexes = [
        "(S|T)(U|V)W^()Y^(+)24",
        "L(M|N)O^(3)P^()Q(2|3)",
        "R^(*)S(T|U|V)W(X|Y|Z)^(2)"
    ]

    for i, regex in enumerate(regexes, 1):
        print(f"\n--- Regex {i}: {regex} ---")
        parser = RegexParser(regex)
        tokens = parser.parse()
        
        for j in range(1, 6):
            trace = []  
            rand_string = generate_random_from_tokens(tokens, trace)
            print(f"\nRandom String {j}: {rand_string}")
            print("Trace:")
            for step in trace:
                print("  -", step)
            print("-" * 40)
```

The program defines three complex regular expressions, processes them using the `RegexParser`, and generates five random valid strings for each regex.
A trace of processing steps is printed, showing which parts of the regex were interpreted and how they contributed to the final output.
This provides insight into the dynamic generation process while ensuring that the generated strings adhere to the given patterns.


## Conclusions / Screenshots / Results

In this implementation, we successfully demonstrated how to dynamically interpret and generate valid strings from complex regular expressions.
The use of the `RegexParser` class allowed for the systematic breakdown of the regex patterns into individual components (tokens), which could be easily manipulated to produce random combinations.
By handling various elements such as literals, groups, alternatives, and repetition operators, the program was able to generate strings that followed the given regular expression rules.

The handling of repetition constraints, such as `*`, `+`, and specific numerical limits, ensured that the generated strings were realistic and not overly long, which addressed the issue of infinite or excessively large outputs.
Moreover, the trace functionality added transparency to the string generation process, enabling us to follow how each part of the regex was processed and used to form the final string.

This approach proved to be a flexible and scalable way to generate valid strings based on arbitrary regular expression patterns, making it useful for testing, data generation, or even educational purposes.
Future improvements could focus on optimizing the parser's performance or extending the program to handle more advanced regex features.

In conclusion, this project demonstrated the ability to dynamically interpret regular expressions and generate strings accordingly, while adhering to the constraints and ensuring the process was both transparent and manageable.

Console Output:

```
--- Regex 1: (S|T)(U|V)W^()Y^(+)24 ---

Random String 1: TVWWWWYYY24
Trace:
  - Processing token: ('S'|'T')
  - Processing token: 'T'
  - Repeating 'T' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 2
  - Repeating ('S'|'T') 1 time(s) (range 1-1)
  - Processing token: ('U'|'V')
  - Processing token: 'V'
  - Repeating 'V' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 2
  - Repeating ('U'|'V') 1 time(s) (range 1-1)
  - Processing token: 'W'
  - Repeating 'W' 4 time(s) (range 1-5)
  - Processing token: 'Y'
  - Repeating 'Y' 3 time(s) (range 1-5)
  - Processing token: '24'
  - Repeating '24' 1 time(s) (range 1-1)
----------------------------------------

Random String 2: SUWWWWY24
Trace:
  - Processing token: ('S'|'T')
  - Processing token: 'S'
  - Repeating 'S' 1 time(s) (range 1-1)
  - Group token: Chose alternative 1 of 2
  - Repeating ('S'|'T') 1 time(s) (range 1-1)
  - Processing token: ('U'|'V')
  - Processing token: 'U'
  - Repeating 'U' 1 time(s) (range 1-1)
  - Group token: Chose alternative 1 of 2
  - Repeating ('U'|'V') 1 time(s) (range 1-1)
  - Processing token: 'W'
  - Repeating 'W' 4 time(s) (range 1-5)
  - Processing token: 'Y'
  - Repeating 'Y' 1 time(s) (range 1-5)
  - Processing token: '24'
  - Repeating '24' 1 time(s) (range 1-1)
----------------------------------------

Random String 3: TVWWWWYY24
Trace:
  - Processing token: ('S'|'T')
  - Processing token: 'T'
  - Repeating 'T' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 2
  - Repeating ('S'|'T') 1 time(s) (range 1-1)
  - Processing token: ('U'|'V')
  - Processing token: 'V'
  - Repeating 'V' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 2
  - Repeating ('U'|'V') 1 time(s) (range 1-1)
  - Processing token: 'W'
  - Repeating 'W' 4 time(s) (range 1-5)
  - Processing token: 'Y'
  - Repeating 'Y' 2 time(s) (range 1-5)
  - Processing token: '24'
  - Repeating '24' 1 time(s) (range 1-1)
----------------------------------------

Random String 4: TVWWWWY24
Trace:
  - Processing token: ('S'|'T')
  - Processing token: 'T'
  - Repeating 'T' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 2
  - Repeating ('S'|'T') 1 time(s) (range 1-1)
  - Processing token: ('U'|'V')
  - Processing token: 'V'
  - Repeating 'V' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 2
  - Repeating ('U'|'V') 1 time(s) (range 1-1)
  - Processing token: 'W'
  - Repeating 'W' 4 time(s) (range 1-5)
  - Processing token: 'Y'
  - Repeating 'Y' 1 time(s) (range 1-5)
  - Processing token: '24'
  - Repeating '24' 1 time(s) (range 1-1)
----------------------------------------

Random String 5: TVWWWWYY24
Trace:
  - Processing token: ('S'|'T')
  - Processing token: 'T'
  - Repeating 'T' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 2
  - Repeating ('S'|'T') 1 time(s) (range 1-1)
  - Processing token: ('U'|'V')
  - Processing token: 'V'
  - Repeating 'V' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 2
  - Repeating ('U'|'V') 1 time(s) (range 1-1)
  - Processing token: 'W'
  - Repeating 'W' 4 time(s) (range 1-5)
  - Processing token: 'Y'
  - Repeating 'Y' 2 time(s) (range 1-5)
  - Processing token: '24'
  - Repeating '24' 1 time(s) (range 1-1)
----------------------------------------

--- Regex 2: L(M|N)O^(3)P^()Q(2|3) ---

Random String 1: LNOOOPPQ3
Trace:
  - Processing token: 'L'
  - Repeating 'L' 1 time(s) (range 1-1)
  - Processing token: ('M'|'N')
  - Processing token: 'N'
  - Repeating 'N' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 2
  - Repeating ('M'|'N') 1 time(s) (range 1-1)
  - Processing token: 'O'
  - Repeating 'O' 3 time(s) (range 3-3)
  - Processing token: 'P'
  - Repeating 'P' 2 time(s) (range 1-5)
  - Processing token: 'Q'
  - Repeating 'Q' 1 time(s) (range 1-1)
  - Processing token: ('2'|'3')
  - Processing token: '3'
  - Repeating '3' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 2
  - Repeating ('2'|'3') 1 time(s) (range 1-1)
----------------------------------------

Random String 2: LMOOOPPQ3
Trace:
  - Processing token: 'L'
  - Repeating 'L' 1 time(s) (range 1-1)
  - Processing token: ('M'|'N')
  - Processing token: 'M'
  - Repeating 'M' 1 time(s) (range 1-1)
  - Group token: Chose alternative 1 of 2
  - Repeating ('M'|'N') 1 time(s) (range 1-1)
  - Processing token: 'O'
  - Repeating 'O' 3 time(s) (range 3-3)
  - Processing token: 'P'
  - Repeating 'P' 2 time(s) (range 1-5)
  - Processing token: 'Q'
  - Repeating 'Q' 1 time(s) (range 1-1)
  - Processing token: ('2'|'3')
  - Processing token: '3'
  - Repeating '3' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 2
  - Repeating ('2'|'3') 1 time(s) (range 1-1)
----------------------------------------

Random String 3: LMOOOPPPPPQ3
Trace:
  - Processing token: 'L'
  - Repeating 'L' 1 time(s) (range 1-1)
  - Processing token: ('M'|'N')
  - Processing token: 'M'
  - Repeating 'M' 1 time(s) (range 1-1)
  - Group token: Chose alternative 1 of 2
  - Repeating ('M'|'N') 1 time(s) (range 1-1)
  - Processing token: 'O'
  - Repeating 'O' 3 time(s) (range 3-3)
  - Processing token: 'P'
  - Repeating 'P' 5 time(s) (range 1-5)
  - Processing token: 'Q'
  - Repeating 'Q' 1 time(s) (range 1-1)
  - Processing token: ('2'|'3')
  - Processing token: '3'
  - Repeating '3' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 2
  - Repeating ('2'|'3') 1 time(s) (range 1-1)
----------------------------------------

Random String 4: LMOOOPPPPQ2
Trace:
  - Processing token: 'L'
  - Repeating 'L' 1 time(s) (range 1-1)
  - Processing token: ('M'|'N')
  - Processing token: 'M'
  - Repeating 'M' 1 time(s) (range 1-1)
  - Group token: Chose alternative 1 of 2
  - Repeating ('M'|'N') 1 time(s) (range 1-1)
  - Processing token: 'O'
  - Repeating 'O' 3 time(s) (range 3-3)
  - Processing token: 'P'
  - Repeating 'P' 4 time(s) (range 1-5)
  - Processing token: 'Q'
  - Repeating 'Q' 1 time(s) (range 1-1)
  - Processing token: ('2'|'3')
  - Processing token: '2'
  - Repeating '2' 1 time(s) (range 1-1)
  - Group token: Chose alternative 1 of 2
  - Repeating ('2'|'3') 1 time(s) (range 1-1)
----------------------------------------

Random String 5: LNOOOPPPPQ2
Trace:
  - Processing token: 'L'
  - Repeating 'L' 1 time(s) (range 1-1)
  - Processing token: ('M'|'N')
  - Processing token: 'N'
  - Repeating 'N' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 2
  - Repeating ('M'|'N') 1 time(s) (range 1-1)
  - Processing token: 'O'
  - Repeating 'O' 3 time(s) (range 3-3)
  - Processing token: 'P'
  - Repeating 'P' 4 time(s) (range 1-5)
  - Processing token: 'Q'
  - Repeating 'Q' 1 time(s) (range 1-1)
  - Processing token: ('2'|'3')
  - Processing token: '2'
  - Repeating '2' 1 time(s) (range 1-1)
  - Group token: Chose alternative 1 of 2
  - Repeating ('2'|'3') 1 time(s) (range 1-1)
----------------------------------------

--- Regex 3: R^(*)S(T|U|V)W(X|Y|Z)^(2) ---

Random String 1: RSTWYY
Trace:
  - Processing token: 'R'
  - Repeating 'R' 1 time(s) (range 0-5)
  - Processing token: 'S'
  - Repeating 'S' 1 time(s) (range 1-1)
  - Processing token: ('T'|'U'|'V')
  - Processing token: 'T'
  - Repeating 'T' 1 time(s) (range 1-1)
  - Group token: Chose alternative 1 of 3
  - Repeating ('T'|'U'|'V') 1 time(s) (range 1-1)
  - Processing token: 'W'
  - Repeating 'W' 1 time(s) (range 1-1)
  - Processing token: ('X'|'Y'|'Z')
  - Processing token: 'Y'
  - Repeating 'Y' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 3
  - Repeating ('X'|'Y'|'Z') 2 time(s) (range 2-2)
----------------------------------------

Random String 2: RRRRRSUWYY
Trace:
  - Processing token: 'R'
  - Repeating 'R' 5 time(s) (range 0-5)
  - Processing token: 'S'
  - Repeating 'S' 1 time(s) (range 1-1)
  - Processing token: ('T'|'U'|'V')
  - Processing token: 'U'
  - Repeating 'U' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 3
  - Repeating ('T'|'U'|'V') 1 time(s) (range 1-1)
  - Processing token: 'W'
  - Repeating 'W' 1 time(s) (range 1-1)
  - Processing token: ('X'|'Y'|'Z')
  - Processing token: 'Y'
  - Repeating 'Y' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 3
  - Repeating ('X'|'Y'|'Z') 2 time(s) (range 2-2)
----------------------------------------

Random String 3: RRSTWXX
Trace:
  - Processing token: 'R'
  - Repeating 'R' 2 time(s) (range 0-5)
  - Processing token: 'S'
  - Repeating 'S' 1 time(s) (range 1-1)
  - Processing token: ('T'|'U'|'V')
  - Processing token: 'T'
  - Repeating 'T' 1 time(s) (range 1-1)
  - Group token: Chose alternative 1 of 3
  - Repeating ('T'|'U'|'V') 1 time(s) (range 1-1)
  - Processing token: 'W'
  - Repeating 'W' 1 time(s) (range 1-1)
  - Processing token: ('X'|'Y'|'Z')
  - Processing token: 'X'
  - Repeating 'X' 1 time(s) (range 1-1)
  - Group token: Chose alternative 1 of 3
  - Repeating ('X'|'Y'|'Z') 2 time(s) (range 2-2)
----------------------------------------

Random String 4: RRRSUWZZ
Trace:
  - Processing token: 'R'
  - Repeating 'R' 3 time(s) (range 0-5)
  - Processing token: 'S'
  - Repeating 'S' 1 time(s) (range 1-1)
  - Processing token: ('T'|'U'|'V')
  - Processing token: 'U'
  - Repeating 'U' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 3
  - Repeating ('T'|'U'|'V') 1 time(s) (range 1-1)
  - Processing token: 'W'
  - Repeating 'W' 1 time(s) (range 1-1)
  - Processing token: ('X'|'Y'|'Z')
  - Processing token: 'Z'
  - Repeating 'Z' 1 time(s) (range 1-1)
  - Group token: Chose alternative 3 of 3
  - Repeating ('X'|'Y'|'Z') 2 time(s) (range 2-2)
----------------------------------------

Random String 5: RSUWZZ
Trace:
  - Processing token: 'R'
  - Repeating 'R' 1 time(s) (range 0-5)
  - Processing token: 'S'
  - Repeating 'S' 1 time(s) (range 1-1)
  - Processing token: ('T'|'U'|'V')
  - Processing token: 'U'
  - Repeating 'U' 1 time(s) (range 1-1)
  - Group token: Chose alternative 2 of 3
  - Repeating ('T'|'U'|'V') 1 time(s) (range 1-1)
  - Processing token: 'W'
  - Repeating 'W' 1 time(s) (range 1-1)
  - Processing token: ('X'|'Y'|'Z')
  - Processing token: 'Z'
  - Repeating 'Z' 1 time(s) (range 1-1)
  - Group token: Chose alternative 3 of 3
  - Repeating ('X'|'Y'|'Z') 2 time(s) (range 2-2)
----------------------------------------
```

## References

[1] [A sample of a lexer implementation](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)

[2] [Lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis)

[3] [Formal Languages and Finite Automata, Guide for practical lessons](https://else.fcim.utm.md/pluginfile.php/110458/mod_resource/content/0/LFPC_Guide.pdf)
