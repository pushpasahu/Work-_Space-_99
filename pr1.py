
#Time complexity O(n)
def panlindromChecker(word : str) -> bool:
    return True if word == word[::-1] else False


#Time complexity O(n) + O(log(n))
def panlindromChecker2(word : str) -> bool:
    i = 0
    j = len(word)-1
    while i < j:
        if word[i] != word[j]:
            return False
        i+=1
        j-=1
    return True
    

word = "12321"

print(panlindromChecker2(word))