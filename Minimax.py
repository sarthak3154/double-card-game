import math


class MiniMax:

    def __int__(self,root_state_node):
        self.root_state_node = root_state_node

    def maximize(self,state_node):
        maximum_heuristic_value = - math.inf
        if state_node is not None and len(state_node.children) == 0:
            return state_node.get_heuristic_value()

        children = state_node.children
        for child in children:
            maximum_heuristic_value = math.max(self.minimize(child),maximum_heuristic_value)

        return maximum_heuristic_value

    def minimize(self,state_node):
        minimum_heuristic_value = math.inf
        if state_node is not None and len(state_node.children) == 0:
            return state_node.heuristic_value
        children = state_node.get_children()
        for child in children:
            minimum_heuristic_value = math.min(self.maximize(child), minimum_heuristic_value)

        return minimum_heuristic_value

    def minimax_algorithm(self, root_state_node):
        decision_value = self.maximize(root_state_node)
        children = root_state_node.children
        decision_state = filter(lambda child: child.heuristic_value == decision_value, children)
        #decision_state = [child for child in children if child.heuristic_value == decision_value]
        return decision_state[0]