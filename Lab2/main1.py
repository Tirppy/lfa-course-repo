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

        # self.VN = {"S", "A", "B", "C"}  
        # self.VT = {"a", "b"}  
        # self.P = {  
        #     "S": ["aAB"],   
        #     "A": ["aB", "b"],  
        #     "B": ["bC", "a"],  
        #     "C": ["b"]   
        # }
        # self.start_symbol = "S"  

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

    def classify_grammar(self):
        if self.is_regular():
            return "Type 3 (Regular)"
        
        if self.is_context_free():
            return "Type 2 (Context-free)"
        
        if self.is_context_sensitive():
            return "Type 1 (Context-sensitive)"
        
        return "Type 0 (Recursively enumerable)"
    
    def is_regular(self):
        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                if len(rhs) > 2:
                    return False
                if len(rhs) == 2:
                    if rhs[0] not in self.VT or rhs[1] not in self.VN:
                        if rhs[1] not in self.VT or rhs[0] not in self.VN:
                            return False
                elif len(rhs) == 1 and rhs[0] not in self.VT and rhs != "":
                    return False
        return True
    
    def is_context_free(self):
        for lhs, rhs_list in self.P.items():
            if len(lhs) != 1 or lhs not in self.VN:
                return False
            for rhs in rhs_list:
                if len(rhs) < 1:
                    return False
                if not all(symbol in self.VN or symbol in self.VT for symbol in rhs):
                    return False
        return True
    
    def is_context_sensitive(self):
        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                if len(lhs) > len(rhs):
                    return False
        return True

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_state = final_states

    def string_belongs(self, input_string):
        current_state = self.start_state
        for char in input_string:
            if (current_state, char) in self.transitions:
                current_state = self.transitions[(current_state, char)]
            else:
                return False
        return current_state in self.final_state

def main():
    grammar = Grammar()

    print("\nGenerate Strings:")
    for string in grammar.generate_strings():
        print(f" - {string}")

    finite_automaton = grammar.to_finite_automaton()

    test_strings = ["abcde", "dde", "aae", "ce", "bdf"]
    print("\nCheck Strings:")
    for test in test_strings:
        result = "Accepted" if finite_automaton.string_belongs(test) else "Rejected"
        print(f" - '{test}' -> {result}")

    print("\nGrammar Classification:")
    print(grammar.classify_grammar())

if __name__ == "__main__":
    main()
