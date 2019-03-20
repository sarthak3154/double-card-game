import math


class MiniMax:

    def __init__(self,root,type):
        self.root_state_node = root
        self.type = type
        self.count = 0

    def maximize(self,state_node):
        maximum_heuristic_value = -math.inf
        if state_node is not None and len(state_node.children) == 0:
            self.count = self.count + 1
            state_node.heuristic_value = state_node.get_data().get_first_informed_heuristic_value(self.type)
            print('x1: ' + str(state_node.data.last_card_placed.first_cell.x) + ' y1: ' + str(state_node.data.last_card_placed.first_cell.y) + ' x2: ' + str(state_node.data.last_card_placed.second_cell.x) + ' y2: ' + str(state_node.data.last_card_placed.second_cell.y) + ' | ' + str(state_node.heuristic_value))
            return state_node.heuristic_value

        for child in state_node.children:
            child.heuristic_value = self.minimize(child)
            maximum_heuristic_value = max(child.heuristic_value,maximum_heuristic_value)
        return maximum_heuristic_value

    def minimize(self,state_node):
        minimum_heuristic_value = math.inf
        if state_node is not None and len(state_node.children) == 0:
            self.count = self.count + 1
            state_node.heuristic_value = state_node.get_data().get_first_informed_heuristic_value(self.type)
            print(state_node.heuristic_value)
            return state_node.heuristic_value

        for child in state_node.children:
            child.heuristic_value = self.maximize(child)
            minimum_heuristic_value = min(child.heuristic_value, minimum_heuristic_value)
        return minimum_heuristic_value

    def minimax_algorithm(self):
        if self.type == "COLOR":
            decision_value = self.maximize(self.root_state_node)
        else:
            decision_value = self.minimize(self.root_state_node)
        self.root_state_node.heuristic_value = decision_value
        print("Decision value: " + str(decision_value))
        children = self.root_state_node.children
        decision_state = [child for child in children if child.heuristic_value == decision_value]
        return decision_state[0]

    def write_nodes_data_to_trace_file(self):
        f = open("tracemm.txt", "a+")
        f.write(str(self.count) + "\n")
        f.write(str(self.root_state_node.heuristic_value) + "\n")
        f.write("\n")
        for child in self.root_state_node.children:
            f.write(str(child.heuristic_value) + "\n")
        f.write("\n")
        f.close()