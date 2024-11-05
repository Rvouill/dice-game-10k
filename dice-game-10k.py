# Game-10K

# Libraries
import random
from collections import Counter

# Default Properties

# Function "Throw" 
# Parameters "number_of_dices"
def throw(number_of_dices):
    # Generate a single array of random integers between 1 and 6
    throw_set = [random.randint(1, 6) for _ in range(number_of_dices)]
    return throw_set

# Function "Get Results"
def get_results(throw_set):
    
    messages = []  # List to store messages
    
    # Royal Suite: 2000 pts
    if len(throw_set) == 6 and set(throw_set) == {1, 2, 3, 4, 5, 6}:
        messages.append("Royal Suite: 2000 pts")
    
    # Triple 1: 1000 pts
    if throw_set.count(1) == 3:
        messages.append("Triple One: 1000 pts")
    
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
    
    # Find Iteration Of "1"
    if throw_set.count(1) == 2:
        messages.append("Double One: 200 pts")
    if throw_set.count(1) == 1:
        messages.append("Only One: 100 pts")
        
    # Find Iteration Of "5"
    if throw_set.count(5) > 0:
        fives = throw_set.count(5)
        messages.append(f"Fives : {fives * 50} pts")
        
    if messages:
        return " | ".join(messages)
    else:
        return "No special combination"

# Execute a throw and get the result
my_throw = throw(6)
print(f'Throw: {my_throw}')
print(f'Result: {get_results(my_throw)}')