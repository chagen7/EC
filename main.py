import sys
import re
from itertools import combinations

def powerset(states):
    for r in range(len(states) + 1):
        for subset in combinations(states, r):
            yield list(subset)

def epsilon_closure(state, transitions):
    closure = set([state])
    stack = [state]
    while stack:
        current_state = stack.pop()
        for transition in transitions:
            if transition[0] == current_state and transition[1] == 'EPS':
                next_state = transition[2]
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return list(closure)

def move(states, symbol, transitions):
    result = []
    for state in states:
        for transition in transitions:
            if transition[0] == state and transition[1] == symbol:
                result.append(transition[2])
    return result

def nfa_to_dfa(states, alphabet, start_state, accept_states, transitions):
    # Compute epsilon closures for all states, including EM
    epsilon_closures = {state: epsilon_closure(state, transitions) for state in states}

    # Initialize DFA states and transitions
    dfa_states = list(powerset(states))

    dfa_accept_states = []
    all_transitions = []
    dfa_transitions = []

    # Process each DFA state
    dfa_state_mapping = []

    for dfa_state in dfa_states:
        for symbol in alphabet:
            next_state_set = []
            for nfa_state in dfa_state:
                next_state_set.extend(epsilon_closure(next_state, transitions) for next_state in move([nfa_state], symbol, transitions))
            next_state_set = sorted(list(set().union(*next_state_set)))
            if next_state_set:
                all_transitions.append((dfa_state, symbol, next_state_set))
                if next_state_set not in dfa_state_mapping:
                    dfa_state_mapping.append(next_state_set)

    dfa_start_state = sorted(epsilon_closure(start_state, transitions))

    for accept in accept_states:
        for states in dfa_state_mapping:
            for state in states:
                if accept in state:
                    dfa_accept_states.append(states)

    # Generate DFA specification
    dfa_spec = f"{', '.join(str(i) for i in dfa_state_mapping)}\n"
    dfa_spec += f"{', '.join(alphabet)}\n"
    dfa_spec += f"{dfa_start_state}\n"
    dfa_spec += f"{', '.join(str(state) for state in dfa_accept_states)}\n"
    dfa_spec += "BEGIN\n"

    for transition in all_transitions:
        if transition[0] in dfa_state_mapping:
            dfa_transitions.append(transition)

    for transition in dfa_transitions:
        dfa_spec += f"{transition[0]}, {transition[1]} = {transition[2]}\n"
    dfa_spec += "END"

    dfa_spec = re.sub("'", "", dfa_spec)

    return dfa_spec

def parse_nfa_file(file_path):
    with open(file_path, 'r') as file:
        nfa_spec = file.read()
    lines = nfa_spec.split('\n')
    states = [state.strip('{}') for state in lines[0].split('\t')]
    print(states)
    alphabet = lines[1].split('\t')
    print(alphabet)
    start_state = lines[2].strip('{}')
    print(start_state)
    accept_states = [state.strip('{}') if state != '{EM}' else 'EM' for state in lines[3].split('\t')]
    print(accept_states)
    transitions = []
    for line in lines[5:]:
        if line == 'END':
            break
        parts = re.split(', | = ', line)
        if len(parts) == 3:
            s, x, sf = [part.strip('{}') for part in parts]
            transitions.append((s, x, sf))

    return states, alphabet, start_state, accept_states, transitions

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <nfa_file>")
        sys.exit(1)

    nfa_file_path = sys.argv[1]

    try:
        states, alphabet, start_state, accept_states, transitions = parse_nfa_file(nfa_file_path)
        dfa_spec = nfa_to_dfa(states, alphabet, start_state, accept_states, transitions)

        with open('output.DFA', 'w') as output_file:
            output_file.write(dfa_spec)

        print(f"Equivalent DFA specification written to 'output.DFA'")
    except FileNotFoundError:
        print(f"Error: File '{nfa_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

