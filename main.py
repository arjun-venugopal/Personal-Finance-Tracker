import pandas as pd
import csv
from matplotlib import pyplot as plt
from datetime import datetime
from data_input import get_date, get_amount, get_category, get_description

class CSV:
    csv_file = "data.csv"
    columns = ['Date', 'Amount', 'Category', 'Comment']
    Time_format = "%d-%m-%Y"

    # Initialize the CSV file
    def initialize_csv(self):
        try:
            pd.read_csv(self.csv_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.csv_file, index=False)

    # Add data to the CSV
    def add_data(self, Date, Amount, Category, Comment):
        new_entry = {
            'Date': Date,
            'Amount': Amount,
            'Category': Category,
            'Comment': Comment
        }
        with open(self.csv_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.columns)
            writer.writerow(new_entry)
        print("Entry Added Successfully......✅")

    # Retrieve transactions between two dates
    def get_transactions(self, start_date, end_date):
        df = pd.read_csv(self.csv_file)
        df['Date'] = pd.to_datetime(df['Date'], format=self.Time_format)
        start_date = datetime.strptime(start_date, self.Time_format)
        end_date = datetime.strptime(end_date, self.Time_format)

        # Filter transactions within the date range
        mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No Transactions Found in the given date range")
        else:
            print(f'The Transactions between {start_date.strftime(self.Time_format)} to {end_date.strftime(self.Time_format)}:')
            print(filtered_df.to_string(index=False, formatters={"Date": lambda x: x.strftime(self.Time_format)}))

            # Calculate totals based on Category
            total_income = filtered_df[filtered_df['Category'] == "Income"]['Amount'].sum()
            total_expense = filtered_df[filtered_df['Category'] == 'Expense']['Amount'].sum()

            # Display summary
            print("\n----------------Summary----------------")
            print(f"Total Income  💵🔺:  ${total_income:.2f}")
            print(f"Total Expense 💵🔻: ${total_expense:.2f}")
            print(f"Net Savings 💰: ${(total_income - total_expense):.2f}")

        return filtered_df


# Function to add a new transaction
def add():
    csv_handler = CSV()  
    csv_handler.initialize_csv()
    # Collect transaction details
    Date = get_date("Enter Date of Transaction (dd-mm-yyyy) or press enter for today's date: ", allow_default=True)
    Amount = get_amount()
    Category = get_category()
    Comment = get_description()
    csv_handler.add_data(Date, Amount, Category, Comment)


def main():
    csv_handler = CSV() 
    while True:
        print("\n----------------Main Menu----------------")
        print("1. Add New Transaction")
        print("2. View Transactions Summary")
        print("3. Exit")
        
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        
        if choice == 1:
            add()
        elif choice == 2:
    
            start_date = get_date("Enter start date (dd-mm-yyyy): ")
            end_date = get_date("Enter end date (dd-mm-yyyy): ")
            csv_handler.get_transactions(start_date, end_date)
        elif choice == 3:
            print("Exiting the program. Have a Good Day ❤️ ")
            break
        else:
            print("Invalid choice. Please select from the options above.")



if __name__ == "__main__":
    main()
