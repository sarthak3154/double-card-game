import math


class AlphaBeta:

    def __init__(self,root,type):
        self.root_state_node = root
        self.type = type

    def maximize(self,state_node, a, b):
        maximum_heuristic_value = -math.inf
        if state_node is not None and len(state_node.children) == 0:
            return state_node.heuristic_value

        for child in state_node.children:
            maximum_heuristic_value = max(self.minimize(child, a, b), maximum_heuristic_value)
            a = max(maximum_heuristic_value, a)
            if a >= b:
                break
        child.heuristic_value = maximum_heuristic_value
        return maximum_heuristic_value

    def minimize(self,state_node, a, b):
        minimum_heuristic_value = math.inf
        if state_node is not None and len(state_node.children) == 0:
            return state_node.heuristic_value

        for child in state_node.children:
            minimum_heuristic_value = min(self.maximize(child, a, b), minimum_heuristic_value)
            b = min(minimum_heuristic_value, b)
            if a >= b:
                break
        child.heuristic_value = minimum_heuristic_value
        return minimum_heuristic_value

    def alpha_beta_algorithm(self):
        a = -math.inf
        b = math.inf

        if self.type is "COLOR":
            decision_value = self.maximize(self.root_state_node, a, b)
        else:
            decision_value = self.minimize(self.root_state_node, a, b)
        children = self.root_state_node.children
        decision_state = [child for child in children if child.heuristic_value == decision_value]
        return decision_state[0]

    def write_nodes_data_to_trace_file(self):
        f = open("tracemm.txt", "a+")
        f.write(str(self.root_state_node.heuristic_value) + "\n")
        f.write("\n")
        for child in self.root_state_node.children:
            f.write(str(child.heuristic_value) + "\n")
        f.write("\n")
        f.close()