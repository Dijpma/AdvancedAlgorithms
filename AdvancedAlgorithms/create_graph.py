from mip import *
# m = Model(sense=model_sense)
# m.verbose = 0
# m.read(file_name)
# m.write("model.mps")
from assignment_21 import Solution


class Graph():
    def __init__(self, graph_string):
        self.graph_edges = None
        self.amount_of_nodes = None
        self.amount_of_edges = None
        self.txt = graph_string

    def parse_graph(self):
        input = [[eval(x) for x in edge.split()] for edge in self.txt.split("\n")]
        self.amount_of_nodes = input[0][0]
        self.amount_of_edges = input[0][1]
        self.graph_edges = input[1:]


def integer_model(graph, relaxation=False):
    """Returns the minimum number of colours using the linear relaxation of the integer model"""

    # Create a model
    m = Model()

    # Do not output solver statistics
    m.verbose = 0

    ########
    # TODO #
    ########
    model_graph = Graph(graph)
    model_graph.parse_graph()
    vertices = model_graph.amount_of_nodes
    big_number = vertices

    ##Decision Variables
    ##Setting the var_type to binary and using bounds already apply Constraints (4) and (5)
    x_v = [m.add_var(name="x", var_type=INTEGER, lb=1, ub=vertices) for i in range(vertices)]
    z = m.add_var(name="z", var_type=INTEGER, lb=1, ub=vertices)
    a = [m.add_var(name="a", var_type=BINARY) for i in range(model_graph.amount_of_edges)]

    ##Constraints
    ##(1)
    for i in range(vertices):
        m += x_v[i] - z <= 0

    ##(2) and (3)
    for i in range(model_graph.amount_of_edges):
        m += x_v[model_graph.graph_edges[i][0]] - x_v[model_graph.graph_edges[i][1]] + big_number * a[i] >= 1  # (2)
        m += x_v[model_graph.graph_edges[i][0]] - x_v[model_graph.graph_edges[i][1]] + big_number * a[
            i] <= big_number - 1  # (3)

    ## Objective Function
    m.objective = minimize(z)

    # Solve the model and return the objective value
    m.optimize(relax=relaxation)

    m.write("graph_color_int.lp")


graph = "".join(open("n20.in").readlines())
integer_model(graph, True)

