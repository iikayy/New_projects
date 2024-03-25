import random
from art import logo

print(logo)
print("Welcome to a game of Rock, Paper, Scissors")

computer_score = 0
player_score = 0


def play_game():

    global player_score, computer_score
    game_on = True
    while game_on:

        player_choice = input("Enter a choice (Rock, Paper, Scissors) : ")
        decision = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(decision)

        if player_choice == computer_choice:
            print(f"Computer chose: {computer_choice}")
            print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")

        elif player_choice == "Rock":
            print(f"Computer chose: {computer_choice}")
            if computer_choice == "Scissors":
                player_score += 1
                print("Rock beats Scissors")
                print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")
            else:
                computer_score += 1
                print("Paper beats Rock")
                print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")

        elif player_choice == "Paper":
            print(f"Computer chose: {computer_choice}")
            if computer_choice == "Rock":
                player_score += 1
                print("Paper beats Rock")
                print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")
            else:
                computer_score += 1
                print("Scissors beats Paper")
                print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")

        elif player_choice == "Scissors":
            print(f"Computer chose: {computer_choice}")
            if computer_choice == "Paper":
                player_score += 1
                print("Scissors beats paper")
                print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")
            else:
                computer_score += 1
                print("Rock beats Scissors")
                print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")

        continue_game = input("Do you want to continue (yes or no?) : ")
        if continue_game == "yes":
            play_game()
        else:
            print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")
            if computer_score > player_score:
                print("Computer won the game!!!")
            elif computer_score == player_score:
                print("It's a tie!!!")
            else:
                print("Congratulations, you won the game!!!")
        game_on = False


play_game()
