# Intro to formal languages. Regular grammars. Finite Automata.

### Course: Formal Languages & Finite Automata
### Author: Alexandru Cebotari

----

## Theory

### Grammar and Formal Languages  
A **grammar** is a formal description of a language, specifying how valid strings in the language are constructed. A grammar consists of a set of **production rules**, which define how symbols can be replaced to generate strings. The standard form of a grammar is given by a **4-tuple (V, Σ, P, S)**, where:  

- **V (Variables/Non-terminals)**: A finite set of symbols that can be replaced.  
- **Σ (Alphabet/Terminals)**: A finite set of symbols that form the actual strings of the language.  
- **P (Production Rules)**: A finite set of rules that define how variables can be replaced with terminals or other variables.  
- **S (Start Symbol)**: A special variable from which derivations begin.  

Grammars are classified into different types based on the **Chomsky Hierarchy**:  

1. **Type 0 (Unrestricted Grammars)**: The most general form, with no restrictions on production rules.  
2. **Type 1 (Context-Sensitive Grammars)**: Rules must have a form `α → β`, where `|α| ≤ |β|`.  
3. **Type 2 (Context-Free Grammars - CFGs)**: Each rule has the form `A → γ`, where `A` is a single non-terminal.  
4. **Type 3 (Regular Grammars)**: Each rule follows the form `A → aB` or `A → a`, making them suitable for **finite automata**.  

### Finite Automata (FA)  
A **Finite Automaton** is a mathematical model used to recognize regular languages. It consists of a finite number of states and transitions between them based on input symbols. The two main types of finite automata are:  

- **Deterministic Finite Automata (DFA)**: Each state has exactly one transition per input symbol.  
- **Nondeterministic Finite Automata (NFA)**: A state may have multiple transitions for the same input symbol, or ε-transitions (moves without consuming input).  

A finite automaton is formally defined as a **5-tuple (Q, Σ, δ, q₀, F)**, where:  

- **Q**: A finite set of states.  
- **Σ**: The input alphabet.  
- **δ (Transition Function)**: A function mapping `Q × Σ → Q` for DFAs (or `Q × Σ → 2^Q` for NFAs).  
- **q₀**: The initial state.  
- **F**: A set of final (accepting) states.  

### Grammar-to-Automaton Conversion  
A **Regular Grammar** can be converted into a **Finite Automaton**, following these steps:  

1. Each **non-terminal** in the grammar becomes a **state** in the FA.  
2. Production rules like `A → aB` create a transition `A → B` on input `'a'`.  
3. If a rule has only a terminal, like `A → a`, the transition leads to a final state.  

### String Generation & Language Recognition  
- **String Generation**: A grammar can be used to **generate valid strings** by applying production rules starting from the initial symbol.  
- **String Recognition**: The automaton can check whether a given string belongs to the language by starting from the initial state and following valid transitions. If the automaton ends in an accepting state, the string is valid.  

This theoretical foundation forms the basis for implementing a **Grammar class** and a **Finite Automaton class**, enabling the conversion of grammars into automata, string generation, and language recognition.


## Objectives:

* Implement a Grammar class to represent a given grammar.
* Implement a Finite Automaton (FA) class to convert the grammar to an automaton.
* Implement a method to generate valid strings from the grammar.
* Implement functionality to check if a string belongs to the language accepted by the automaton.


## Implementation description

The program consists of two main classes:

1. **Grammar**: Represents a formal grammar and allows string generation.
2. **FiniteAutomaton**: Represents a finite automaton converted from the grammar, allowing string validation.

The `main()` function initializes and demonstrates both classes. Below is a breakdown of each component:

### 1. Grammar Class

The `Grammar` class defines a **formal grammar** with non-terminal symbols, terminal symbols, production rules, and a start symbol. It provides methods to **generate strings** and **convert the grammar into a finite automaton**.

#### Instance Variables
The constructor initializes the grammar components:

```
    class Grammar:
        def __init__(self):
            self.VN = {"S", "L", "D"}  # Non-terminal symbols
            self.VT = {"a", "b", "c", "d", "e", "f", "j"}  # Terminal symbols
            self.P = {  # Production rules
                "S": ["aS", "bS", "cD", "dL", "e"],
                "L": ["eL", "fL", "jD", "e"],
                "D": ["eD", "d"]
            }
            self.start_symbol = "S"  # The start symbol
```

- **VN**: Set of **non-terminal symbols** `{S, L, D}`
- **VT**: Set of **terminal symbols** `{a, b, c, d, e, f, j}`
- **P**: Dictionary representing **production rules**
- **start_symbol**: The starting point of derivation

### 2. Generating Strings from the Grammar

The `generate_string` method creates a valid string by **randomly replacing non-terminals** with terminal sequences until only terminal symbols remain.

#### Function: `generate_string()`

```
    def generate_string(self):
        current_string = self.start_symbol
        while any(char in self.VN for char in current_string):  # Continue while there are non-terminals
            for nt in current_string:
                if nt in self.VN:  
                    replacement = random.choice(self.P[nt])  # Replace with a random rule
                    current_string = current_string.replace(nt, replacement, 1)  # Apply only one replacement
                    break  
        return current_string
```

