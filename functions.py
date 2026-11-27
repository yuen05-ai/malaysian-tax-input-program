import csv
import math
from pathlib import Path

import pandas as pd
# Keep both CSV files in the same folder as this program.
folder = Path(__file__).parent
users_file = folder / "users.csv"
tax_file = folder / "tax_records.csv"

tax_columns = [
    "User ID",
    "Test Case ID",
    "Year of Assessment",
    "Annual Income",
    "Total Tax Relief",
    "Chargeable Income",
    "Tax Before Rebate",
    "Tax Rebate",
    "Final Tax Payable"
]

# Each row contains a test case ID, annual income, and total relief.
test_cases = [
    ["T01", 9000, 9000],
    ["T02", 40000, 9000],
    ["T03", 65000, 14000],
    ["T04", 120000, 18000],
    ["T05", 83000, 12000]
]


def valid_ic(ic_number):
    #Check that the IC number contains exactly 12 digits.
    if len(ic_number) != 12:
        return False

    for character in ic_number:
        if character not in "0123456789":
            return False

    return True


def read_users():
    #Read registered users into a list of rows.
    try:
        with open(users_file, "r", newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))
            return rows[1:]  # Skip the header.
    except FileNotFoundError:
        return []


def register_user(user_id, ic_number):
    #Check the details and save a new user.
    if user_id == "":
        return "User ID cannot be empty."

    if not valid_ic(ic_number):
        return "Invalid IC number. Enter exactly 12 digits."

    for row in read_users():
        if row and row[0] == user_id:
            return "User ID already exists."

    with open(users_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(["User ID", "IC Number"])

        writer.writerow([user_id, ic_number])

    return "Registration successful.To log in, use the last 4 digits of your IC number as your password."


def login_user(user_id, password):
    #Check the User ID and the last four digits of its IC.
    for row in read_users():
        if len(row) == 2:
            saved_id = row[0]
            saved_ic = row[1]

            if saved_id == user_id and valid_ic(saved_ic):
                return password == saved_ic[-4:]

    return False


def read_amount(prompt):
    #Keep asking until the user enters a valid nonnegative amount.
    while True:
        try:
            amount = float(input(prompt))

            if math.isfinite(amount) and amount >= 0:
                return round(amount, 2)

        except ValueError:
            pass

        print("Enter a valid amount of 0 or more, for example 40000.50.")


def calculate_tax(income, relief):
    """Calculate the YA 2026 tax amounts using the assignment rules."""
    chargeable = round(max(0, income - relief), 2)

    # Each row contains the upper limit and tax rate for one band.
    bands = [
        [5000, 0.00],
        [20000, 0.01],
        [35000, 0.03],
        [50000, 0.06],
        [70000, 0.11],
        [100000, 0.19],
        [400000, 0.25],
        [600000, 0.26],
        [2000000, 0.28]
    ]

    tax = 0
    lower_limit = 0

    for upper_limit, rate in bands:
        amount_in_band = min(chargeable, upper_limit) - lower_limit

        if amount_in_band > 0:
            tax = tax + amount_in_band * rate

        lower_limit = upper_limit

    if chargeable > 2000000:
        tax = tax + (chargeable - 2000000) * 0.30

    tax = round(tax, 2)
    rebate = 0

    if chargeable <= 35000:
        rebate = 400

    final_tax = round(max(0, tax - rebate), 2)

    return [chargeable, tax, rebate, final_tax]


def build_tax_record(user_id, test_id, income, relief):
    #Put the values in a list, then convert it to a dictionary.
    tax_values = calculate_tax(income, relief)
    values = [user_id, test_id, "YA 2026", income, relief] + tax_values

    record = {}
    for index in range(len(tax_columns)):
        record[tax_columns[index]] = values[index]

    return record


def save_tax_records(records):
    #Convert a list of dictionaries to a DataFrame and append to CSV.
    table = pd.DataFrame(records, columns=tax_columns)

    write_header = True
    if tax_file.exists() and tax_file.stat().st_size > 0:
        write_header = False

    table.to_csv(
        tax_file,
        mode="a",
        header=write_header,
        index=False,
        float_format="%.2f"
    )


def display_record(record):

    #Display one tax record with monetary amounts in RM.
    print("\nUser ID:", record["User ID"])
    print("Year of Assessment:", record["Year of Assessment"])

    if record["Test Case ID"] == "":
        print("Calculation type: Personal")
    else:
        print("Test Case ID:", record["Test Case ID"])

    # The monetary columns start at index 3.
    for column in tax_columns[3:]:
        amount = float(record[column])
        print(column + ": RM", format(amount, ",.2f"))


def view_tax_records(user_id):
    #Display the saved records for the logged-in user.
    try:
        table = pd.read_csv(
            tax_file,
            dtype=str,
            keep_default_na=False
        )
    except (FileNotFoundError, pd.errors.EmptyDataError):
        print("No tax records have been saved yet.")
        return

    user_records = table[table["User ID"] == user_id]

    if user_records.empty:
        print("You have no saved tax records.")
        return

    for record in user_records.to_dict("records"):
        display_record(record)