words = ["HELLO", "COMPUTER", "KEYBOARD", "INTERNET", "CORRECT", "HORSE", "BATTERY", "STAPLE"]
word = choice(words)

user = ["_" for _ in word]
tries = 10

while True:    
    if tries <= 0:
        print("You lose!")
        print("The word was: " + word)
        break
        
    print(" ".join(user))
        
    if user == list(word):
        print("You win!")
        break
    
    print("%d tries remaining" % tries)
    
    current = input("? ")[:1].upper()
    
    if not current:
        continue
        
    found = False
    
    for i in range(len(user)):
        if word[i] == current:
            user[i] = current
            found = True
            
    if not found:
        tries -= 1
        
    print("\n")
