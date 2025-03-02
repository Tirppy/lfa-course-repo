### Course: Formal Languages & Finite Automata
### Author: Alexandru Cebotari

----

## Theory

### Automata Theory Overview

Automata theory is the study of abstract machines and the problems they can solve. It forms the foundation of computational theory, helping us understand the limits of computation. In particular, the study of finite automata plays a crucial role in understanding regular languages, which are the simplest class of formal languages.

An **automaton** (plural: automata) is a mathematical model of computation that takes an input and processes it according to a set of predefined rules, producing an output or transitioning between states.

### Finite Automata (FA)

A **Finite Automaton (FA)** is a theoretical machine used to recognize patterns within input data. It consists of:
- A finite set of states (one of which is designated as the start state).
- A set of input symbols (alphabet).
- A transition function that defines how to move from one state to another.
- A set of accepting (or final) states.
- A start state.

There are two primary types of finite automata:
1. **Deterministic Finite Automaton (DFA)**:
   - In a DFA, for each state and input symbol, there is exactly one transition to a new state. This ensures a unique path through the automaton for any given input string.
   
2. **Non-Deterministic Finite Automaton (NDFA or NFA)**:
   - In an NDFA, for some state and input symbol, there can be multiple possible next states or no transition at all. In such cases, the automaton can "choose" a path non-deterministically, leading to different possible computations.

### Chomsky Hierarchy

The Chomsky Hierarchy is a classification of formal grammars based on their generative power. It was introduced by Noam Chomsky in 1956. The hierarchy consists of four levels:

1. **Type 0 (Recursively Enumerable Languages)**: These grammars can generate any language that can be recognized by a Turing machine. They have no restrictions on their production rules.
   
2. **Type 1 (Context-Sensitive Languages)**: These grammars have rules where the left side of a production may contain more symbols than the right side, but they are still more restricted than Type 0.
   
3. **Type 2 (Context-Free Languages)**: These grammars are more restricted, where the left side of each production rule must consist of exactly one non-terminal symbol. Context-free grammars can describe many programming languages and are useful in syntax analysis (parsing).
   
4. **Type 3 (Regular Languages)**: These grammars have even more restrictive rules, where the left side of a production is always a single non-terminal and the right side is a single terminal symbol or a non-terminal followed by a terminal. Regular languages are typically described by regular expressions or finite automata.

### Conversion from NDFA to DFA

The process of converting a Non-Deterministic Finite Automaton (NDFA) to a Deterministic Finite Automaton (DFA) is known as the **Subset Construction** or **Powerset Construction** method. This is a critical step in automata theory because, while NFAs are easier to design, DFAs are easier to implement. The conversion process involves:
- Creating a state in the DFA for every possible subset of states in the NDFA.
- Defining transitions based on the union of transitions from the NDFA.
- Marking final states in the DFA based on the presence of final states in the NDFA.

This conversion is essential because DFAs are used in practical applications like lexical analysis in compilers, while NFAs are mainly a theoretical concept.

### Regular Grammar

A **Regular Grammar** is a type of grammar that generates regular languages, and it can be used to represent the same languages that DFAs and NFAs recognize. A regular grammar has specific production rules that allow it to be easily converted to a finite automaton and vice versa. There are two forms of regular grammar:
1. **Right-Regular Grammar**: All production rules are of the form \( A \rightarrow xB \) or \( A \rightarrow x \), where \( A, B \) are non-terminals, and \( x \) is a terminal symbol.
2. **Left-Regular Grammar**: All production rules are of the form \( A \rightarrow Bx \) or \( A \rightarrow x \).

Converting a finite automaton to a regular grammar involves creating production rules based on the transitions between states in the automaton. This is a process that helps represent a finite automaton in the form of a grammar.

### Determinism in Finite Automata

The concept of **determinism** refers to whether an automaton behaves in a predictable manner. A deterministic automaton always follows one, and only one, transition for any given input symbol from any state. In contrast, a non-deterministic automaton may follow multiple paths for the same input symbol, allowing it to process inputs in a less predictable manner.

- **Deterministic Finite Automaton (DFA)**: In a DFA, there are no choices to make during computation. Every input symbol leads to exactly one transition from any given state.
- **Non-Deterministic Finite Automaton (NDFA or NFA)**: An NDFA can have multiple possible transitions for the same input symbol, or it can have transitions based on no input symbol at all (epsilon transitions). 

While DFAs are easier to implement and simulate, NFAs are often simpler to design. However, it is important to note that **NFAs and DFAs are equivalent in terms of the languages they can recognize** — they both recognize exactly the set of regular languages. The conversion from NFA to DFA, though, often results in a DFA that has exponentially more states than the original NFA.


