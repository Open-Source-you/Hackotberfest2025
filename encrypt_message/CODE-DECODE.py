# code or decode
print("WELCOME TO INCRIPTION ")
A = input("Weither you want to Code or Decode:")
if A.lower() == "code":
    words = input("Enter a word:").split()
    print("YOUR CODE IS :")
    for word in words:
        if len(word) < 2:
            print(word, end=" ")
        elif len(word) == 2:
            new_word = word[::-1]
            print(new_word, end=" ")
        else:
            word = list(
                word
            )  # Yes, word = word.split() does convert the string into a list — but only a list of words (based on spaces),not a list of characters.co
            word[0], word[-1] = word[-1], word[0]
            new_word = "".join(word)
            import random

            chars = "abcdefghijklmnopqrstuvwxyz"
            new3 = ""
            for i in range(3):
                new3 += random.choice(chars)
            new_word1 = new3 + new_word
            new4 = ""
            for i in range(3):
                new4 += random.choice(chars)
            new_word2 = new_word1 + new4
            print(new_word2, end=" ")

elif A.lower() == "decode":
    words = input("Enter a word:").split()
    print("YOUR DECODE IS :")
    for word in words:
        word = list(word)
        new_word = word[3::]
        new_word2 = new_word[:-3]
        if len(word) < 2:
            print(word, end=" ")
        elif len(word) == 2:
            new_word = word[::-1]
            new_word = "".join(new_word)
            print(new_word, end="")
        else:
            new_word2[0], new_word2[-1] = new_word2[-1], new_word2[0]
        new_word3 = "".join(new_word2)
        print(new_word3, end=" ")

else:
    raise ValueError("ENTER CODE OR DECODE ONLY")
