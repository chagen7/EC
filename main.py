# import sys
# import re

# def powerset(states):
#     yield [] # first return the result we’re sure about 
#     for i in range(len(states)):
#         for x in powerset(states[i+1:]): 
#             # induction part 
#             yield [states[i]] + x 
#     # result = ["EM"]
#     # for i in range(2**len(states)):
#     #     result.append(tuple(states[j] for j in range(len(states)) if (i & (2**j)) > 0))
#     #     print(result)
#     # return result

# def epsilon_closure(state, transitions):
#     closure = set([state])
#     stack = [state]
#     while stack:
#         current_state = stack.pop()
#         for transition in transitions:
#             if transition[0] == current_state and transition[1] == 'EPS':
#                 next_state = transition[2]
#                 if next_state not in closure:
#                     closure.add(next_state)
#                     stack.append(next_state)
#     return closure

# def move(states, symbol, transitions):
#     result = set()
#     for state in states:
#         print("State: ", state)
#         print("Symbol: ", symbol)
#         for transition in transitions:
#             print("Transition: ", transition)
#             if transition[0] == state and transition[1] == symbol:
#                 result.add(transition[2])
#                 print("State Added: ", transition[2])
#                 print("CURR RESULT: ", result)
#     return result

# def nfa_to_dfa(states, alphabet, start_state, accept_states, transitions):
#     # Compute epsilon closures for all states, including EM
#     epsilon_closures = {state: epsilon_closure(state, transitions) for state in states}

#     # Initialize DFA states and transitions
#     dfa_states = []
#     for x in powerset(states):
#         dfa_states.append(x)
#     print(dfa_states)
#     dfa_transitions = []

#     # Process each DFA state
#     for dfa_state in dfa_states:
#         for symbol in alphabet:
#             next_state_set = set()
#             for nfa_state in dfa_state:
#                 print("NFA State: ", nfa_state)
#                 print("DFA State: ", dfa_state)
#                 next_state_set.update(epsilon_closure(next_state, transitions) for next_state in move([nfa_state], symbol, transitions))
#                 print("break here???")
#             print("break here?")
#             next_state_set = frozenset().union(next_state_set)
#             if next_state_set:
#                 dfa_transitions.append((tuple(dfa_state), symbol, tuple(next_state_set)))
#                 if tuple(next_state_set) not in dfa_states:
#                     dfa_states.append(tuple(next_state_set))

#     dfa_states = frozenset().union(dfa_states)
#     # Map DFA states to new names
#     dfa_state_mapping = {tuple(states): f'{{{", ".join(map(str, states))}}}' for states in dfa_states}

#     # Generate DFA specification
#     dfa_spec = f"{', '.join(dfa_state_mapping[tuple(states)] for states in dfa_states)}\n"
#     dfa_spec += f"{', '.join(alphabet)}\n"
#     dfa_spec += f"{dfa_state_mapping[tuple([start_state])]}\n"
#     dfa_spec += f"{', '.join(dfa_state_mapping[tuple(accept)] for accept in accept_states)}\n"
#     dfa_spec += "BEGIN\n"
#     for transition in dfa_transitions:
#         dfa_spec += f"{dfa_state_mapping[transition[0]]}, {transition[1]} = {dfa_state_mapping[transition[2]]}\n"
#     dfa_spec += "END"

#     return dfa_spec

# def parse_nfa_file(file_path):
#     with open(file_path, 'r') as file:
#         nfa_spec = file.read()
#     lines = nfa_spec.split('\n')
#     states = [state.strip('{}') for state in lines[0].split('\t')]
#     print(states)
#     alphabet = lines[1].split('\t')
#     print("Alphabet:")
#     print(alphabet)
#     start_state = lines[2].strip('{}')
#     print("Start State:")
#     print(start_state)
#     accept_states = [state.strip('{}') if state != '{EM}' else 'EM' for state in lines[3].split('\t')]
#     print("Accept States:")
#     print(accept_states)
#     transitions = []
#     for line in lines[5:]:
#         if line == 'END':
#             break
#         parts = re.split(', | = ', line)
#         if len(parts) == 3:
#             s, x, sf = [part.strip('{}') for part in parts]
#             transitions.append((s, x, sf))

#     for transition in transitions:
#         print("Transition:")
#         print(transition)
    
#     return states, alphabet, start_state, accept_states, transitions

# def main():
#     if len(sys.argv) != 2:
#         print("Usage: python script.py <nfa_file>")
#         sys.exit(1)

#     nfa_file_path = sys.argv[1]
    
#     try:
#         states, alphabet, start_state, accept_states, transitions = parse_nfa_file(nfa_file_path)
#         dfa_spec = nfa_to_dfa(states, alphabet, start_state, accept_states, transitions)

#         with open('output.DFA', 'w') as output_file:
#             output_file.write(dfa_spec)

#         print(f"Equivalent DFA specification written to 'output.DFA'")
#     except FileNotFoundError:
#         print(f"Error: File '{nfa_file_path}' not found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()

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
    dfa_transitions = []

    # Process each DFA state
    dfa_state_mapping = []

    for dfa_state in dfa_states:
        for symbol in alphabet:
            next_state_set = []
            for nfa_state in dfa_state:
                print("NFA State: ", nfa_state)
                print("DFA State: ", dfa_state)
                next_state_set.extend(epsilon_closure(next_state, transitions) for next_state in move([nfa_state], symbol, transitions))
            next_state_set = list(set().union(*next_state_set))
            if next_state_set:
                dfa_transitions.append((dfa_state, symbol, next_state_set))
                if next_state_set not in dfa_state_mapping:
                    dfa_state_mapping.append(next_state_set)
                    print("MAPPING: ", dfa_state_mapping)

    dfa_start_state = epsilon_closure(start_state, transitions)
    # Generate DFA specification
    dfa_spec = f"{', '.join(str(i) for i in range(len(dfa_state_mapping)))}\n"
    dfa_spec += f"{', '.join(alphabet)}\n"
    print("DFA Mapping: "), dfa_state_mapping
    dfa_spec += f"{dfa_state_mapping.index([dfa_start_state])}\n"
    dfa_spec += f"{', '.join(str(dfa_state_mapping.index(accept)) for accept in accept_states)}\n"
    dfa_spec += "BEGIN\n"
    for transition in dfa_transitions:
        dfa_spec += f"{dfa_state_mapping.index(transition[0])}, {transition[1]} = {dfa_state_mapping.index(transition[2])}\n"
    dfa_spec += "END"

    return dfa_spec

def parse_nfa_file(file_path):
    with open(file_path, 'r') as file:
        nfa_spec = file.read()
    lines = nfa_spec.split('\n')
    states = [state.strip('{}') for state in lines[0].split('\t')]
    print(states)
    alphabet = lines[1].split('\t')
    print("Alphabet:")
    print(alphabet)
    start_state = lines[2].strip('{}')
    print("Start State:")
    print(start_state)
    accept_states = [state.strip('{}') if state != '{EM}' else 'EM' for state in lines[3].split('\t')]
    print("Accept States:")
    print(accept_states)
    transitions = []
    for line in lines[5:]:
        if line == 'END':
            break
        parts = re.split(', | = ', line)
        if len(parts) == 3:
            s, x, sf = [part.strip('{}') for part in parts]
            transitions.append((s, x, sf))

    for transition in transitions:
        print("Transition:")
        print(transition)

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

