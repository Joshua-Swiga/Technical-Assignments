import csv
import time

class BudgetManager:

    monthly_income = 0.0
    
    def workflow(self):
        """
        Main workflow of the budget manager application.

        Prompts the user for an action and executes the selected action.

        :return: None
        """
        print ("Welcome to the budget manager!")
        print("What would you like to do?")
        print(
            "1.Log income details\n2.Log client details\n3.Make a transaction"
            )
            
        action = int(input("Enter action: "))
        if action == 1:
            self.log_income_details()
        elif action == 2:
            self.log_client_details()
        elif action == 3:
            self.make_transaction()
        else:
            print("Invalid action")

    def log_income_details(self):
        """
        Logs the income details of the user.

        This function is used to track the monthly income of the user. 
        It prompts the user to enter the monthly income, salary date and source of income. 
        The entered information is then written to a CSV file for future reference.

        Args:
            None

        Returns:
            None

        Raises:
            ValueError: If the income is not a positive number
        """

        print("Hello! This is your monthly income tracker")
        log_income_info = float(input("Enter monthly income: "))
        
        salary_date = input("Enter salary date: ")
        source_of_income = input("Enter source of income: ")

        if (log_income_info < 0) and (type(log_income_info) != float):
             raise ValueError(f"Amount must be a positive number: {log_income_info}")
        else:
            try:
                self.monthly_income = log_income_info

                with open("incomeDetails.csv", "a", newline='') as f:
                    csv_writer = csv.writer(f)
                    writting_attempt = csv_writer.writerow([
                        self.monthly_income,
                        salary_date,
                        source_of_income
                    ])
                    
                    try:
                        print("Please wait...")
                        time.sleep(1)
                        print("Income logged successfully")
                    except Exception as e:
                        print("There was an issue:", e)

            except Exception as e:

                print("There was an issue:", e)
        try:
            next_action = input("Do you want to make another transaction? (y/n): ")
            if next_action == "y":
                self.make_transaction()
            else:
                print("Goodbye!")
        except Exception as e:
            print("There was an issue:", e)


    def log_client_details(self):        
        """
        Logs client details into the budget.txt file. If the file does not exist, it will be created.
        If the file does exist, it will be overwritten.
        
        :raises ValueError: If the amount is not a positive number or if any of the fields (description, category, date) are empty.
        :return: None
        """
        try:
            description: str = str(input("Enter desription: "))

            while True:
                amount: float = float(input("Enter amount (Numeric values only): "))
                if (amount < 0) and (type(amount) != float):
                    raise ValueError(f"Amount must be a positive number: {amount}")
                break

            category: str = str(input("Enter category: "))
            date: str = str(input("Enter date: "))
            
            if description == "" or category == "" or date == "":
                raise ValueError("All fields are required")
        
        except ValueError as e:
            print(e)
        finally:
            print(f"{description} {amount} {category} {date}")
            try:
                with open("budget.csv", "w+") as f:
                    csv.writer(f).writerow([
                        description,
                        amount,
                        category,
                        date
                    ])
                       
                    print("Budget logged successfully")
            except Exception as e:
                print("There was an issue:", e)

            try:
                with open("budget.txt", "r") as f:
                    print(f.read())
            except FileNotFoundError as e:
                print("File not found:", e)


    def make_transaction(self):
        """
        Allows users to make a transaction and update their bank account balance. This function also logs the transaction details in a CSV file.

        Args:
            None

        Returns:
            None

        Raises:
            FileExistsError: If the incomeDetails.csv file does not exist
            ValueError: If the income, item purchased, price of item or person paying is not a positive number
        """
        income_details = []
        with open ("incomeDetails.csv", "r") as f:
            csv_reader = csv.reader(f)
            row_data = list(csv_reader)
            income_details = row_data
        bank_account_balance = float(income_details[0][0])

        print("Welcome! Please make a transaction")
        transaction_type = input("Enter transaction type: ")
        name_of_transaction = input("Enter name of transaction: ")
        item_purchased = input("Enter item purchased: ")
        price_of_item = float(input("Enter price of item: "))
        person_paying = input("Enter person paying: ")

        try:
            if (bank_account_balance > 0 and bank_account_balance >= float(price_of_item)):
                bank_account_balance -= float(price_of_item)
                
                with open("incomeDetails.csv", "w+", newline='') as f:
                    csv_writer = csv.writer(f)
                    income_details[0][0] = bank_account_balance  
                    csv_writer.writerow(income_details[0]) 

                with open("transactions.csv", "a+", newline='') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow([
                        transaction_type,
                        name_of_transaction,
                        item_purchased,
                        price_of_item,
                        person_paying
                    ])
            
                print("Transaction completed successfully")
            else:
                print("Insufficient funds. Transaction aborted.")
                return
 
        except Exception as e:
            print("There was an issue:", e)

        try:
            next_action = input("Do you want to make another transaction? (y/n): ")
            if next_action == "y" or next_action == "1":
                self.make_transaction()
            else:
                second_action = input("Do you want to view all transactions? (y/n): ")
                if second_action == "y":
                    self.view_all_transactions()
                else: 
                    print("Goodbye!")
        except Exception as e:
            print("There was an issue:", e)
        

    def view_all_transactions(self):
        """
        View all transactions

        Prints all transactions from transactions.csv to the console, with each
        transaction on a new line.

        Asks the user if they want to make another transaction afterwards.

        :return: None
        """

        with open ("transactions.csv", "r") as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                print("Transaction type:", row[0])
                print("Name of transaction:", row[1])
                print("Item purchased:", row[2])
                print("Price of item:", row[3])
                print("Person paying:", row[4])
            
            print("End of transactions")
            time.sleep(2)
        next_action = input("Do you want to make another transaction? (y/n): ")
        if next_action == "y":
            self.make_transaction()
        else:
            print("Goodbye!")
