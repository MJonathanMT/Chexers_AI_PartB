import math
import random
import time

class treeNode():
    def __init__(self, state, parent):
        self.state = state
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = self.isTerminal
        self.parent = parent
        self.children = {}

class mcts():
    # init function still up for changes
    def __init__(self, time_limit=None):
        """
        init function?
        :param time_limit: time limit of the whole program
        """
                 # , rolloutPolicy=randomPolicy):
        if time_limit != None:
           # time taken for each MCTS search in milliseconds
            self.timeLimit = time_limit
            self.limitType = 'time'
        # self.rollout = rolloutPolicy
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
        time_limit = time.time() + self.timeLimit/1000
        while time.time() < time_limit:
            self.execute_round(root)
        best_child = self.get_best_child(root, 0)
        return self.getAction(self.root, best_child)

    def execute_round(self, root):
        """
        Not too sure what this does tbh haha
        :param root: Executes from the top of the tree
        """
        node = self.select_node(root)
        # 2. need to implement points system for state in state class
        # 4. idk what roll out is taking alook later, we might need it
        reward = self.rollout(node.state)

        self.backpropogate(node, reward)

    def select_node(self, node):
        """
        Fcuntion that returns the node with best child
        :param node: The current node
        :return: The current node with the best child
        """
        while not node.isTerminal:
            if node.isFullyExpanded:
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
            # 3. Formula can be changed
            node_value = child.totalReward / child.numVisits + exploration_value * math.sqrt(
                2 * math.log(node.numVisits) / child.numVisits)
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
        actions = node.state.getPossibleAction()
        for action in actions:
            if action not in node.child.keys():
                # use zach's take action
                new_node = treeNode(node.state.takeAction(action), node)
                node.children[action] = new_node
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return new_node

    @staticmethod
    def backpropogate(node, reward):
        """
        Function to compute gradient descent in respect to weights
        :param node: the current node
        :param reward: value of the node?
        """
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent