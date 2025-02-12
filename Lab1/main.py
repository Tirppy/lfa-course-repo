import random

class Grammar:
    def __init__(self):
        self.VN = {"S", "L", "D"}  
        self.VT = {"a", "b", "c", "d", "e", "f", "j"}  
        self.P = {  
            "S": ["aS", "bS", "cD", "dL", "e"],
            "L": ["eL", "fL", "jD", "e"],
            "D": ["eD", "d"]
        }
        self.start_symbol = "S"

    def generate_string(self):
        current_string = self.start_symbol
        while any(char in self.VN for char in current_string):  
            for nt in current_string:
                if nt in self.VN:
                    replacement = random.choice(self.P[nt])  
                    current_string = current_string.replace(nt, replacement, 1)
                    break  
        return current_string

    def generate_strings(self, n=5):
        return [self.generate_string() for _ in range(n)]

    def to_finite_automaton(self):
        states = set(self.VN) | {"q_accept"}  
        alphabet = self.VT
        transitions = {}

        for non_terminal, rules in self.P.items():
            for rule in rules:
                if len(rule) == 1:  
                    transitions[(non_terminal, rule)] = "q_accept"
                else:
                    terminal, next_state = rule[0], rule[1:]
                    transitions[(non_terminal, terminal)] = next_state

        return FiniteAutomaton(states, alphabet, transitions, "S", {"q_accept"})

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def string_belongs(self, input_string):
        current_state = self.start_state
        for char in input_string:
            if (current_state, char) in self.transitions:
                current_state = self.transitions[(current_state, char)]
            else:
                return False
        return current_state in self.final_states

def main():
    
    grammar = Grammar()
    print("Generate Strings:")
    for string in grammar.generate_strings():
        print(f" - {string}")

    finite_automaton = grammar.to_finite_automaton()

    test_strings = ["abcde", "dde", "aae", "ce", "bdf"]
    print("\nCheck Strings:")
    for test in test_strings:
        result = "Accepted" if finite_automaton.string_belongs(test) else "Rejected"
        print(f" - '{test}' -> {result}")

if __name__ == "__main__":
    main()