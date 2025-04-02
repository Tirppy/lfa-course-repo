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

class RegexParser:
    def __init__(self, pattern):
        self.pattern = pattern
        self.index = 0

    def parse(self):
        tokens = self.parse_sequence()
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

    def parse_literal(self):
        start = self.index
        while self.index < len(self.pattern) and self.pattern[self.index] not in "^( )|":
            self.index += 1
        literal = self.pattern[start:self.index]
        return Token("literal", literal)

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
