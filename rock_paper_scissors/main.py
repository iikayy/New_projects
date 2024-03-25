import random
from art import logo

print(logo)
print("Welcome to a game of Rock, Paper, Scissors")


def play_game():
    game_on = True
    while game_on:

        player_choice = input("Enter a choice (Rock, Paper, Scissors) : ")
        decision = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(decision)

        if player_choice == computer_choice:
            print(f"It's a tie\nComputer chose: {computer_choice}"
                  f" \nYou chose: {player_choice}")
        elif player_choice == "Rock":
            print(f"Computer chose: {computer_choice}")
            print("You win!!!\n Rock beats Scissors") if computer_choice == "Scissors" else print("You lose!!!\n Paper beats Rock")
        elif player_choice == "Paper":
            print(f"Computer chose: {computer_choice}")
            print("You win!!!\n Paper beats Rock") if computer_choice == "Rock" else print("You lose!!!\n Scissors beats Paper")
        elif player_choice == "Scissors":
            print(f"Computer chose: {computer_choice}")
            print("You win!!!\n Scissors beats paper") if computer_choice == "Paper" else print("You lose!!!\n Rock beats Scissors")

        continue_game = input("Do you want to continue (yes or no?) : ")
        if continue_game == "yes":
            play_game()
        else:
            print("Goodbye!!!")
        game_on = False


play_game()



