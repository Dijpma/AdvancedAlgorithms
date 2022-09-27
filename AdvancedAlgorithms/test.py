import unittest
import create_graph
from unittest import TextTestRunner
from mip import *
import assignment_21 as solution

class Sign(Enum):
    Smaller = 1
    Equals = 2
    Greater = 3


class Mode(Enum):
    Minimization = 1
    Maximization = 2


class TestSolution(unittest.TestCase):

    def run_test_from_file(self, model_sense, file_name, expected_objective_value, epsilon=0.0001):
        m = Model(sense=model_sense)
        m.verbose = 0
        m.read(file_name)

        original = m.copy()  # make copy to check solution

        x = solution.Solution(
            solution.ProblemType.MINIMIZATION if m.sense == "MIN" else solution.ProblemType.MAXIMIZATION,
            solution.VariableSelectionStrategy.LECTURE)

        (best_found, global_bound) = x.branch_and_bound(m)

        self.assertAlmostEqual(expected_objective_value, global_bound, places=4)

        if global_bound != float("inf") and global_bound != float("-inf"):
            for index, var in enumerate(best_found):
                original += original.vars[index] == var
                self.assertTrue(abs(best_found[index] - round(best_found[index])) < epsilon)
            status = original.optimize()

            self.assertEqual(status, OptimizationStatus.OPTIMAL)
            self.assertAlmostEqual(expected_objective_value, original.objective_value, places=4)

    # TEST CASES

    def test_matrix(self):
        self.run_test_from_file(MAXIMIZE, "random.mps", 70)

    def test_knapsack(self):
        self.run_test_from_file(MAXIMIZE, "knapsack_students.mps.gz", 23376)

    def test_g503inf(self):
        self.run_test_from_file(MINIMIZE, "g503inf.mps.gz", float("inf"))

    def test_graph_color(self):
        self.run_test_from_file(MINIMIZE, "graph_color_int.lp", 4)


if __name__ == '__main__':
    unittest.main(testRunner=TextTestRunner)
# import unittest
# import solution
# from weblabTestRunner import TestRunner
# from mip import *
#
# class Sign(Enum):
#     Smaller = 1
#     Equals = 2
#     Greater = 3
#
# class Mode(Enum):
#     Minimization = 1
#     Maximization = 2
#
# class TestSolution(unittest.TestCase):
#
#   def run_test_from_file(self, model_sense, file_name, expected_objective_value, epsilon=0.0001):
#     m = Model(sense=model_sense)
#     m.verbose = 0
#     m.read(file_name)
#
#     original = m.copy() # make copy to check solution
#
#     x = solution.Solution(
#         solution.ProblemType.MINIMIZATION if m.sense == "MIN" else solution.ProblemType.MAXIMIZATION,
#         solution.VariableSelectionStrategy.LECTURE)
#
#     (best_found, global_bound) = x.branch_and_bound(m)
#
#     self.assertAlmostEqual(expected_objective_value, global_bound, places=4)
#
#     if global_bound != float("inf") and global_bound != float("-inf"):
#       for index, var in enumerate(best_found):
#         original += original.vars[index] == var
#         self.assertTrue(abs(best_found[index] - round(best_found[index])) < epsilon)
#       status = original.optimize()
#
#       self.assertEqual(status, OptimizationStatus.OPTIMAL)
#       self.assertAlmostEqual(expected_objective_value, original.objective_value, places=4)
#
# # TEST CASES
#
#   def test_matrix(self):
#     self.run_test_from_file(MAXIMIZE, "random.mps", 70)
#
#   def test_knapsack(self):
#     self.run_test_from_file(MAXIMIZE, "knapsack_students.mps.gz", 23376)
#
#   def test_g503inf(self):
#     self.run_test_from_file(MINIMIZE, "g503inf.mps.gz", float("inf"))
#
#
#
# if __name__ == '__main__':
#     unittest.main(testRunner=TestRunner)
# # import unittest
# # import solution
# # from weblabTestRunner import TestRunner
# # from mip import *
# #
# # class Sign(Enum):
# #     Smaller = 1
# #     Equals = 2
# #     Greater = 3
# #
# # class Mode(Enum):
# #     Minimization = 1
# #     Maximization = 2
# #
# # class TestSolution(unittest.TestCase):
# #
# #   def run_test_from_file(self, model_sense, file_name, expected_objective_value, epsilon=0.0001):
# #     m = Model(sense=model_sense)
# #     m.verbose = 0
# #     m.read(file_name)
# #
# #     original = m.copy() # make copy to check solution
# #
# #     x = solution.Solution(
# #         solution.ProblemType.MINIMIZATION if m.sense == "MIN" else solution.ProblemType.MAXIMIZATION,
# #         solution.VariableSelectionStrategy.LECTURE)
# #
# #     result = x.branch_and_bound(m)
# #
# #     (best_found, global_bound) = result
# #
# #     self.assertAlmostEqual(expected_objective_value, global_bound, places=4)
# #
# #     if global_bound != float("inf") and global_bound != float("-inf"):
# #       for index, var in enumerate(best_found):
# #         original += original.vars[index] == var
# #         self.assertTrue(abs(best_found[index] - round(best_found[index])) < epsilon)
# #       status = original.optimize()
# #
# #       self.assertEqual(status, OptimizationStatus.OPTIMAL)
# #       self.assertAlmostEqual(expected_objective_value, original.objective_value, places=4)
# #
# # # TEST CASES
# #
# #   def test_matrix(self):
# #     self.run_test_from_file(MINIMIZE, "random.mps", 40)
# #
# #   # def test_knapsack(self):
# #   #   self.run_test_from_file(MAXIMIZE, "knapsack_students.mps.gz", 23376)
# #
# #   # def test_g503inf(self):
# #   #   self.run_test_from_file(MINIMIZE, "g503inf.mps.gz", float("inf"))
# #
# #
# #
# # if __name__ == '__main__':
# #     unittest.main(testRunner=TestRunner)
