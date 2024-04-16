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
    while True:
        print(translate("Do you want to print your transaction slip?"))
        choice = ["yes", "no"]
        for index, items in enumerate(choice, 1):
            msg = f"{index}. {items}"
            print(translate(msg))
        decision = input(translate("Make a choice using the index digits: "))
        if decision == "1":
            document_folder = os.path.expanduser("~/Documents")
            file_path = os.path.join(document_folder, f"transaction_slip_{machine_type}.txt")
            with open(file_path, "w") as file:
                file.write(transaction)
            print(translate(f"Transaction slip saved to {file_path}"))
            print(translate("Transaction slip printed!"))
            break
        elif decision == "2":
            break
        else:
            print(translate("Invalid option, please enter (yes or no)"))


def translate(sentence):
    return translator.translate(sentence, dest=language).text


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


def withdraw():
    global balance
    if withdraw_amount > balance:
        print(translate("Insufficient balance."))
    else:
        balance -= withdraw_amount
        print(translate(f"Congratulations, you've withdrawn #{withdraw_amount}"))


def transfer():
    global balance
    if transfer_amount > balance:
        print(translate("Insufficient balance."))
    else:
        balance -= transfer_amount
        print(translate(f"Congratulations, you've transferred #{transfer_amount}"))


def deposit():
    global balance
    balance += deposit_amount
    print(translate(f"Congratulations, you've deposited #{deposit_amount}"))


while True:
    print(translate("Select a transaction"))
    menu_items = ["Withdraw", "Transfer", "Deposit", "Check Balance", "Exit"]
    for i, item in enumerate(menu_items, 1):
        message = f"{i}. {item}"
        print(translate(message))

    text = input(translate("Make a choice using the index digits: "))
    if text == "1":
        withdraw_amount = get_valid_amount(translate("How much do you want to withdraw?: "))
        withdraw()
        print_transaction_slip(translate(f"Congratulations, you've withdrawn #{withdraw_amount}"))

    elif text == "2":
        transfer_amount = get_valid_amount(translate("How much do you want to Transfer?: "))
        transfer()
        print_transaction_slip(translate(f"Congratulations, you've transferred #{transfer_amount}"))

    elif text == "3":
        deposit_amount = get_valid_amount(translate("How much do you want to Deposit?: "))
        deposit()
        print_transaction_slip(translate(f"Congratulations, you've deposited #{deposit_amount}"))

    elif text == "4":
        print(translate(f"Your account balance is #{balance}"))

    elif text == "5":
        print(translate("Goodbye, please take your card!"))
        break



# from googletrans import Translator
# import os
#
# class ATM:
#     def __init__(self):
#         self.language = "English"
#         self.account_balance = 10000.0  # Initial account balance
#         self.translator = Translator()
#
#     def translate(self, sentence):
#         return self.translator.translate(sentence, dest=self.language).text
#
#     def get_valid_amount(self, number):
#         while True:
#             try:
#                 amount = float(input(number))
#                 if amount <= 0:
#                     print(self.translate("Amount must be greater than zero."))
#                 else:
#                     return amount
#             except ValueError:
#                 print(self.translate("Invalid input. Please enter a valid amount."))
#
#     def print_transaction_slip(self, transaction):
#         while True:
#             print(self.translate("Do you want to print your transaction slip?"))
#             choice = ["yes", "no"]
#             for index, items in enumerate(choice, 1):
#                 msg = f"{index}. {items}"
#                 print(self.translate(msg))
#             decision = input(self.translate("Make a choice using the index digits: "))
#             if decision == "1":
#                 document_folder = os.path.expanduser("~/Documents")
#                 file_path = os.path.join(document_folder, f"transaction_slip.txt")
#                 with open(file_path, "w") as file:
#                     file.write(transaction)
#                 print(self.translate(f"Transaction slip saved to {file_path}"))
#                 print(self.translate("Transaction slip printed!"))
#                 break
#             elif decision == "2":
#                 break
#             else:
#                 print(self.translate("Invalid option, please enter (yes or no)"))
#
#     def withdraw(self):
#         amount = self.get_valid_amount(self.translate("How much do you want to withdraw?: "))
#         if amount <= self.account_balance:
#             self.account_balance -= amount
#             print(self.translate(f"Congratulations, you've withdrawn #{amount}"))
#             self.print_transaction_slip(self.translate(f"Congratulations, you've withdrawn #{amount}"))
#         else:
#             print(self.translate("Insufficient balance."))
#
#     def transfer(self):
#         recipient = input(self.translate("Enter recipient's account number: "))
#         amount = self.get_valid_amount(self.translate("Enter amount to transfer: "))
#         if amount <= self.account_balance:
#             self.account_balance -= amount
#             print(self.translate(f"Transfer of {amount} to {recipient} successful. Remaining balance: {self.account_balance}"))
#             self.print_transaction_slip(self.translate(f"Transfer of {amount} to {recipient} successful. Remaining balance: {self.account_balance}"))
#         else:
#             print(self.translate("Insufficient balance."))
#
#     def deposit(self):
#         amount = self.get_valid_amount(self.translate("Enter amount to deposit: "))
#         self.account_balance += amount
#         print(self.translate(f"Congratulations, you've deposited #{amount}. New balance: {self.account_balance}"))
#         self.print_transaction_slip(self.translate(f"Congratulations, you've deposited #{amount}. New balance: {self.account_balance}"))
#
#     def check_balance(self):
#         print(self.translate(f"Your account balance is #{self.account_balance}"))
#
#     def exit(self):
#         print(self.translate("Goodbye, please take your card!"))
#
#     def run(self):
#         while True:
#             print(self.translate("Select a transaction"))
#             menu_items = ["Withdraw", "Transfer", "Deposit", "Check Balance", "Exit"]
#             for i, item in enumerate(menu_items, 1):
#                 message = f"{i}. {item}"
#                 print(self.translate(message))
#
#             text = input(self.translate("Make a choice using the index digits: "))
#             if text == "1":
#                 self.withdraw()
#             elif text == "2":
#                 self.transfer()
#             elif text == "3":
#                 self.deposit()
#             elif text == "4":
#                 self.check_balance()
#             elif text == "5":
#                 self.exit()
#                 break
#
# # Create an instance of the ATM class and run the ATM system
# atm = ATM()
# atm.run()