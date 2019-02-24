FAILURE = 'FAILURE'
import pprint
pp=pprint.PrettyPrinter(indent=2)
use_mrv=False
use_lcv=True
use_dh=True


def solve(csp):
    result = backtrack({}, csp['variables'], csp)
    if result == FAILURE: return result
    return {k: v[0] for k, v in result.items()}  # Unpack values wrapped in arrays.

#make formalisation work on all

# add degree heuristic

# interface

def ac3(assignments, unassigned, csp):
    def remove_inconsistent_values(head, tail, constraint, variables):
        valid_tail_values = [t for t in variables[tail] if any((constraint(h, t) for h in variables[head]))]
        variables[tail] = valid_tail_values
        removed = len(variables[tail]) != len(valid_tail_values)
        return removed

    def select_constraints(node):
      return [(h, t, c) for h, t, c in csp['constraints'] if h == node]

    queue, variables = csp['constraints'][:], all_remaining_assignments(assignments, unassigned)
    while len(queue):
        head, tail, constraint = queue.pop(0)
        if remove_inconsistent_values(head, tail, constraint, variables):
            queue.extend(select_constraints(tail))  # Applying Arc consistency  by rechecking constraints of modified arcs
    return variables



def backtrack(assignments, unassigned, csp):
    if csp_solved(unassigned): return assignments
    print("Applying AC3")
    csp['variables'] = ac3(assignments, unassigned, csp)
    print("AC3 Applied:")
    pp.pprint(csp['variables'])

    if(use_mrv):
        var = select_unassigned_variable_mrv(unassigned)
        print("Var Selected by MRV is "+str(var))
    elif (use_dh):
        var=select_unassigned_variable_dh(unassigned,csp)
        print("Var Selected by DH is "+str(var))
    else:
        var = select_variables_in_order_of_appearance(unassigned)
        print("Var selected by order of apperance is "+str(var))
    #make lcv optional
    if(use_lcv):
        values = order_values_lcv(var, assignments, unassigned, csp)
        print("Values in LCV Order")
        pp.pprint(csp['variables'])
    else:
        values=select_values_in_order_of_appearance(var,unassigned)
        print("Values in  Order of Appearance")
        pp.pprint(csp['variables'])


    for value in values:
        assignments[var] = [value]
        v = forward_check(var,assignments, unassigned, csp)
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


def forward_check(node,assignments, unassigned, csp):
    def remove_inconsistent_values(head, tail, constraint, variables):
        valid_tail_values = [t for t in variables[tail] if any((constraint(h, t) for h in variables[head]))]
        variables[tail] = valid_tail_values
        removed = len(variables[tail]) != len(valid_tail_values)
        return removed

    def select_constraints(node):
      return [(h, t, c) for h, t, c in csp['constraints'] if h == node]

    queue, variables = select_constraints(node), all_remaining_assignments(assignments, unassigned) # We're going to only verify the contsraints of the are we modified
    while len(queue):
        head, tail, constraint = queue.pop(0)
        if remove_inconsistent_values(head, tail, constraint, variables):
            queue.extend(select_constraints(tail))  # Applying Forward check by rechecking constraints of modified arcs that are related to var
    return variables


def select_unassigned_variable_mrv(unassigned):
    return min(unassigned.keys(), key=lambda k: len(unassigned[k]))

def select_unassigned_variable_dh(unassigned,csp):
    def count_constraints(node):
      return len([h for h, t, c in csp['constraints'] if h == node])
    return max(unassigned.keys(), key=count_constraints)



def select_variables_in_order_of_appearance(unassigned):
    return next(iter(unassigned.keys()))

def select_values_in_order_of_appearance(var,unassigned):
    return unassigned[var]

def order_values_lcv(var, assignments, unassigned, csp):

    def count_vals(vars):
        return sum((len(vars[v]) for v in unassigned if v != var))

    def values_eliminated(val):
        assignments[var] = [val]
        new_vals = count_vals(forward_check(var,assignments, unassigned, csp))
        del assignments[var]
        return new_vals

    return sorted(unassigned[var], key=values_eliminated, reverse=True)
