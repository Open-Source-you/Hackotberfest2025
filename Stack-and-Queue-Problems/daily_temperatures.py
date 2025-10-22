def dailyTemperatures(T):
    res = [0] * len(T)
    stack = []
    for i, temp in enumerate(T):
        while stack and T[stack[-1]] < temp:
            idx = stack.pop()
            res[idx] = i - idx
        stack.append(i)
    return res
