"""
Problem: https://www.hackerrank.com/challenges/sparse-arrays/problem?isFullScreen=true
There is a collection of input strings and a collection of query strings. 
For each query string, determine how many times it occurs in the list of input strings. 
Return an array of the results.
Example
stringList = ['ab', 'ab', 'abc'for jfjf 
queries = ['ab', 'abc', 'bc']
here are 2 instances of 'ab', 1 of 'abc', and 0 of 'bc'. 
For each query, add an element to the return array: results = [2, 1, 0].
There are  instances of '',  of '', and  of ''. For each query, add an element to the return array: .
"""


def matchingStrings(stringList, queries):

    Counter = {} # key= String; 

    # Loop through the string
    for string in stringList:  
        # Count number of occurences of each unique string
        if string in Counter:
            Counter[string] += 1
        else:
            Counter[string] = 1

    counts = []

    # Loop through queries
    for query in queries:
        # Add frequency of each query to counts
        if query in Counter:
            counts.append(Counter[query])
        else:
            counts.append(0)

    return counts

def main():
    stringList = ["ab", "ab", "abc"]
    queries = ["ab", "abc", "bc"]
    print(matchingStrings(stringList, queries))

if __name__ == '__main__':
    main()