## Objectives:

The primary objectives of this lab are to:

1. **Understand what an automaton is and what it can be used for**:
   - Gain a deep understanding of the concept of automata, their components (such as states, input alphabet, transition function, start and final states), and how they process input to recognize patterns and languages.

2. **Classify a grammar based on the Chomsky hierarchy**:
   - Implement a function in the grammar type/class that can determine the classification of a grammar (Type 0, Type 1, Type 2, Type 3) according to the Chomsky hierarchy, based on its production rules.

3. **Convert a finite automaton to a regular grammar**:
   - Develop the ability to convert a given finite automaton (whether deterministic or non-deterministic) into an equivalent regular grammar, which can then be used to generate the same language.

4. **Determine whether the finite automaton is deterministic or non-deterministic**:
   - Analyze a given finite automaton and determine whether it is a DFA (Deterministic Finite Automaton) or an NFA (Non-Deterministic Finite Automaton). Understand the key differences between these types of automata.

5. **Convert a Non-Deterministic Finite Automaton (NDFA) to a Deterministic Finite Automaton (DFA)**:
   - Implement a conversion algorithm that transforms an NDFA into an equivalent DFA using the subset construction or powerset construction method.

6. **Represent the finite automaton graphically** (Optional):
   - Utilize external libraries, tools, or APIs to graphically represent the structure of the finite automaton, providing a visual representation of the states, transitions, and start/final states.

7. **Document the conversion process and code changes**:
   - Write a detailed report that describes the conversion process, the implementation steps taken, and any challenges or modifications encountered during the task.

## Implementation description

In this section, we describe the implementation of the lab tasks and the functions that were used to solve each part.
The implementation covers several key aspects such as grammar classification, conversion of finite automata to regular grammar, checking determinism, converting NFA to DFA, and visualizing the automaton.

### Functions Used

#### 1. **`classify_grammar(self)`**
```
    def classify_grammar(self):
        if self.is_regular():
            return "Type 3 (Regular)"
        
        if self.is_context_free():
            return "Type 2 (Context-free)"
        
        if self.is_context_sensitive():
            return "Type 1 (Context-sensitive)"
        
        return "Type 0 (Recursively enumerable)"
```
This function classifies a grammar based on the Chomsky hierarchy. It checks if the grammar is of type 3 (Regular), type 2 (Context-Free), type 1 (Context-Sensitive), or type 0 (Recursively Enumerable).
It utilizes helper functions (`is_regular()`, `is_context_free()`, and `is_context_sensitive()`) to determine the type of the grammar. The function returns the classification as a string.

#### 2. **`is_regular(self)`**
```
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
```
This helper function checks if the grammar is a regular grammar (Type 3).
It verifies that all production rules conform to the regular grammar rules. It checks that the right-hand side of each production is either a terminal symbol or a combination of terminal and non-terminal symbols.

#### 3. **`is_context_free(self)`**
```
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
```
This helper function checks if the grammar is context-free (Type 2).
It checks if each production rule has a left-hand side consisting of a single non-terminal and the right-hand side composed of terminals and non-terminals.

#### 4. **`is_context_sensitive(self)`**
```
    def is_context_sensitive(self):
        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                if len(lhs) > len(rhs):
                    return False
        return True
```
This helper function checks if the grammar is context-sensitive (Type 1).
It checks that for every production rule, the length of the left-hand side is less than or equal to the length of the right-hand side, adhering to the rules of context-sensitive grammars.

#### 5. **`to_regular_grammar(self)`**
```
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
```
This function converts a finite automaton to a regular grammar.
The function generates non-terminal symbols based on the states of the automaton. It then creates production rules by converting state transitions into grammar rules. It handles final states by adding empty productions for them.

#### 6. **`is_deterministic(self)`**
```
    def is_deterministic(self):
        for (state, char), next_states in self.transitions.items():
            if len(next_states) > 1:  
                return False
        return True
```
This function checks whether a given finite automaton is deterministic (DFA) or non-deterministic (NFA).
It checks the transitions of the automaton and ensures that each state and input symbol pair leads to exactly one state. If there are multiple transitions for any state and input symbol, the automaton is classified as non-deterministic.

#### 7. **`convert_to_dfa(self)`**
```
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
```
This function converts a non-deterministic finite automaton (NDFA) into a deterministic finite automaton (DFA) using the subset construction algorithm.
It creates new states in the DFA corresponding to the subsets of states from the NFA. It then computes transitions for the new states and identifies final states in the DFA based on the presence of final states in the original NFA.

