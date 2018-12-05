import python.csp as csp
import pprint

F = open("problem.txt")
P = F.read();

variables = P.split("\n")[0].split(":")[1].split(",");
domain = P.split("\n")[1].split(":")[1].split(",");
constraints = P.split("\n")[2].split(":")[1].split(",");

print(variables)
print(domain)
print(constraints)

realconstraints = []
for element in constraints:
    head = element.split(" ")[0];
    tail = element.split(" ")[2];
    op = element.split(" ")[1];
    if op == "!=":
        realconstraints.append([head,tail,lambda x,y: x != y])

print(realconstraints)

realvariables = {state:domain for state in variables}

print(realvariables)

us = {}
us['variables'] = realvariables
us['constraints'] = realconstraints
result = csp.solve(us)

status = 'SUCCESS'
if result == 'FAILURE':
  status = 'FAILURE'

print ('\n***************')
print ('    ' + status)
print ('***************\n')
pprint.PrettyPrinter(indent=2).pprint(result)
print ('\n')
