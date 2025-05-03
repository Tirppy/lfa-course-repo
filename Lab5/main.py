class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        """
        non_terminals: set of non-terminal symbols (VN)
        terminals: set of terminal symbols (VT)
        productions: dictionary mapping each non-terminal to a list of productions,
                     where each production is represented as a list of symbols.
        start_symbol: the starting symbol of the grammar.
        """
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def eliminate_epsilon_productions(self):
        """
        Step 1: Eliminate ε-productions.
        This method first determines all nullable non-terminals (ones that can derive ε).
        Then for each production, it generates alternatives by optionally omitting nullable symbols.
        For the start symbol, if an alternative is empty, it is replaced with ["ε"].
        For non-start symbols, empty alternatives are omitted.
        """
        nullable = set()
        changed = True
        while changed:
            changed = False
            for nt, rules in self.productions.items():
                if nt not in nullable:
                    for rule in rules:
                        if rule == ["ε"] or all(symbol in nullable for symbol in rule):
                            nullable.add(nt)
                            changed = True
                            break

        new_productions = {}
        for nt, rules in self.productions.items():
            new_rules = set()
            for rule in rules:
                if rule == ["ε"]:
                    continue  # Skip the original ε-production.
                alternatives = self._generate_alternatives(rule, nullable)
                for alt in alternatives:
                    # For non-start symbols, skip empty alternatives.
                    # For the start symbol, replace an empty alternative with ["ε"].
                    if not alt:
                        if nt == self.start_symbol:
                            new_rules.add(("ε",))
                        continue
                    new_rules.add(alt)
            new_productions[nt] = [list(prod) for prod in new_rules]
        self.productions = new_productions
        return self

    def _generate_alternatives(self, rule, nullable):
        """
        Recursively generate all alternatives for a production rule by
        optionally omitting nullable non-terminals.
        :param rule: A list of symbols for a production.
        :param nullable: A set of nullable non-terminals.
        :return: A set of tuples, each tuple is one variant of the production.
        """
        results = set()
        def helper(index, current):
            if index == len(rule):
                results.add(tuple(current))
            else:
                symbol = rule[index]
                if symbol in nullable:
                    # Option to omit the symbol.
                    helper(index + 1, current)
                # Always include the symbol.
                helper(index + 1, current + [symbol])
        helper(0, [])
        return results

    def eliminate_unit_productions(self):
        """
        Step 2: Eliminate renaming (unit) productions.
        For each non-terminal A, the method computes the set of non-terminals that
        are reachable through unit productions and then adds all non-unit productions
        from those non-terminals, explicitly skipping any ε-productions.
        """
        unit_pairs = {nt: set() for nt in self.non_terminals}
        for nt in self.non_terminals:
            unit_pairs[nt].add(nt)
            changed = True
            while changed:
                changed = False
                for A in list(unit_pairs[nt]):
                    for rule in self.productions.get(A, []):
                        if len(rule) == 1 and rule[0] in self.non_terminals:
                            if rule[0] not in unit_pairs[nt]:
                                unit_pairs[nt].add(rule[0])
                                changed = True

        new_productions = {}
        for nt in self.non_terminals:
            new_rules = set()
            for B in unit_pairs[nt]:
                for rule in self.productions.get(B, []):
                    if rule == ["ε"]:
                        continue
                    if len(rule) == 1 and rule[0] in self.non_terminals:
                        continue
                    new_rules.add(tuple(rule))
            new_productions[nt] = [list(rule) for rule in new_rules]
        self.productions = new_productions
        return self

    def eliminate_inaccessible_symbols(self):
        """
        Step 3: Eliminate inaccessible symbols.
        Starting from the start symbol, this method finds all reachable non-terminals 
        and terminals, then removes productions that are not reachable.
        """
        reachable_nts = set()
        to_process = {self.start_symbol}
        while to_process:
            current = to_process.pop()
            reachable_nts.add(current)
            for prod in self.productions.get(current, []):
                for symbol in prod:
                    if symbol in self.non_terminals and symbol not in reachable_nts:
                        to_process.add(symbol)
        new_productions = {nt: self.productions[nt] for nt in reachable_nts if nt in self.productions}
        self.productions = new_productions
        self.non_terminals = self.non_terminals.intersection(reachable_nts)
        reachable_terminals = set()
        for rules in self.productions.values():
            for rule in rules:
                for symbol in rule:
                    if symbol in self.terminals:
                        reachable_terminals.add(symbol)
        self.terminals = reachable_terminals
        return self

    def eliminate_non_productive_symbols(self):
        """
        Step 4: Eliminate non-productive symbols.
        A symbol is productive if it can derive a string consisting solely of terminals.
        This method computes the set of productive non-terminals and removes any
        productions (and non-terminals) that include non-productive symbols.
        """
        productive = set()
        changed = True
        while changed:
            changed = False
            for nt, rules in self.productions.items():
                if nt not in productive:
                    for rule in rules:
                        if all(symbol in self.terminals or symbol in productive or symbol == "ε" for symbol in rule):
                            productive.add(nt)
                            changed = True
                            break
        new_productions = {}
        for nt, rules in self.productions.items():
            if nt in productive:
                valid_rules = []
                for rule in rules:
                    if all(symbol in self.terminals or symbol in productive or symbol == "ε" for symbol in rule):
                        valid_rules.append(rule)
                if valid_rules:
                    new_productions[nt] = valid_rules
        self.productions = new_productions
        self.non_terminals = self.non_terminals.intersection(productive)
        new_terminals = set()
        for rules in self.productions.values():
            for rule in rules:
                for symbol in rule:
                    if symbol in self.terminals:
                        new_terminals.add(symbol)
        self.terminals = new_terminals
        return self

    def convert_to_cnf(self):
        """
        Step 5: Convert the grammar into Chomsky Normal Form (CNF).
        This involves two parts:
          A. For productions with length >= 2, replace any terminal symbols by new non-terminals.
          B. For productions with more than two symbols, break them into binary productions.
        """
        # Part A: Replace terminals in rules of length >= 2.
        terminal_mapping = {}  # maps terminal -> new non-terminal representing it
        new_prod = {}
        for nt, rules in self.productions.items():
            new_rules = []
            for rule in rules:
                if len(rule) >= 2:
                    new_rule = []
                    for symbol in rule:
                        if symbol in self.terminals:
                            if symbol not in terminal_mapping:
                                new_nt = f"T_{symbol}"
                                while new_nt in self.non_terminals:
                                    new_nt += "_"
                                terminal_mapping[symbol] = new_nt
                                self.non_terminals.add(new_nt)
                                new_prod.setdefault(new_nt, []).append([symbol])
                            new_rule.append(terminal_mapping[symbol])
                        else:
                            new_rule.append(symbol)
                    new_rules.append(new_rule)
                else:
                    new_rules.append(rule)
            new_prod.setdefault(nt, []).extend(new_rules)
        self.productions = new_prod

        # Part B: Convert productions with more than 2 symbols into binary rules.
        cnf_productions = {}
        new_non_terminals = set(self.non_terminals)
        count = 0
        for nt, rules in self.productions.items():
            for rule in rules:
                if len(rule) <= 2:
                    cnf_productions.setdefault(nt, []).append(rule)
                else:
                    # For a rule A -> X1 X2 ... Xn (n > 2), introduce new non-terminals.
                    current = rule[0]
                    tail = rule[1:]
                    count += 1
                    new_nt = f"X{count}"
                    new_non_terminals.add(new_nt)
                    cnf_productions.setdefault(nt, []).append([current, new_nt])
                    temp_rule = tail
                    current_nt = new_nt
                    while len(temp_rule) > 2:
                        count += 1
                        next_nt = f"X{count}"
                        new_non_terminals.add(next_nt)
                        cnf_productions.setdefault(current_nt, []).append([temp_rule[0], next_nt])
                        current_nt = next_nt
                        temp_rule = temp_rule[1:]
                    cnf_productions.setdefault(current_nt, []).append(temp_rule)
        self.productions = cnf_productions
        self.non_terminals = new_non_terminals
        return self


