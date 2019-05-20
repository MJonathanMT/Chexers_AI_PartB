import math
import random
import time


def random_policy(state):
    while not state.is_terminal():
        try:
            action = random.choice(state.legal_actions())
        except IndexError:
            raise Exception(
                "Non-terminal state has no possible actions: " + str(state))
        state = state.next_state(action)
    return state.get_reward()


# def get_reward():
#     current_reward = 0
#     # distance each piece from the goal
#     # formula -> 6 - distance of piece from goal

#     # how many pieces on the board
#     # formula (number of pieces - 4)*2?

#     # how many exits the current player have
#     # formula numb_exits *3

#     # how many pieces stand alone without adjacent pieces
#     # formula number pieces adjacentt - piece not adjacent

#     return current_reward


class treeNode():
    def __init__(self, state, parent):
        self.state = state
        self.is_terminal = state.is_terminal()
        self.is_fully_expanded = self.is_terminal
        self.parent = parent
        self.num_visits = 0
        self.total_reward = 0
        self.children = {}


class mcts():
    # init function still up for changes
    def __init__(self, time_limit=None, exploration_constant=1/math.sqrt(2),
                 roll_out_policy=random_policy):
        """
        init function?
        :param time_limit: time limit of the whole program
        """
        if time_limit is not None:
           # time taken for each MCTS search in milliseconds
            self.time_limit = time_limit
            self.limit_type = 'time'
        self.roll_out = roll_out_policy
        self.exploration_constant = exploration_constant
        self.root = ()

    # main search function

    def search(self, initial_state):
        """
        Main search function for the mct
        :param initial_state: Starting state of the whole game
        :return: Final action of the mct
        """
        # Initial root (None for parent)
        root = treeNode(initial_state, None)
        # 1. implement time? set time maybe idk
        time_limit = time.time() + self.time_limit/1000
        while time.time() < time_limit:
            self.execute_round(root)
        best_child = self.get_best_child(root, 0)
        return self.get_action(root, best_child)

    def execute_round(self, root):
        """
        Not too sure what this does tbh haha
        :param root: Executes from the top of the tree
        """
        node = self.select_node(root)
        # 2. need to implement points system for state in state class
        # 4. idk what roll out is taking alook later, we might need it
        reward = self.roll_out(node.state)

        self.backpropogate(node, reward)

    def select_node(self, node):
        """
        Fcuntion that returns the node with best child
        :param node: The current node
        :return: The current node with the best child
        """
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_child(node, self.exploration_constant)
            else:
                return self.expand(node)
        return node

    @staticmethod
    def get_best_child(node, exploration_value):
        """
        Function to get best child based on exploration/eval function
        :param node: The current node
        :param exploration_value: Value of the node
        :return: One of the best child with the best value
        """
        # Set best value to - infinity and best node to empty
        best_value = float("-inf")
        best_nodes = []

        #
        for child in node.children.values():
            node_value = child.total_reward / child.num_visits + exploration_value * math.sqrt(
                2 * math.log(node.num_visits) / child.num_visits)
            if node_value > best_value:
                best_value = node_value
                best_nodes = [child]
            elif node_value == best_value:
                best_nodes.append(child)
        return random.choice(best_nodes)

    @staticmethod
    def expand(node):
        """
        Function to expand the nodes to all possible expansion
        :param node: The current node
        :return: the new expanded node
        """
        actions = node.state.legal_actions()
        for action in actions:
            if action not in node.children.keys():
                # use zach's take action
                new_node = treeNode(node.state.next_state(action), node)
                node.children[action] = new_node
                if len(actions) == len(node.children):
                    node.is_fully_expanded = True
                return new_node

    @staticmethod
    def backpropogate(node, reward):
        """
        Function to compute gradient descent in respect to weights
        :param node: the current node
        :param reward: value of the node?
        """
        while node is not None:
            node.num_visits += 1
            node.total_reward += reward
            node = node.parent

    @staticmethod
    def get_action(root, best_child):
        for action, node in root.children.items():
            if node is best_child:
                return action
