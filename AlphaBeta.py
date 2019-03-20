import math


class AlphaBeta:

    def __init__(self,root,type):
        self.root_state_node = root
        self.type = type
        self.count = 0

    def maximize(self,state_node, depth,a, b):
        maximum_heuristic_value = -math.inf
        if depth is 0 or (state_node is not None and len(state_node.children) == 0):
            self.count = self.count + 1
            state_node.heuristic_value = state_node.get_data().get_first_informed_heuristic_value(state_node.parent.data.last_card_placed,self.type)
            # print('x1: ' + str(state_node.data.last_card_placed.first_cell.x) + ' y1: ' + str(state_node.data.last_card_placed.first_cell.y) + ' x2: ' + str(state_node.data.last_card_placed.second_cell.x) + ' y2: ' + str(state_node.data.last_card_placed.second_cell.y) + ' | ' + str(state_node.heuristic_value))
            return state_node.heuristic_value

        for child in state_node.children:
            child.heuristic_value = self.minimize(child, depth-1, a, b)
            maximum_heuristic_value = max(child.heuristic_value, maximum_heuristic_value)
            if maximum_heuristic_value >= b:
                return maximum_heuristic_value
            a = max(maximum_heuristic_value, a)
        return maximum_heuristic_value

    def minimize(self,state_node, depth, a, b):
        minimum_heuristic_value = math.inf
        if depth is 0 or (state_node is not None and len(state_node.children) == 0):
            self.count = self.count + 1
            state_node.heuristic_value = state_node.get_data().get_first_informed_heuristic_value(state_node.parent.data.last_card_placed,self.type)
            # print('x1: ' + str(state_node.data.last_card_placed.first_cell.x) + ' y1: ' + str(state_node.data.last_card_placed.first_cell.y) + ' x2: ' + str(state_node.data.last_card_placed.second_cell.x) + ' y2: ' + str(state_node.data.last_card_placed.second_cell.y) + ' | ' + str(state_node.heuristic_value))
            return state_node.heuristic_value

        for child in state_node.children:
            child.heuristic_value = self.maximize(child, depth-1, a, b)
            minimum_heuristic_value = min(child.heuristic_value, minimum_heuristic_value)
            if a >= minimum_heuristic_value:
                return minimum_heuristic_value
            b = min(minimum_heuristic_value, b)
        return minimum_heuristic_value

    def alpha_beta_algorithm(self, depth):

        a = -math.inf
        b = math.inf

        if depth is 0:
            return self.root_state_node

        if self.type == 'COLOR':
            decision_value = -math.inf
            for child in self.root_state_node.children:
                child.heuristic_value = self.minimize(child, depth-1, a, b)
                if child.heuristic_value > decision_value:
                    decision_value = child.heuristic_value
                    decision_state = child
                a = max(decision_value,a)

        else:
            decision_value = math.inf
            for child in self.root_state_node.children:
                child.heuristic_value = self.maximize(child, depth -1, a, b)
                if child.heuristic_value < decision_value:
                    decision_value = child.heuristic_value
                    decision_state = child
                b = min(decision_value,b)

        self.root_state_node.heuristic_value = decision_value
        # print('Decison value:' + str(decision_value))
        return decision_state

    def write_nodes_data_to_trace_file(self):
        f = open("tracemm.txt", "a+")
        f.write(str(self.count) + "\n")
        f.write(str(self.root_state_node.heuristic_value) + "\n")
        f.write("\n")
        for child in self.root_state_node.children:
            # if child.heuristic_value is not None:
            f.write(str(child.heuristic_value) + "\n")
        f.write("\n")
        f.close()