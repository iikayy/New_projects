from googletrans import Translator
import platform
import os


balance = 0
translator = Translator()


def set_language():
    while True:
        choice = input("Please choose your preferred language (English, Igbo, Hausa, Yoruba): ").title()
        if choice == "English":
            return "en"
        elif choice == "Igbo":
            return "ig"
        elif choice == "Hausa":
            return "ha"
        elif choice == "Yoruba":
            return "yo"
        else:
            print("Invalid option, please enter (English, Igbo, Hausa, Yoruba)")


def detect_machine():
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Darwin":
        return "mac"
    else:
        return "unknown"


machine_type = detect_machine()
print(f"Welcome to the {machine_type} Automated Teller Machine ")
language = set_language()


def print_transaction_slip(transaction):
    document_folder = os.path.expanduser("~/Documents")
    file_path = os.path.join(document_folder, f"transaction_slip_{machine_type}.txt")
    with open(file_path, "w") as file:
        file.write(transaction)
    print(f"Transaction slip saved to {file_path}")


def translate(text):
    return translator.translate(text, dest=language).text


def get_valid_amount(number):
    while True:
        try:
            amount = int(input(number))
            if amount <= 0:
                print(translate("Amount must be greater than zero."))
            else:
                return amount
        except ValueError:
            print(translate("Invalid input. Please enter a valid amount."))


while True:
    text = input(translate("Select a transaction\n1.Withdraw\n2.Transfer\n3.Deposit\n4.Check balance\n5.Exit\n__\n ")).title()

    if text == translate("Withdraw"):
        withdraw_amount = get_valid_amount(translate("How much do you want to withdraw?: "))
        if withdraw_amount > balance:
            print(translate("Insufficient balance."))
        else:
            balance -= withdraw_amount
            print(translate(f"Congratulations, you've withdrawn #{withdraw_amount}"))

        decision = input(translate("Do you want to print your transaction slip (yes or no): ")).lower()
        if decision == "yes":
            print_transaction_slip(translate(f"Congratulations, you've withdrawn #{withdraw_amount}"))
            print(translate("Transaction slip printed!"))
        elif decision == "no":
            continue
        else:
            print(translate("Invalid option, please enter (yes or no)"))

    elif text == translate("Transfer"):
        transfer_amount = get_valid_amount(translate("How much do you want to Transfer?: "))
        if transfer_amount > balance:
            print(translate("Insufficient balance."))
        else:
            balance -= transfer_amount
            print(translate(f"Congratulations, you've transferred #{transfer_amount}"))

        decision = input(translate("Do you want to print your transaction slip (yes or no): ")).lower()
        if decision == "yes":
            print_transaction_slip(translate(f"Congratulations, you've transferred #{transfer_amount}"))
            print(translate("Transaction slip printed!"))
        elif decision == "no":
            continue
        else:
            print(translate("Invalid option, please enter (yes or no)"))

    elif text == translate("Deposit"):
        deposit_amount = get_valid_amount(translate("How much do you want to Deposit?: "))
        balance += deposit_amount
        print(translate(f"Congratulations, you've deposited #{deposit_amount}"))

        decision = input(translate("Do you want to print your transaction slip (yes or no): ")).lower()
        if decision == "yes":
            print_transaction_slip(translate(f"Congratulations, you've deposited #{deposit_amount}"))
            print(translate("Transaction slip printed!"))
        elif decision == "no":
            continue
        else:
            print(translate("Invalid option, please enter (yes or no)"))

    elif text == translate("Check Balance"):
        print(translate(f"Your account balance is #{balance}"))

    elif text == translate("Exit"):
        print(translate("Goodbye, please take your card!"))
        break
