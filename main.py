class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class ATMMachine:
    def __init__(self, curr_user=User("test", "test"), pin=None):
        self.pin_trials: int = 0
        self.balance: float = 0.0  # Float should ideally not be used for money! this is just a dummy
        self.pin: str = pin
        self.blocked: bool = False
        self.user = curr_user
        self.logged_in = False

    @classmethod
    def menu(cls):
        menu = ("Check balance", "Deposit", "Withdraw", "EXIT")
        return f"{menu}"

    def set_pin(self, pin: str):
        self.pin = pin
        return "Successful"

    def validate_pin(self, input_pin: str) -> [str, bool]:
        if self.pin_trials >= 3:
            self.blocked = True
            return "Number of pin attempts exceeded, Account blocked", False
        if self.blocked:
            return "Card blocked", False
        if input_pin == self.pin and not self.blocked:
            self.logged_in = True
            return f"{ATMMachine.menu()}", True
        elif input_pin != self.pin and not self.blocked:
            self.pin_trials += 1
            trials_left = 3 - self.pin_trials
            return f"Wrong pin, try again. {trials_left} trials left", False

    def check_balance(self) -> str:
        return f"Your balance is {self.balance}"

    def deposit_money(self, amount) -> str:
        self.balance += amount
        return f"Successful deposit, your current balance is {self.balance}"

    def withdraw_money(self, amount) -> str:
        if self.balance < amount:
            return "Insufficient balance!"
        else:
            self.balance -= amount
            return f"Successful withdrawal of {amount}"

    def check_prompt(self, user_choice):
        if user_choice == "check balance":
            print(self.balance)
        elif user_choice == "deposit":
            amount_input = float(input(f"How much are you depositing? "))
            print(self.deposit_money(amount_input))
        elif user_choice == "withdraw":
            amount_input = float(input(f"How much are you withdrawing? "))
            print(self.withdraw_money(amount_input))
        elif user_choice == "exit":
            print("Bye, Thank you for banking with us")


if __name__ == '__main__':
    user = User("Haleemah", "Badmus")
    atm = ATMMachine(user, "9999")
    pin_input = input(f"Welcome to HB ATM, please enter your pin: ")

    message, valid = atm.validate_pin(pin_input)
    while not valid:
        if atm.blocked:
            print(message)
            break
        pin_input = input(f"{message}, please re-enter your pin: ")
        message, valid = atm.validate_pin(pin_input)

    if valid:
        operation = input(f"What do you want to do today? {ATMMachine.menu()} ")
        user_choice = operation.lower()
        atm.check_prompt(user_choice)
        while user_choice != "exit":
            user_choice = input(f"What do you want to do next? {ATMMachine.menu()} ")
            user_choice = user_choice.lower()
            atm.check_prompt(user_choice)
