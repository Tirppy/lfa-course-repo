import itertools

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

class RegexParser:
    def __init__(self, pattern):
        self.pattern = pattern
        self.index = 0
        self.steps = []  

    def log(self, message):
        self.steps.append(message)

    def parse(self):
        self.log("Start parsing the regex.")
        tokens = self.parse_sequence()
        self.log("Finished parsing the regex.")
        return tokens

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
        self.log(f"Parsing token at index {self.index}: {self.pattern[self.index:]}")
        char = self.pattern[self.index]
        token = None

        if char == '(':
            
            token = self.parse_group()
        else:
            
            token = self.parse_literal()

        if self.index < len(self.pattern) and self.pattern[self.index] == '^':
            self.index += 1  
            rep_min, rep_max = self.parse_repetition()
            token.repeat = (rep_min, rep_max)
            self.log(f"Applied repetition {token.repeat} to token {token}")
        return token

    def parse_literal(self):
        start = self.index
        while self.index < len(self.pattern) and self.pattern[self.index] not in "^( )|":
            self.index += 1
        literal = self.pattern[start:self.index]
        self.log(f"Parsed literal: {literal}")
        return Token("literal", literal)

    def parse_group(self):
        self.index += 1
        self.log("Parsing group starting at index " + str(self.index))
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
        self.log(f"Parsed group with alternatives: {alternatives}")
        return Token("group", alternatives)

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
        self.log(f"Parsed repetition specifier: '{rep_str}'")
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

def generate_from_tokens(tokens):
    possibilities = []
    for token in tokens:
        poss = generate_from_token(token)
        possibilities.append(poss)
    return [''.join(prod) for prod in itertools.product(*possibilities)]

def generate_from_token(token):
    base_strings = []
    if token.kind == "literal":
        base_strings = [token.value]
    elif token.kind == "group":
        for alt in token.value:
            gen = generate_from_tokens(alt)
            base_strings.extend(gen)
    else:
        raise ValueError("Unknown token type.")

    
    rep_min, rep_max = token.repeat
    results = []
    for count in range(rep_min, rep_max + 1):
        if count == 0:
            results.append("")  
        else:
            for s in base_strings:
                results.append(s * count)
    return results

def generate_from_regex(regex):
    parser = RegexParser(regex)
    tokens = parser.parse()
    all_strings = generate_from_tokens(tokens)
    return all_strings, parser.steps

def explain_processing(regex):
    parser = RegexParser(regex)
    _ = parser.parse()  
    return "\n".join(parser.steps)

if __name__ == "__main__":
    regexes = [
        "(S|T)(U|V)W^()Y^(+)24",
        "L(M|N)O^(3)P^()Q(2|3)",
        "R^(*)S(T|U|V)W(X|Y|Z)^(2)"
    ]

    for i, regex in enumerate(regexes, 1):
        print(f"\n--- Regex {i}: {regex} ---")
        all_valid, processing_steps = generate_from_regex(regex)
        print(f"Total combinations generated: {len(all_valid)}")
        print("Examples:", all_valid[:10])
        print("\nProcessing Trace:")
        print(explain_processing(regex))