#### 8. **`visualize(self, is_nfa=True)`**
```
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
```
This function generates a graphical representation of the finite automaton using the Graphviz library.
It creates a directed graph where nodes represent states and edges represent transitions. The function visualizes both NFAs and DFAs by distinguishing start states (with a special color) and final states (using double circles). The graph is saved as a PNG image for easy visualization.

## Conclusions / Screenshots / Results

In this lab, we successfully explored several key concepts related to finite automata and their interactions with formal grammar. The primary objectives were achieved through the development and implementation of various functions for converting finite automata to regular grammars, checking determinism, converting NFA to DFA, and generating graphical representations of automata. The results can be summarized as follows:

1. **Grammar Classification**: The function `classify_grammar` was implemented to classify grammars according to the Chomsky hierarchy. The grammar was successfully identified as either Type 3 (Regular), Type 2 (Context-Free), Type 1 (Context-Sensitive), or Type 0 (Recursively Enumerable) based on the given production rules.

2. **Finite Automaton to Regular Grammar**: The `to_regular_grammar` function correctly converted a given finite automaton to a regular grammar. The conversion process generated non-terminal symbols from the states of the automaton and translated transitions into production rules. The start and final symbols were also accurately determined.

3. **Determinism Check**: The `is_deterministic` function correctly identified whether a finite automaton was deterministic (DFA) or non-deterministic (NFA) by checking if multiple transitions existed for the same state and input symbol.

4. **NFA to DFA Conversion**: The `convert_to_dfa` function successfully performed the subset construction algorithm, converting a non-deterministic finite automaton (NFA) into an equivalent deterministic finite automaton (DFA). The conversion ensured that all transitions were deterministic and provided an accurate mapping of states between the NFA and DFA.

5. **Visualization**: The `visualize` function generated clear and accurate visual representations of both NFAs and DFAs using the Graphviz library. The graphical diagrams illustrated the states, transitions, start states, and final states in an intuitive manner. These visualizations were helpful in understanding the structure of the automata.

**Example Output:**

- **Regular Grammar Output**:
```
Regular Grammar:
VN: {'Q0', 'Q3', 'Q2', 'Q1'}
VT: {'b', 'a'}
P: {'Q3': [''], 'Q0': ['aQ1', 'aQ2'], 'Q1': ['bQ1', 'aQ2'], 'Q2': ['aQ1', 'bQ3']}
Start Symbol: Q0
Final Symbols: {'Q3'}
```

- **Convert to DFA**:  
```
DFA States: {'q1', 'q3', 'q13', 'q0', 'q12', 'q2'}
DFA Alphabet: {'b', 'a'}
DFA Transitions:
  (q0, a) -> ['q12']
  (q12, b) -> ['q13']
  (q12, a) -> ['q12']
  (q13, b) -> ['q1']
  (q13, a) -> ['q2']
  (q2, b) -> ['q3']
  (q2, a) -> ['q1']
  (q1, b) -> ['q1']
  (q1, a) -> ['q2']
DFA Start State: q0
DFA Final States: {'q3', 'q13'}
```

- **NFA Graph**:  
![nfa_graph](https://github.com/user-attachments/assets/0effd9dd-85cf-4b25-92d3-0479b931ca76)


- **DFA Graph**:  
![dfa_graph](https://github.com/user-attachments/assets/a30e3273-a259-4327-8e86-24eb39e77f58)


## Results

The results of this lab demonstrated the following:

- **Finite Automaton Conversion**: The conversion from finite automaton to regular grammar was performed successfully, and the resulting grammar followed the rules of a regular grammar.

- **Correctness of Determinism Check**: The determinism check function worked correctly, distinguishing between deterministic and non-deterministic finite automata.

- **Successful NFA to DFA Conversion**: The NFA to DFA conversion was implemented correctly, and the resulting DFA was deterministic with no ambiguities in state transitions.

- **Graphical Representation**: The visualization feature using Graphviz was a valuable addition to the project, offering a visual understanding of both NFA and DFA structures.

Overall, the project was successful in meeting its objectives, and the implemented functions provided the necessary tools for analyzing and manipulating finite automata. The use of Graphviz for visualization significantly enhanced the interpretability of the automaton structures.

## References

_Formal Languages and Finite Automata, Guide for practical lessons_ by COJUHARI Irina, DUCA Ludmila, FIODOROV Ion -
https://else.fcim.utm.md/pluginfile.php/110458/mod_resource/content/0/LFPC_Guide.pdf
