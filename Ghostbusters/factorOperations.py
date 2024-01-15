# factorOperations.py
# -------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from typing import List
from bayesNet import Factor
import functools
from util import raiseNotDefined
def joinFactorsByVariableWithCallTracking(callTrackingList=None):
    def joinFactorsByVariable(factors: List[Factor], joinVariable: str):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.
        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.
        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.
        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """
        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))
        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]
        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        if numVariableOnLeft > 1:
            print("Factor failed joinFactorsByVariable typecheck: ", factor)
            raise ValueError("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        
        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor
    return joinFactorsByVariable
joinFactorsByVariable = joinFactorsByVariableWithCallTracking()
########### ########### ###########
########### QUESTION 2  ###########
########### ########### ###########
def joinFactors(factors: List[Factor]):
    """
    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.
    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.
    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.
    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).
    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.
    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """
    # typecheck portion
    setsOfUnconditioned = [set(factor.unconditionedVariables()) for factor in factors]
    if len(factors) > 1:
        intersect = functools.reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print("Factor failed joinFactors typecheck: ", factor)
            raise ValueError("unconditionedVariables can only appear in one factor. \n"
                    + "unconditionedVariables: " + str(intersect) + 
                    "\nappear in more than one input factor.\n" + 
                    "Input factors: \n" +
                    "\n".join(map(str, factors)))
            
            
            
            
    "*** YOUR CODE HERE ***"
    conditioned_set_result = set()
    unconditioned_set_result = set()
    variable_domains_dict_result = {}

    # Extract conditioned and unconditioned variables from factors
    for factor_instance in factors:
        conditioned_set_result.update(factor_instance.conditionedVariables())
        unconditioned_set_result.update(factor_instance.unconditionedVariables())
        variable_domains_dict_result.update(factor_instance.variableDomainsDict())

    # Remove variables that are both conditioned and unconditioned
    conditioned_set_result -= unconditioned_set_result

    # Create a new factor with updated variable sets and domains
    new_factor_result = Factor(unconditioned_set_result, conditioned_set_result, variable_domains_dict_result)

    assignments_result = new_factor_result.getAllPossibleAssignmentDicts()

    while assignments_result:
        assignment_result = assignments_result.pop()
        probability_result = 1

        for factor_instance in factors:
            probability_result *= factor_instance.getProbability(assignment_result)

        new_factor_result.setProbability(assignment_result, probability_result)

    # Return the new factor
    return new_factor_result

    # raiseNotDefined()
    # return
    "*** END YOUR CODE HERE ***"
    
    
    
    
    
########### ########### ###########
########### QUESTION 3  ###########
########### ########### ###########
def eliminateWithCallTracking(callTrackingList=None):
    def eliminate(factor: Factor, eliminationVariable: str):
        """
        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.
        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.
        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))
        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))
            
            
        "*** YOUR CODE HERE ***"
        conditioned_vars = set(factor.conditionedVariables())
        unconditioned_vars = set(factor.unconditionedVariables())
        variable_domains = factor.variableDomainsDict()

        unconditioned_vars.discard(eliminationVariable)
        new_factor = Factor(unconditioned_vars, conditioned_vars, variable_domains)

        for assignment in new_factor.getAllPossibleAssignmentDicts():
            probability = sum(
                factor.getProbability({**assignment, eliminationVariable: value})
                for value in variable_domains[eliminationVariable]
            )
            new_factor.setProbability(assignment, probability)

        return new_factor

    return eliminate
  
eliminate = eliminateWithCallTracking()