def format_symbol(symbol):
    """
    Format a symbol for printing. If the symbol corresponds to a terminal
    replacement (starts with 'T_'), return the terminal itself.
    Otherwise, return the symbol unchanged.
    """
    if symbol.startswith("T_"):
        return symbol[2:]
    return symbol


def main():
    non_terminals = {"S", "A", "B", "C", "D"}
    terminals = {"a", "b"}
    productions = {
        "S": [["a", "B"], ["b", "A"], ["A"]],
        "A": [["B"], ["A", "S"], ["a", "B", "A", "B"], ["b"]],
        "B": [["b"], ["b", "S"], ["a", "D"], ["ε"]],
        "D": [["A", "A"]],
        "C": [["B", "a"]]
    }
    start_symbol = "S"

    grammar = Grammar(non_terminals, terminals, productions, start_symbol)
    
    grammar.eliminate_epsilon_productions() \
           .eliminate_unit_productions() \
           .eliminate_inaccessible_symbols() \
           .eliminate_non_productive_symbols() \
           .convert_to_cnf()
    
    print("Grammar in Chomsky Normal Form:")
    for nt, rules in grammar.productions.items():
        rules_str = " | ".join("".join(format_symbol(sym) for sym in rule) for rule in rules)
        print(f"{nt} -> {rules_str}")


if __name__ == "__main__":
    main()