**Steps:**
1. Start with the **start symbol** `"S"`.
2. Check if the string contains any **non-terminal symbols**.
3. Replace the first non-terminal encountered with one of its **random production rules**.
4. Repeat until only **terminal symbols** remain.
5. Return the generated string.

#### Function: `generate_strings(n=5)`

    def generate_strings(self, n=5):
        return [self.generate_string() for _ in range(n)]

- Calls `generate_string()` **n times** to generate multiple strings.

### 3. Converting Grammar to Finite Automaton

The `to_finite_automaton` method constructs a **finite automaton (FA)** equivalent to the grammar.

#### Function: `to_finite_automaton()`

```
    def to_finite_automaton(self):
        states = set(self.VN) | {"q_accept"}  # Non-terminals as states, plus a final state
        alphabet = self.VT
        transitions = {}

        for non_terminal, rules in self.P.items():
            for rule in rules:
                if len(rule) == 1:  # If rule leads to only a terminal, it reaches final state
                    transitions[(non_terminal, rule)] = "q_accept"
                else:
                    terminal, next_state = rule[0], rule[1:]  
                    transitions[(non_terminal, terminal)] = next_state  

        return FiniteAutomaton(states, alphabet, transitions, "S", {"q_accept"})
```

**Steps:**
1. **Define states**: Each **non-terminal** becomes a **state**, and an additional `"q_accept"` state is added.
2. **Define transitions**:
   - If a rule consists of a **single terminal**, it transitions to `"q_accept"`.
   - Otherwise, the first symbol becomes a **transition** to another state.
3. **Return a `FiniteAutomaton` object** initialized with these transitions.

### 4. Finite Automaton Class

The `FiniteAutomaton` class implements a **finite state machine** that checks if a string belongs to the language generated by the grammar.

#### Constructor: Initializing FA

```
    class FiniteAutomaton:
        def __init__(self, states, alphabet, transitions, start_state, final_states):
            self.states = states
            self.alphabet = alphabet
            self.transitions = transitions
            self.start_state = start_state
            self.final_states = final_states
```

- **States**: All possible states in the automaton.
- **Alphabet**: Set of valid input symbols.
- **Transitions**: Dictionary mapping **(state, input) → next state**.
- **Start state**: `"S"` (from the grammar).
- **Final states**: `{q_accept}` (indicating a valid string).

### 5. Checking if a String Belongs to the Language

The `string_belongs` method **simulates the automaton** to check whether a given string is accepted by the FA.

#### Function: `string_belongs(input_string)`

```
    def string_belongs(self, input_string):
        current_state = self.start_state
        for char in input_string:
            if (current_state, char) in self.transitions:
                current_state = self.transitions[(current_state, char)]
            else:
                return False  # No valid transition, reject the string
        return current_state in self.final_states
```

**Steps:**
1. Start in the **initial state** (`"S"`).
2. For each **character in the input string**, check if there’s a valid transition.
3. If no transition exists, **reject the string**.
4. After processing, check if the final state is an **accepting state** (`"q_accept"`).

### 6. Running the Program

The `main()` function demonstrates the functionality by:

1. **Generating random strings** using `Grammar`.
2. **Converting the grammar to an automaton**.
3. **Testing predefined strings** to see if they are accepted.

#### Function: `main()`

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

**Steps:**
1. **Create a `Grammar` object**.
2. **Generate and print 5 random strings** from the grammar.
3. **Convert the grammar into an automaton**.
4. **Test predefined strings** to check if they belong to the language.
5. **Print "Accepted" or "Rejected"** based on the automaton’s response.

## Conclusions / Screenshots / Results

This program successfully demonstrates the relationship between **grammars** and **finite automata**. Through the implementation of the `Grammar` and `FiniteAutomaton` classes, we are able to:

- **Generate random strings** from a given grammar using production rules.
- **Convert a grammar to a finite automaton** and simulate its behavior to check if a string belongs to the language generated by the grammar.

From the example output:

Example of output:
```
Generate Strings:
 - bbcd
 - be
 - deeejed
 - dffee
 - be

Check Strings:
 - 'abcde' -> Rejected
 - 'dde' -> Rejected
 - 'aae' -> Accepted
 - 'ce' -> Rejected
 - 'bdf' -> Rejected
```


We observe the following:

- The program **generates strings** that conform to the grammar's rules. For example, `"bbcd"`, `"be"`, and `"deeejed"` are valid strings derived from the grammar's production rules.
- The finite automaton **correctly identifies whether a string belongs to the language**. For instance:
  - `"aae"` is accepted as a valid string (it can be derived from the grammar).
  - Strings like `"abcde"`, `"dde"`, `"ce"`, and `"bdf"` are rejected since they do not conform to the grammar's rules or the automaton's transitions.

This approach of combining **grammar-based string generation** with **automata-based validation** is useful for applications such as **lexical analysis**, **parsing**, and **compiler construction**, where formal rules are required to generate and validate strings in a language.

## References

_Formal Languages and Finite Automata, Guide for practical lessons_ by COJUHARI Irina, DUCA Ludmila, FIODOROV Ion -
https://else.fcim.utm.md/pluginfile.php/110458/mod_resource/content/0/LFPC_Guide.pdf
