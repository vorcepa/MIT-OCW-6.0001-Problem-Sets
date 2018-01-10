# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx


def permutations(s):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    if len(s) <= 1:
        return s
    else:
        perms = []
        for e in permutations(s[:-1]):
            for i in range(len(e)+1):
                to_append = e[:i] + s[-1] + e[i:]
                if to_append not in perms:
                    perms.append(to_append)
        return perms
    
if __name__ == "__main__":
    s = input("Enter a string to get all unique permutation (recommend 7 characters or less): ")
    output = permutations(s)
    print(output)

