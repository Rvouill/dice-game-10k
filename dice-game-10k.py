# Dice 10K #
############

# Includes
import functions

# Start #
#########

# Get players number from user ?
num_players = int(input("Enter the number of players: "))

# Create a collection to store scores, initialized to 0 for all players
players = [{"name": f"Player{i+1}", "scores": [], "total_score": 0} for i in range(num_players)]

# Display the initial scores
print("\nInitial Scores:")

# Loop For Rounds Till One Player Get 10K
while True:
    # Display scores
    for player in players:
        print(f"{player['name']} : {player['total_score']}")

    # Start round
    for player in players:

        re_throw   = True # Determine whether to throw or not
        dice_nbr   = 6 # Determine the number of dice to throw 
        player_pts = 0 # Store player total round score 

        while re_throw:

            # Execute a throw, get and display results
            my_throw = functions.throw(dice_nbr)
            print(f'\nThrow: {my_throw}')
            print(f'\nResult: {functions.get_results(my_throw)}')

            # Enter & store hand points scored in this round
            while True:
                try:
                    hand = int(input(f"\nEnter points scored by {player['name']} in this round: "))
                    if hand == 0:
                        player_pts = 0
                    else:
                        player_pts += hand
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            # Check if the user wants to re-throw
            while True:
                re_throw_input = input(f"\nRe throw? (Y/N): ").strip().lower()
                if re_throw_input == "y":
                    re_throw = True
                    dice_nbr = int(input(f"\nEnter dice left for {player['name']} in this round: "))
                    break
                if re_throw_input == "n":
                    re_throw = False
                     # Add the points to the player's scores list
                    player["scores"].append(player_pts)
                    
                    # Update the total score
                    player["total_score"] += player_pts
                    break
                else:
                    print("Invalid input. Please enter 'Y' or 'N'.")


        # Display current player infos
        print(f"\n{player['name']} - Round score : {player_pts} Points - Total score : {player["total_score"]} Points")
        
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
