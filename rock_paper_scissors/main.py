import random
from art import logo

print(logo)
print("Welcome to a game of Rock, Paper, Scissors")


computer_score = 0
player_score = 0

easy_level = 11
medium_level = 7
hard_level = 3

Round = 0

def set_level():
    while True:
        level = input("Choose your difficulty. \nIn easy mode, you get 11 chances."
                      " In medium mode, you get 7 chances."
                      " In hard mode, you get 3 chances\n(easy, medium or hard?): ").lower()
        if level == "easy":
            return easy_level
        elif level == "hard":
            return hard_level
        elif level == "medium":
            return medium_level
        else:
            print("Invalid input! Please choose 'easy', 'medium', or 'hard'.")


turns = set_level()


def play_game(turns):
    global player_score, computer_score, Round

    for i in range(turns):
        while True:
            player_choice = input("Enter a choice (Rock, Paper, Scissors) : ").title()
            if player_choice in ["Rock", "Paper", "Scissors"]:
                break
            else:
                print("Invalid input! Please choose 'Rock', 'Paper', or 'Scissors'.")

        decision = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(decision)

        if player_choice == computer_choice:
            Round += 1
            print(f"Round {Round}")
            print(f"Computer chose: {computer_choice}\nThis round is a tie! ")
            print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")
            turns -= 1
            print(f"Chances remaining: {turns}")

        elif player_choice == "Rock":
            Round += 1
            print(f"Round {Round}")
            print(f"Computer chose: {computer_choice}")
            if computer_choice == "Scissors":
                player_score += 1
                print("Rock smashes Scissors\nYou won this round!")
                print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")
            else:
                computer_score += 1
                print("Paper covers Rock\nComputer won this round!")
                print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")
            turns -= 1
            print(f"Chances remaining: {turns}")

        elif player_choice == "Paper":
            Round += 1
            print(f"Round {Round}")
            print(f"Computer chose: {computer_choice}")
            if computer_choice == "Rock":
                player_score += 1
                print("Paper covers Rock\nYou won this round!")
                print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")
            else:
                computer_score += 1
                print("Scissors cuts Paper\nComputer won this round!")
                print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")
            turns -= 1
            print(f"Chances remaining: {turns}")

        elif player_choice == "Scissors":
            Round += 1
            print(f"Round {Round}")
            print(f"Computer chose: {computer_choice}")
            if computer_choice == "Paper":
                player_score += 1
                print("Scissors cuts paper\nYou won this round!")
                print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")
            else:
                computer_score += 1
                print("Rock smashes Scissors\nComputer won this round!")
                print(f"Computer_score is {computer_score}\nPlayer_score is {player_score}")
            turns -= 1
            print(f"Chances remaining: {turns}")



play_game(turns)

if computer_score > player_score:
    print("Computer won the game!!!")
elif computer_score == player_score:
    print("It's a tie!!!")
else:
    print("Congratulations, you won the game!!!")






