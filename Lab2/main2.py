import graphviz

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def to_regular_grammar(self):
        # Convert the FA to a regular grammar
        VN = {state.upper() for state in self.states}  # Non-terminal symbols
        VT = self.alphabet  # Terminal symbols
        P = {state.upper(): [] for state in self.states}  # Production rules
        
        for (state, char), next_states in self.transitions.items():
            for next_state in next_states:
                P[state.upper()].append(char + next_state.upper())  # Add transition as production
        
        for final_state in self.final_states:
            P[final_state.upper()].append("")  # Final states have an empty production
        
        start_symbol = self.start_state.upper()  # Start symbol of the grammar
        final_symbol = {state.upper() for state in self.final_states}  # Final symbols in the grammar
        
        return VN, VT, P, start_symbol, final_symbol

    def is_deterministic(self):
        # Check if the automaton is deterministic
        for (state, char), next_states in self.transitions.items():
            if len(next_states) > 1:  # If multiple next states exist for the same state and symbol
                return False
        return True
    
    def convert_to_dfa(self):
        # Convert NDFA to DFA using the subset construction algorithm
        dfa_states = set()
        dfa_transitions = {}
        dfa_start_state = frozenset([self.start_state])
        dfa_final_states = set()
        unprocessed_states = [dfa_start_state]
        state_mapping = {dfa_start_state: "q0"}  # Mapping NDFA state to DFA state
        state_counter = 1

        while unprocessed_states:
            current_state = unprocessed_states.pop()
            dfa_states.add(current_state)
            for symbol in self.alphabet:
                next_state = frozenset(
                    sum((self.transitions.get((sub_state, symbol), []) for sub_state in current_state), []))
                if next_state:
                    state_name = "q" + "".join(sorted(next_state)).replace("q", "")
                    if next_state not in state_mapping:
                        state_mapping[next_state] = state_name
                        unprocessed_states.append(next_state)
                    # Save the transition from current state to next state
                    dfa_transitions[(state_mapping[current_state], symbol)] = [state_mapping[next_state]]
        
        for state in dfa_states:
            if any(sub_state in self.final_states for sub_state in state):
                dfa_final_states.add(state_mapping[state])
        
        # Create DFA using the calculated state names and transitions
        dfa = FiniteAutomaton(
            states=set(state_mapping.values()),
            alphabet=self.alphabet,
            transitions=dfa_transitions,
            start_state=state_mapping[dfa_start_state],
            final_states=dfa_final_states,
        )
        return dfa

    def visualize(self, is_nfa=True):
        # Visualize the FA (either NFA or DFA) using Graphviz
        dot = graphviz.Digraph(format='png', engine='dot')
        
        # Add nodes for all states
        for state in self.states:
            if state == self.start_state:
                dot.node(state, shape='ellipse', style='filled', fillcolor='lightblue', label=f"start\n{state}")
            elif state in self.final_states:
                dot.node(state, shape='doublecircle', label=f"final\n{state}")
            else:
                dot.node(state, shape='ellipse', label=state)

        # Add transitions
        for (state, symbol), next_states in self.transitions.items():
            for next_state in next_states:
                if is_nfa:
                    # For NFA: multiple transitions for the same symbol are allowed
                    dot.edge(state, next_state, label=symbol)
                else:
                    # For DFA: transition is deterministic
                    dot.edge(state, next_state, label=symbol)
        
        # Render the diagram to a file
        if is_nfa:
            dot.render('nfa_graph')  # Save NFA as 'nfa_graph.png'
            print("NFA Graph has been generated and saved as 'nfa_graph.png'.")
        else:
            dot.render('dfa_graph')  # Save DFA as 'dfa_graph.png'
            print("DFA Graph has been generated and saved as 'dfa_graph.png'.")

def main():
    # Example Finite Automaton
    states = {"q0", "q1", "q2", "q3"}
    alphabet = {"a", "b"}
    transitions = {
        ("q0", "a"): ["q1", "q2"],
        ("q1", "b"): ["q1"],
        ("q1", "a"): ["q2"],
        ("q2", "a"): ["q1"],
        ("q2", "b"): ["q3"],
    }
    start_state = "q0"
    final_states = {"q3"}

    # Create the NFA
    fa = FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

    # Convert to Regular Grammar
    VN, VT, P, start_symbol, final_symbol = fa.to_regular_grammar()
    print("Regular Grammar:")
    print("VN:", VN)
    print("VT:", VT)
    print("P:", P)
    print("Start Symbol:", start_symbol)
    print("Final Symbols:", final_symbol)

    # Check if the FA is deterministic or non-deterministic
    print("Is Deterministic:", fa.is_deterministic())

    # Visualize the NFA
    fa.visualize(is_nfa=True)

    # Convert the NFA to DFA
    dfa = fa.convert_to_dfa()

    # Print the DFA details
    print("\nDFA States:", dfa.states)
    print("DFA Alphabet:", dfa.alphabet)
    print("DFA Transitions:")
    for (state, symbol), next_states in dfa.transitions.items():
        print(f"  ({state}, {symbol}) -> {next_states}")
    print("DFA Start State:", dfa.start_state)
    print("DFA Final States:", dfa.final_states)

    # Visualize the DFA
    dfa.visualize(is_nfa=False)

if __name__ == "__main__":
    main()
