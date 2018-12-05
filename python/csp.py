FAILURE = 'FAILURE'
import pprint

def solve(csp):
    """
  csp is an object that should have properties:

    variables:  
      dictionary of variables and values they can take on

    constraints:
      list of constraints where each element is a tuple of 
      (head node, tail node, constraint function)
 """
    result = backtrack({}, csp['variables'], csp)
    if result == FAILURE: return result
    return {k: v[0] for k, v in result.items()}  # Unpack values wrapped in arrays.

#make formalisation work on all
# add degree heuristic
# make lcv mrv optional
# interface

def ac3(assignments, unassigned, csp):
    def remove_inconsistent_values(head, tail, constraint, assignments):
        valid_tail_values = [t for t in assignments[tail] if any((constraint(h, t) for h in assignments[head]))]
        assignments[tail] = valid_tail_values

    queue = csp['constraints'][:]
    assignments = all_remaining_assignments(assignments, unassigned)

    while len(queue):
        head, tail, constraint = queue.pop(0)
        remove_inconsistent_values(head, tail, constraint, assignments)
    return assignments

use_mrv=True
use_lcv=True

def backtrack(assignments, unassigned, csp):
    if csp_solved(unassigned): return assignments
    print("Applying AC3")
    csp['variables'] = ac3(assignments, unassigned, csp)
    print("AC3 Applied:")
    pprint.PrettyPrinter(indent=2).pprint(csp['variables'])

    #make mrv optional
    var = select_unassigned_variable_mrv(unassigned)
    print("Selected var by MRV is "+str(var))
    #make lcv optional
    values = order_values_lcv(var, assignments, unassigned, csp)
    print(csp['variables'])

    for value in values:
        assignments[var] = [value]
        v = forward_check(assignments, unassigned, csp)
        print("if" + str(var) + "equals" + str(value) + "then remaining possible assignments  are" + str(v))
        if empty_remaining_domain(v):
            print("Impossible , a variable has no possible assignment")
            continue  # A variable has no legal values,try another assignment
        u = {var: val for var, val in v.items() if var not in assignments}
        result = backtrack(assignments.copy(), u, csp)
        if result != FAILURE: return result

    return FAILURE


def csp_solved(unassigned):
    return len(unassigned) == 0


def empty_remaining_domain(v):
    return any((len(values) == 0 for values in v.values()))


def all_remaining_assignments(assignments, unassigned):
    """
  Merge together assigned and unassigned dictionaries (assigned
  values take priority).
  """
    v = unassigned.copy()
    v.update(assignments)
    return v


def forward_check(assignments, unassigned, csp):
    def remove_inconsistent_values(head, tail, constraint, variables):
        valid_tail_values = [t for t in variables[tail] if any((constraint(h, t) for h in variables[head]))]
        removed = len(variables[tail]) != len(valid_tail_values)
        variables[tail] = valid_tail_values
        return removed

    def select_constraints(node):
      return [(h, t, c) for h, t, c in csp['constraints'] if h == node]

    queue, variables = csp['constraints'][:], all_remaining_assignments(assignments, unassigned)
    while len(queue):
        head, tail, constraint = queue.pop(0)
        if remove_inconsistent_values(head, tail, constraint, variables):
            queue.extend(select_constraints(tail))  # Applying Forward check by rechecking constraints of modified arcs
    return variables


def select_unassigned_variable_mrv(unassigned):
    return min(unassigned.keys(), key=lambda k: len(unassigned[k]))


def order_values_lcv(var, assignments, unassigned, csp):
    """
  Orders the values of an unassigned variable according to the
  Least Constraining Value principle: order values by the amount
  of values they eliminate when assigned (fewest eliminated at the
  front, most eliminated at the end). Keeps future options open.
  """

    def count_vals(vars):
        return sum((len(vars[v]) for v in unassigned if v != var))

    def values_eliminated(val):
        assignments[var] = [val]
        new_vals = count_vals(forward_check(assignments, unassigned, csp))
        del assignments[var]
        return new_vals

    return sorted(unassigned[var], key=values_eliminated, reverse=True)
