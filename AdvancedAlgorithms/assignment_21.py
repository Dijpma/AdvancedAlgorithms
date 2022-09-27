from mip import *
from enum import Enum, unique
import numpy as np
import math
import random
from typing import List, Tuple


class ProblemType(Enum):
    MAXIMIZATION = 1
    MINIMIZATION = 2


class VariableSelectionStrategy(Enum):
    LECTURE = 1
    SELF = 2


class NodeInstance:

    def __init__(self, model: Model, lower_bound: float, upper_bound: float):
        self.model = model
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

class Solution:

    def __init__(self, problem_type: ProblemType, selection_strategy: VariableSelectionStrategy):
        self.problem_type = problem_type
        self.selection_strategy = selection_strategy
        self.graph_size = 1

    def branch_and_bound(self, m: Model) -> Tuple[List[int], int]:
        if self.problem_type == ProblemType.MINIMIZATION:
          return self.branch_and_bound_min(m)
        else:
        #   m.optimize()
        #   for v in m.vars:
        #       print(v.lb)
        #   for v in m.constrs:
        #       print(v)
          return self.branch_and_bound_max(m)

    def branch_and_bound_min(self, m: Model):
        start_node = NodeInstance(m, float("-inf"), float("inf"))
        current_problems = [start_node]

        upper_bound_global = float("inf")
        lower_bound_global = float("-inf")

        current_solution = None

        while len(current_problems) > 0:
            #break
            active_problem = current_problems.pop()
            status = active_problem.model.optimize()
            if status == OptimizationStatus.INFEASIBLE:
                continue
            elif status == OptimizationStatus.UNBOUNDED:
                continue
                # prune_infeasibility()  ## continue
            active_problem.lower_bound = math.ceil(active_problem.model.objective_value)
            if self.check_integrality(
                    active_problem.model.vars) and active_problem.model.objective_value < upper_bound_global:
                upper_bound_global = active_problem.model.objective_value
                current_solution = active_problem
                # prune_optimality()
                print("********************************")
                print("Prune Optimal")
                print("********************************")

                continue
            elif active_problem.lower_bound >= upper_bound_global:
                # prune_bound()
                print("********************************")
                print("Prune Bound")
                print("********************************")
                continue
            else:
                # print("********************************")
                # print("Else")
                # print("********************************")
                # var_split = self.variable_selection_method_lecture(active_problem.model.vars)
                # var_split = self.variable_selection_random(active_problem.model.vars)
                var_split = self.variable_selection_method_self(active_problem.model.vars)
                # print("********************************")
                # print(var_split)
                # print("********************************")
                new_model = active_problem.model.copy()
                new_model += var_split >= math.ceil(var_split.x)
                new_node = NodeInstance(new_model, active_problem.lower_bound, active_problem.upper_bound)
                # print("********************************")
                # print("Node 1: ", new_node)
                # print(new_node.lower_bound)
                # print(new_node.upper_bound)
                # print("********************************")


                new_model2 = active_problem.model.copy()
                new_model2 += var_split <= math.floor(var_split.x)
                new_node2 = NodeInstance(new_model2, active_problem.lower_bound, active_problem.upper_bound)
                self.graph_size += 2

                print("Floor:")
                print(math.floor(var_split.x))

                print("Ceil:")
                print(math.ceil(var_split.x))
                # print("********************************")
                # print("Node 2: ", new_node2)
                # print(new_node2.lower_bound)
                # print(new_node2.upper_bound)
                # print("********************************")

                current_problems.append(new_node2)
                current_problems.append(new_node)

        if current_solution is None:
            return ([], float("inf"))
        else:
            result = Solution.build_solution(current_solution)
            print("*****************************")
            print(self.graph_size)
            print("*****************************")
            return result

    def branch_and_bound_max(self, m: Model):
        start_node = NodeInstance(m, float("-inf"), float("inf"))
        current_problems = [start_node]

        upper_bound_global = float("inf")
        lower_bound_global = float("-inf")

        current_solution = None

        while len(current_problems) > 0:
            active_problem = current_problems.pop()
            status = active_problem.model.optimize()

            if status == OptimizationStatus.INFEASIBLE :
                continue
            elif status == OptimizationStatus.UNBOUNDED:
                continue
            # prune_infeasibility()  ## continue

            active_problem.upper_bound = math.floor(active_problem.model.objective_value)
            if self.check_integrality(
                    active_problem.model.vars) and active_problem.model.objective_value > lower_bound_global:
                lower_bound_global = active_problem.model.objective_value
                current_solution = active_problem
            # prune_optimality()
                continue
            elif active_problem.upper_bound <= lower_bound_global:
            # prune_bound()a
                continue
            else:
                # var_split = self.variable_selection_method_lecture(active_problem.model.vars)
                var_split = self.variable_selection_method_self(active_problem.model.vars)

                new_model = active_problem.model.copy()
                new_model += var_split >= math.ceil(var_split.x)
                new_node = NodeInstance(new_model, active_problem.lower_bound, active_problem.upper_bound)

                new_model2 = active_problem.model.copy()
                new_model2 += var_split <= math.floor(var_split.x)
                print("Floor:")
                print(math.floor(var_split.x))
                new_node2 = NodeInstance(new_model2, active_problem.lower_bound, active_problem.upper_bound)

                current_problems.append(new_node)
                current_problems.append(new_node2)
                self.graph_size += 2

        if current_solution is None:
            return ([], float("-inf"))
        else:
            result = Solution.build_solution(current_solution)
            print("*****************************")
            print(self.graph_size)
            print("*****************************")
            return result

    @staticmethod
    def build_solution(cur: NodeInstance) -> Tuple[List[int], int]:
        result_list = []
        for var in cur.model.vars:
            result_list.append(var.x)
        return (result_list, cur.model.objective_value)

    @staticmethod
    def variable_selection_method_lecture(variables: List[mip.Var]) -> mip.Var:
        res = None
        small_diff = 1
        for var in variables:
            curr_diff = abs(var.x - (math.floor(var.x) + 0.5))
            if (curr_diff < small_diff):
                res = var
                small_diff = curr_diff
        return res

    @staticmethod
    def variable_selection_method_self(variables: List[mip.Var]) -> mip.Var:
        res = None
        small_diff = 0
        for var in variables:
            curr_diff = abs(math.floor(var.x)-var.x)
            if (curr_diff > small_diff and (float(1)-curr_diff) <  1e-5):
                res = var
                small_diff = curr_diff
        if small_diff < 1e-5:
            print("********************")
            print("Random Selected")
            res = random.choice(variables)
        print("********************")
        for var in variables:
            print(var.x)
        print(res)
        print(variables[0].x)
        print(variables[0])

        return res

    @staticmethod
    def variable_selection_first_nonint(variables: List[mip.Var]) -> mip.Var:
        pass

    @staticmethod
    def variable_selection_random(variables: List[mip.Var]) -> mip.Var:
        variable = [var for var in variables if not var.x.is_integer]
        if len(variable) == 0:
            return random.choice(variables)
        print(variable)
        return random.choice(variable)


    @staticmethod
    def check_integrality(variables: List[mip.Var]):
        for var in variables:
            if (not var.x.is_integer()):
                return False
        return True

