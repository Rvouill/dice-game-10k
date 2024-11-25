# Dice 10K

# Libraries
import random
from collections import Counter

# Includes

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

# Main Process #
################

# Get players number from user ?
num_players = int(input("Enter the number of players: "))

# Create a collection to store scores, initialized to 0 for all players
players = [{"name": f"Player{i+1}", "scores": [], "total_score": 0} for i in range(num_players)]

# Display the initial scores
print("\nInitial Scores:")
for player in players:
    print(f"{player['name']} : {player['total_score']}")


# Loop For Rounds Till One Player Get 10K
while True:
    for player in players:

        re_throw = True
        dice_nbr = 6
        while re_throw:
            # Execute a throw and get the result
            my_throw = throw(dice_nbr)
            print(f'\nThrow: {my_throw}')
            print(f'\nResult: {get_results(my_throw)}')

            # Enter & store points scored in this round
            while True:
                try:
                    points = int(input(f"\nEnter points scored by {player['name']} in this round: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")


            # Add the points to the player's scores list
            player["scores"].append(points)
            
            # Update the total score
            player["total_score"] += points

            # Check if the user wants to re-throw
            while True:
                re_throw_input = input(f"\nRe throw? (Y/N): ").strip().lower()
                if re_throw_input in {"y", "n"}:
                    re_throw = re_throw_input == "y"
                    dice_nbr = int(input(f"\nEnter dice left for {player['name']} in this round: "))
                    break
                else:
                    print("Invalid input. Please enter 'Y' or 'N'.")


        # Display current player infos
        print(f"\n{player['name']} - Round score : {points} Points - Total score : {player["total_score"]} Points")
        
        # Check if the player's total score exceeds 10,000
        if player["total_score"] >= 10000:
            print(f"\n{player['name']} has won the game with a total score of {player['total_score']}!")
            break
    else:
        # Continue the game if no one has exceeded 10,000
        continue
    break  # Exit the outer loop if a player has won


# Display final scores
print("\nFinal Scores:")
for player in players:
    print(f"{player['name']}: {player['total_score']}")
