# Source(s): 
# Adapted from "Optimization Sample: Shipping" by Microsoft Azure Quantum Docs (2021)

import os
from typing import List
from azure.quantum import Workspace
from azure.identity import ClientSecretCredential
from azure.quantum.optimization import Problem, ProblemType, Term
from azure.quantum.optimization import ParallelTempering


tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]
credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)

workspace = Workspace(
    subscription_id = os.environ["QUANTUM_SUBSCRIPTION_ID"],
    resource_group = os.environ["QUANTUM_RESOURCE_GROUP"],
    name = os.environ["QUANTUM_WORKSPACE_NAME"],
    location = os.environ["QUANTUM_LOCATION"]
)

workspace.credentials = credential

def create_problem_for_number_partition(partition_weights: List[int]) -> Problem:
    terms: List[term] = []

    for i in range(len(partition_weights)):
        for j in range(len(partition_weights)):
            if i == j:
                continue
            terms.append(
                Term(
                    c = partition_weights[i] * partition_weights[j],

                    indices = [i, j]
                )
            )

    return Problem(name="Number Partitioning Problem", problem_type=ProblemType.ising, terms=terms)

def create_simplified_problem_for_number_partition(partition_weights: List[int]) -> Problem:
    terms: List[Term] = []

    for i in range(len(partition_weights)-1):
        for j in range(i+1, len(partition_weights)):
            terms.append(
                Term(
                    c = partition_weights[i] * partition_weights[j],

                    indices = [i, j]
                )
            )

    return Problem(name="Number Partition Problem (Simplified)", problem_type = ProblemType.ising, terms=terms)

def solve_number_partition(problem):
    print("Log workspace!", workspace)
    print(workspace.credentials)
    solver = ParallelTempering(workspace, timeout=100)
    result = solver.optimize(problem)
    return result