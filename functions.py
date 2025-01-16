# Libraries
import random
from collections import Counter

# Function    : Throw
# Description : Simulate a throw of dices
# Parameter   : Int "number_of_dices"
# Return      : Array "throw_set"
def throw(number_of_dices):
    # Generate a single array of random integers between 1 and 6
    throw_set = [random.randint(1, 6) for _ in range(number_of_dices)]
    print(f"Throw Set : {throw_set}")
    return throw_set

# Function    : Get Results
# Description : Apply 10k rules to throw set & display possible results 
# Parameter   : Array of dice results
# Reurn       : String "messages"
def get_results(throw_set):
    
    messages = []  # List to store messages
    
    # Royal Suite: 2000 pts
    if len(throw_set) == 6 and set(throw_set) == {1, 2, 3, 4, 5, 6}:
        messages.append("Royal Suite: 2000 pts")
    
    # Triples of 1 : 1000 pts (each)
    # + remaings of 1 : 100 pts (each)
    count_of_1 = throw_set.count(1)
    triples_of_1 = count_of_1 // 3  # Number of triples of 1
    remaining_1s = count_of_1 % 3   # Leftover of 1

    if triples_of_1 > 0:
        messages.append(f"Triple 1s: {triples_of_1 * 1000} pts")
    if remaining_1s > 0:
        messages.append(f" Ones: {remaining_1s * 100} pts")
    
    # 3 Doubles: 500 pts
    doubles = [num for num in set(throw_set) if throw_set.count(num) == 2]
    if len(doubles) == 3:
        messages.append("3 Doubles: 500 pts")
    
    # 3 Times Same Number : Dice Value x 100 pts
    counts = Counter(throw_set)
    triples = [num for num, count in counts.items() if count > 2 and num != 1]
    if len(triples) == 1:
        # Calculate the score based on the triple values
        value = sum(triple * 100 for triple in triples)
        messages.append(f"Triple : {value} pts (Values: {triples[0]})")
    if len(triples) == 2:
        # Calculate the score based on the triple values
        value = sum(triple * 100 for triple in triples)
        messages.append(f"Triple : {value} pts (Values: {triples[0]} and {triples[1]})")
        
    # Find Iteration Of "5"
    if throw_set.count(5) > 0:
        fives = throw_set.count(5)
        messages.append(f"Fives : {fives * 50} pts")
        
    if messages:
        return " | ".join(messages)
    else:
        return "No special combination"
