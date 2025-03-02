import graphviz

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def to_regular_grammar(self):
        VN = {state.upper() for state in self.states}  
        VT = self.alphabet  
        P = {state.upper(): [] for state in self.states}  
        
        for (state, char), next_states in self.transitions.items():
            for next_state in next_states:
                P[state.upper()].append(char + next_state.upper())  
        
        for final_state in self.final_states:
            P[final_state.upper()].append("")  
        
        start_symbol = self.start_state.upper()  
        final_symbol = {state.upper() for state in self.final_states}  
        
        return VN, VT, P, start_symbol, final_symbol

    def is_deterministic(self):
        for (state, char), next_states in self.transitions.items():
            if len(next_states) > 1:  
                return False
        return True
    
    def convert_to_dfa(self):
        dfa_states = set()
        dfa_transitions = {}
        dfa_start_state = frozenset([self.start_state])
        dfa_final_states = set()
        unprocessed_states = [dfa_start_state]
        state_mapping = {dfa_start_state: "q0"}  
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
                    dfa_transitions[(state_mapping[current_state], symbol)] = [state_mapping[next_state]]
        
        for state in dfa_states:
            if any(sub_state in self.final_states for sub_state in state):
                dfa_final_states.add(state_mapping[state])
        
        dfa = FiniteAutomaton(
            states=set(state_mapping.values()),
            alphabet=self.alphabet,
            transitions=dfa_transitions,
            start_state=state_mapping[dfa_start_state],
            final_states=dfa_final_states,
        )
        return dfa

    def visualize(self, is_nfa=True):
        dot = graphviz.Digraph(format='png', engine='dot')
        
        for state in self.states:
            if state == self.start_state:
                dot.node(state, shape='ellipse', style='filled', fillcolor='lightblue', label=f"start\n{state}")
            elif state in self.final_states:
                dot.node(state, shape='doublecircle', label=f"final\n{state}")
            else:
                dot.node(state, shape='ellipse', label=state)

        for (state, symbol), next_states in self.transitions.items():
            for next_state in next_states:
                if is_nfa:
                    dot.edge(state, next_state, label=symbol)
                else:
                    dot.edge(state, next_state, label=symbol)
        
        if is_nfa:
            dot.render('nfa_graph')  
            print("NFA Graph has been generated and saved as 'nfa_graph.png'.")
        else:
            dot.render('dfa_graph')  
            print("DFA Graph has been generated and saved as 'dfa_graph.png'.")

def main():
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

    fa = FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

    VN, VT, P, start_symbol, final_symbol = fa.to_regular_grammar()
    print("Regular Grammar:")
    print("VN:", VN)
    print("VT:", VT)
    print("P:", P)
    print("Start Symbol:", start_symbol)
    print("Final Symbols:", final_symbol)

    print("Is Deterministic:", fa.is_deterministic())

    fa.visualize(is_nfa=True)

    dfa = fa.convert_to_dfa()

    print("\nDFA States:", dfa.states)
    print("DFA Alphabet:", dfa.alphabet)
    print("DFA Transitions:")
    for (state, symbol), next_states in dfa.transitions.items():
        print(f"  ({state}, {symbol}) -> {next_states}")
    print("DFA Start State:", dfa.start_state)
    print("DFA Final States:", dfa.final_states)

    dfa.visualize(is_nfa=False)

if __name__ == "__main__":
    main()
