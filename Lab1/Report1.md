# Intro to formal languages. Regular grammars. Finite Automata.

### Course: Formal Languages & Finite Automata
### Author: Alexandru Cebotari

----

## Theory
A formal language consists of an alphabet, a vocabulary, and a grammar.
The grammar defines the rules for constructing valid words in the language, and the automaton defines a mechanism for recognizing strings belonging to the language.
This project explores the relationship between regular grammars and finite automata by converting a given grammar into a finite automaton and checking if a string belongs to the language defined by the grammar.
A finite automaton (FA) is a state machine with a finite number of states that processes input strings one symbol at a time, transitioning between states based on predefined rules.


## Objectives:

* Implement a Grammar class to represent a given grammar.
* Implement a Finite Automaton (FA) class to convert the grammar to an automaton.
* Implement a method to generate valid strings from the grammar.
* Implement functionality to check if a string belongs to the language accepted by the automaton.


## Implementation description

* "generate_string" generates a single valid string from the grammar by starting from the start symbol and recursively replacing non-terminals with corresponding production rules until no non-terminal symbols remain.

```
def generate_string(self):
    current_string = self.start_symbol
    while any(char in self.VN for char in current_string):  
        for nt in current_string:
            if nt in self.VN:
                replacement = random.choice(self.P[nt])  
                current_string = current_string.replace(nt, replacement, 1)
                break  
    return current_string
```

* "to_finite_automaton" converts the grammar into a Finite Automaton representation.
* It builds the FA's states, alphabet, and transition function from the grammar.

```
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
```

* "string_belongs" checks if a given input string is accepted by the finite automaton.

```
def string_belongs(self, input_string):
    current_state = self.start_state
    for char in input_string:
        if (current_state, char) in self.transitions:
            current_state = self.transitions[(current_state, char)]
        else:
            return False
    return current_state in self.final_states
```

## Conclusions / Screenshots / Results

The program successfully implements the conversion of a given regular grammar into a finite automaton.
The Grammar class generates strings based on the production rules, and the FiniteAutomaton class checks whether a string belongs to the language.
For example, the string "abcde" is rejected because there is no valid transition for the last symbol "e" from the accepting state.

Example of output:
```
Generate Strings:
 - e
 - cd
 - cd
 - djd
 - cd

Check Strings:
 - 'abcde' -> Rejected
 - 'dde' -> Rejected
 - 'aae' -> Accepted
 - 'ce' -> Rejected
```

## References

_Formal Languages and Finite Automata, Guide for practical lessons_ by COJUHARI Irina, DUCA Ludmila, FIODOROV Ion -
https://else.fcim.utm.md/pluginfile.php/110458/mod_resource/content/0/LFPC_Guide.pdf
