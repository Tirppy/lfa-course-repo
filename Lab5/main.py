class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def eliminate_epsilon_productions(self):
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
                    continue
                alternatives = self._generate_alternatives(rule, nullable)
                for alt in alternatives:
                    if not alt:
                        if nt == self.start_symbol:
                            new_rules.add(("ε",))
                        continue
                    new_rules.add(alt)
            new_productions[nt] = [list(prod) for prod in new_rules]
        self.productions = new_productions
        return self

    def _generate_alternatives(self, rule, nullable):
        results = set()
        def helper(index, current):
            if index == len(rule):
                results.add(tuple(current))
            else:
                symbol = rule[index]
                if symbol in nullable:
                    
                    helper(index + 1, current)
                
                helper(index + 1, current + [symbol])
        helper(0, [])
        return results

    def eliminate_unit_productions(self):
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
        cnf_productions = {}
        new_non_terminals = set(self.non_terminals)
        generated = {}   
        count = 0

        for nt, rules in self.productions.items():
            for rule in rules:
                if len(rule) <= 2:
                    cnf_productions.setdefault(nt, []).append(rule)
                else:
                    head, *tail = rule
                    key = tuple(tail)
                    if key in generated:
                        Xprime = generated[key]
                    else:
                        count += 1
                        Xprime = f"X{count}"
                        while Xprime in new_non_terminals:
                            count += 1
                            Xprime = f"X{count}"
                        generated[key] = Xprime
                        new_non_terminals.add(Xprime)

                        curr_nt = Xprime
                        temp = tail
                        while len(temp) > 2:
                            first, *rest = temp
                            sub_key = tuple(rest)
                            if sub_key in generated:
                                next_nt = generated[sub_key]
                            else:
                                count += 1
                                next_nt = f"X{count}"
                                while next_nt in new_non_terminals:
                                    count += 1
                                    next_nt = f"X{count}"
                                generated[sub_key] = next_nt
                                new_non_terminals.add(next_nt)
                            cnf_productions.setdefault(curr_nt, []).append([first, next_nt])
                            curr_nt = next_nt
                            temp = rest
                        cnf_productions.setdefault(curr_nt, []).append(temp)

                    cnf_productions.setdefault(nt, []).append([head, Xprime])

        self.productions = cnf_productions
        self.non_terminals = new_non_terminals
        return self


def format_symbol(symbol):
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

    new_start = "S0"
    while new_start in non_terminals:
        new_start += "0"
    productions[new_start] = [[start_symbol]]
    non_terminals.add(new_start)
    grammar = Grammar(non_terminals, terminals, productions, new_start)
    
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
