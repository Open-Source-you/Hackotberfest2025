chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

# Base 62 encoder
def encode(num : int) -> str:
    
    if num == 0:            # Base Case
        return chars[0]
        
    result = []    
    
    while(num > 0):
        remainder = num % 62
        result.append(chars[remainder])
        num = num // 62
        
    result.reverse()
    return ''.join(result)