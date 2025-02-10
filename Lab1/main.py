import random

class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
        
    def generate_string(self):
        return self._generate_from_symbol(self.start_symbol)
    
    def _generate_from_symbol(self, symbol):
        if symbol in self.terminals:
            return random.choice(symbol)
        production = random.choice(self.productions[symbol])
        result = ""
        for part in production:
            result += self._generate_from_symbol(part)
        return result
    
    def to_finite_automaton(self):
        states = ['q0', 'q1', 'q2']
        alphabet = self.terminals
        delta = {
            'q0': {'a': 'q0', 'b': 'q0', 'c': 'q1', 'd': 'q2', 'e': 'q1'},
            'q1': {'e': 'q1', 'f': 'q1', 'j': 'q2'},
            'q2': {'e': 'q2', 'd': 'q2'}
        }
        start_state = 'q0'
        final_states = ['q1', 'q2']
        
        return FiniteAutomaton(states, alphabet, delta, start_state, final_states)


class FiniteAutomaton:
    def __init__(self, states, alphabet, delta, start_state, final_states):
        self.states = states            # List of states
        self.alphabet = alphabet        # List of alphabet symbols
        self.delta = delta              # Transition function (dict)
        self.start_state = start_state  # Start state
        self.final_states = final_states # Set of final (accepting) states
        
    def string_belong_to_language(self, input_string):
        """Check if the input string belongs to the language of the automaton."""
        current_state = self.start_state  # Start from the initial state
        
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False  # Invalid symbol in input
            if symbol in self.delta[current_state]:
                current_state = self.delta[current_state][symbol]
            else:
                return False  # No valid transition for this symbol
        return current_state in self.final_states  # Check if the end state is final


def main():
    non_terminals = ['S', 'L', 'D']
    terminals = ['a', 'b', 'c', 'd', 'e', 'f', 'j']
    productions = {
        'S': [['a', 'S'], ['b', 'S'], ['c', 'D'], ['d', 'L'], ['e']],
        'L': [['e', 'L'], ['f', 'L'], ['j', 'D'], ['e']],
        'D': [['e', 'D'], ['d']]
    }
    start_symbol = 'S'

    grammar = Grammar(non_terminals, terminals, productions, start_symbol)

    print("Generated:")
    for _ in range(5):
        print(grammar.generate_string())

    automaton = grammar.to_finite_automaton()

    # Check if strings belong to the automaton's language
    test_strings = ['ab', 'cdd', 'aa', 'ee', 'bfd']
    print("\nChecking:")
    for test_string in test_strings:
        result = automaton.string_belong_to_language(test_string)
        print(f"'{test_string}' -> {'Valid' if result else 'Invalid'}")


if __name__ == "__main__":
    main()
