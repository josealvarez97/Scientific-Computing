'''
References:
* Karmarkar, N. & Karp, R. (1982). The differencing method of set partitioning. Technical Report. University of California at Berkeley, USA. https://dl.acm.org/doi/10.5555/894426
* Korf, R. E. (1998). A complete anytime algorithm for number partitioning. Artificial Intelligence. https://doi.org/10.1016/S0004-3702(98)00086-1
'''

from copy import deepcopy

def replace_element(array, target, new_elem):
    for i in range(len(array)):
        if array[i] == target:
            array[i] = new_elem
            break

def karmarkar_karp(number_list):
    '''
    largest_differencing_method

    To-do:
        * It's a mistake to sort the list more than once, it should be possible to do all operations in the same list.
    '''
    number_list.sort()
    L = number_list
    Ls = [L]

    A = []
    B = []
    diffs = []
    optimal_value = None

    while True:
        # Order the numbers
        L.sort() 
        # Replace the largest and second-largest by their difference
        diff = L[-1] - L[-2]
        diffs.append(diff)
        L = L[0:len(L)-2] + [diff]
        Ls.append(deepcopy(L))
        #  If two or more numbers remain, return to step 1
        if len(L) < 2: 
            # I don't really care about saving the last one into a list...
            # But I do 
            A = L
            optimal_value = L[0]
            break
  
    print(Ls)
    # Using backtracking, compute the partition
    for i in range(2, len(Ls)+1):
        diff = diffs[-i+1]
        print("diff", diff)
        Ls[-i].sort() 

        if diff in A:
            print(A)
            print(Ls[-i])
            # A = A[0:-1] + [Ls[-i][-1]]
            replace_element(A, diff, Ls[-i][-1])
            B.append(Ls[-i][-2])
        else:
            # B = B[0:-1] + [Ls[-i][-1]]
            replace_element(B, diff, Ls[-i][-1])
            A.append(Ls[-i][-2])
        print(A, B)

    return A, B, optimal_value


def application():
    # partition_weights = [1, 5, 9, 21, 35, 5, 3, 5, 10, 11]
    partition_weights = [4,5,6,8,7]
    ship_A, ship_B, ship_diff = karmarkar_karp(partition_weights)

    print("\nVerify result")
    print("sum(ship_A) - sum(ship_B)", sum(ship_A) - sum(ship_B))
    print("ship_diff", ship_diff)
    print(ship_A)
    print(ship_B)


if __name__ == '__main__':
    application()

