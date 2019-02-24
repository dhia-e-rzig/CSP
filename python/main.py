import itertools as it
import re
import python.csp as csp
import pprint

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

F = open("testproblem.txt")
R = F.read()

testvariables1 = R.split("variables:")[1].split("\ndomaine:")[0]
testdomain1 = R.split("domaine:")[1].split("\ncontraintes:")[0]
testconstrainte1 = R.split("contraintes:")[1]+" "


variables = []
for el in testvariables1.split(","):
    variables.append(el)


domain = testdomain1.split(";")
domainvalues = []
domaincombinations = []
domainattr = []
if len(domain)>1:
    for dom in domain:
        d = []
        for el in dom.split(":")[1].split(","):
            if RepresentsInt(el):
                d.append(eval(el))
            else:
                d.append(el)
        domainvalues.append(d)
        domainattr.append(dom.split(":")[0])
    for iter in it.product(*domainvalues):
        domaincombinations.append(iter)
else:
    for d in domain[0].split(","):
        if RepresentsInt(d):
            domaincombinations.append(eval(d))
        else:
            domaincombinations.append(d)

print(domaincombinations)
print(domainattr)

print("----------------------------------------")




constraints = testconstrainte1.split(";")

problem = {}
problem['variables'] = []
problem['constraints'] = []

problem['variables'] = {var:domaincombinations for var in variables}

for con in constraints:
    #si "pour tout" existe
    if len(con.split(":"))>1:
        the_v = con.split(":")[0].split("pour tout ")[1].split(" dans ")[0]
        ensemble = con.split(":")[0].split("pour tout ")[1].split(" dans ")[1]
        the_vars = []
        for el in the_v.split(","):
            the_vars.append(el)

        operations = con.split(":")[1]
        for i in range(len(domainattr)):
            operations = operations.replace("."+domainattr[i],"["+str(i)+"]")
        operations = operations.replace(",","and")
        operations = operations.replace(" |"," abs(").replace("| ",") ")
        lambdaexpr = "lambda "
        for el in the_vars:
            lambdaexpr = lambdaexpr+el+","
        lambdaexpr = lambdaexpr[:-1] + ":"+operations
        print(lambdaexpr)
        varparams = ""
        for i in range(len(the_vars)):
            varparams = varparams+"el["+str(i)+"]"+","
        fullstring = varparams+" "+lambdaexpr
        print(fullstring)

        for el in it.permutations(variables,len(the_vars)):
            problem['constraints'].append(list(eval(fullstring)))
    else:
        constraint = con.replace(" et "," and ")
        nospace = constraint.replace(" ","")
        varparams = []
        fullstring = ""
        for el in re.split('!=|==|>|<',nospace):
            varparams.append(el.lower())
            fullstring = fullstring + "'"+ el +"',"
        lambdaexpr = "lambda "
        for el in varparams:
            lambdaexpr = lambdaexpr + el +","
        lambdaexpr = lambdaexpr[:-1] + ":" + constraint.lower()
        fullstring = fullstring + lambdaexpr
        problem['constraints'].append(list(eval(fullstring)))

print(problem['variables'])
print(problem['constraints'])

result = csp.solve(problem)
status = 'SUCCESS'
if result == 'FAILURE':
    status = 'FAILURE'

print('\n***************')
print('    ' + status)
print('***************\n')
pprint.PrettyPrinter(indent=2).pprint(result)
print('\n')