# from mip import *
# from enum import Enum, unique
# import numpy as np
# import math
#
# from typing import List, Tuple
#
# class ProblemType(Enum):
#     MAXIMIZATION = 1
#     MINIMIZATION = 2
#
# class VariableSelectionStrategy(Enum):
#     LECTURE = 1
#     SELF = 2
#
# class Solution:
#
#   def __init__(self, problem_type: ProblemType, selection_strategy: VariableSelectionStrategy):
#     pass
#
#   def branch_and_bound(self, m: Model) -> Tuple[List[int], int]:
#     pass
#
#   def variable_selection_method_lecture(self, variables: List[mip.Var]) -> mip.Var:
#     pass
#
#   def variable_selection_method_self(self, variables: List[mip.Var]) -> mip.Var:
#     pass
# # from mip import *
# # from enum import Enum, unique
# # import numpy as np
# # import math
# #
# # from typing import List, Tuple
# #
# #
# # class ProblemType(Enum):
# #     MAXIMIZATION = 1
# #     MINIMIZATION = 2
# #
# #
# # class VariableSelectionStrategy(Enum):
# #     LECTURE = 1
# #     SELF = 2
# #
# #
# # class NodeInstance:
# #
# #     def __init__(self, model: Model, lower_bound: float, upper_bound: float):
# #         self.model = model
# #         self.lower_bound = lower_bound
# #         self.upper_bound = upper_bound
# #
# # class Solution:
# #
# #     def __init__(self, problem_type: ProblemType, selection_strategy: VariableSelectionStrategy):
# #         self.problem_type = problem_type
# #         self.selection_strategy = selection_strategy
# #
# #     def branch_and_bound(self, m: Model) -> Tuple[List[int], int]:
# #         if self.problem_type == ProblemType.MINIMIZATION:
# #             m.optimize()
# #             for v in m.vars:
# #                 print(v.lb)
# #             for v in m.constrs:
# #                 print(v)
# #             return self.branch_and_bound_min(m)
# #         else:
# #             return self.branch_and_bound_max(m)
# #
# #     def branch_and_bound_min(self, m: Model):
# #         start_node = NodeInstance(m, float("-inf"), float("inf"))
# #         current_problems = [start_node]
# #
# #         upper_bound_global = float("inf")
# #         lower_bound_global = float("-inf")
# #
# #         current_solution = None
# #
# #         while len(current_problems) > 0:
# #             active_problem = current_problems.pop()
# #             status = active_problem.model.optimize(relax=True)
# #             if status == 1:
# #                 continue
# #             elif status == OptimizationStatus.UNBOUNDED:
# #                 return ([], float("inf"))
# #                 # prune_infeasibility()  ## continue
# #             else:
# #
# #                 active_problem.lower_bound = math.ceil(active_problem.model.objective_value)
# #                 if self.check_integrality(
# #                         active_problem.model.vars) and active_problem.model.objective_value < upper_bound_global:
# #                     upper_bound_global = active_problem.model.objective_value
# #                     current_solution = active_problem
# #                     # prune_optimality()
# #                     continue
# #                 elif active_problem.lower_bound >= upper_bound_global:
# #                     # prune_bound()
# #                     continue
# #                 else:
# #                     var_split = self.variable_selection_method_lecture(active_problem.model.vars)
# #
# #                     new_model = active_problem.model.copy()
# #                     new_model += var_split >= math.ceil(var_split.x)
# #                     new_node = NodeInstance(new_model, active_problem.lower_bound, active_problem.upper_bound)
# #
# #                     new_model2 = active_problem.model.copy()
# #                     new_model2 += var_split <= math.floor(var_split.x)
# #                     new_node2 = NodeInstance(new_model2, active_problem.lower_bound, active_problem.upper_bound)
# #
# #                     current_problems.append(new_node)
# #                     current_problems.append(new_node2)
# #
# #         result = Solution.build_solution(current_solution)
# #         return result
# #
# #     def branch_and_bound_max(self, m: Model):
# #         start_node = NodeInstance(m, float("-inf"), float("inf"))
# #         current_problems = [start_node]
# #
# #         upper_bound_global = float("inf")
# #         lower_bound_global = float("-inf")
# #
# #         current_solution = None
# #
# #         while len(current_problems) > 0:
# #             active_problem = current_problems.pop()
# #             status = active_problem.model.optimize(relax=True)
# #             if status == 1:
# #                 continue
# #             elif status == OptimizationStatus.UNBOUNDED:
# #                 return ([], float("-inf"))
# #             # prune_infeasibility()  ## continue
# #
# #             active_problem.upper_bound = math.floor(active_problem.model.objective_value)
# #             if self.check_integrality(
# #                     active_problem.model.vars) and active_problem.model.objective_value > lower_bound_global:
# #                 lower_bound_global = active_problem.model.objective_value
# #                 current_solution = active_problem
# #                 # prune_optimality()
# #                 continue
# #             elif active_problem.upper_bound <= lower_bound_global:
# #                 # prune_bound()a
# #                 continue
# #             else:
# #                 var_split = self.variable_selection_method_lecture(active_problem.model.vars)
# #
# #                 new_model = active_problem.model.copy()
# #                 new_model += var_split >= math.ceil(var_split.x)
# #                 new_node = NodeInstance(new_model, active_problem.lower_bound, active_problem.upper_bound)
# #
# #                 new_model2 = active_problem.model.copy()
# #                 new_model2 += var_split <= math.floor(var_split.x)
# #                 new_node2 = NodeInstance(new_model2, active_problem.lower_bound, active_problem.upper_bound)
# #
# #                 current_problems.append(new_node)
# #                 current_problems.append(new_node2)
# #
# #         result = Solution.build_solution(current_solution)
# #         return result
# #
# #     @staticmethod
# #     def build_solution(cur: NodeInstance) -> Tuple[List[int], int]:
# #         result_list = []
# #         for var in cur.model.vars:
# #             result_list.append(var.x)
# #         return (result_list, cur.model.objective_value)
# #
# #     @staticmethod
# #     def variable_selection_method_lecture(variables: List[mip.Var]) -> mip.Var:
# #         res = None
# #         small_diff = 1
# #         for var in variables:
# #             curr_diff = abs(var.x - (math.floor(var.x) + 0.5))
# #             if (curr_diff < small_diff):
# #                 res = var
# #                 small_diff = curr_diff
# #         return res
# #
# #     @staticmethod
# #     def variable_selection_method_self(variables: List[mip.Var]) -> mip.Var:
# #         res = None
# #         small_diff = 1
# #         for var in variables:
# #             curr_diff = math.abs(var.x - (math.floor(var.x) + 0.5))
# #             if (curr_diff < small_diff):
# #                 res = var
# #                 small_diff = curr_diff
# #         return res
# #
# #     @staticmethod
# #     def check_integrality(variables: List[mip.Var]):
# #         for var in variables:
# #             if (not var.x.is_integer()):
# #                 return False
# #         return True
