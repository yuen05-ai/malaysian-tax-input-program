import functions
def tax_menu(user_id):
    #Show the tax menu after a successful login.
    while True:
        print("\nMalaysian Tax Input Program (YA 2026)")
        print("1. Calculate and save my tax")
        print("2. View my saved tax records")
        print("3. Run and save the five test cases")
        print("4. Log out")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            income = functions.read_amount("Enter annual income (RM): ")
            relief = functions.read_amount("Enter total tax relief (RM): ")

            # A blank Test Case ID means this is a personal calculation.
            record = functions.build_tax_record(user_id, "", income, relief)
            functions.display_record(record)
            functions.save_tax_records([record])
            print("\nTax record saved.")

        elif choice == "2":
            functions.view_tax_records(user_id)

        elif choice == "3":
            records = []

            for test_id, income, relief in functions.test_cases:
                record = functions.build_tax_record(
                    user_id, test_id, income, relief
                )
                records.append(record)
                functions.display_record(record)

            functions.save_tax_records(records)
            print("\nFive test cases saved.")

        elif choice == "4":
            print("Logged out.")
            break

        else:
            print("Invalid choice. Enter 1, 2, 3, or 4.")


def main():
    """Show the welcome menu and handle registration and login."""
    while True:
        print("\nWelcome to the Malaysian Tax Input Program")
        print("1. Register")
        print("2. Log in")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                user_id = input("Enter a new User ID: ").strip()
                ic_number = input("Enter a 12-digit IC number: ").strip()

                message = functions.register_user(user_id, ic_number)
                print(message)

            elif choice == "2":
                user_id = input("Enter User ID: ").strip()
                password = input("Enter the last 4 digits of your IC number: ").strip()

                if functions.login_user(user_id, password):
                    print("Login successful.")
                    tax_menu(user_id)
                else:
                    print("Incorrect User ID or password.")

            elif choice == "3":
                print("Goodbye.")
                break

            else:
                print("Invalid choice. Enter 1, 2, or 3.")

        except OSError:
            print("Could not read or save the CSV file. Check if it is open in Excel.")
        except (ValueError, KeyError):
            print("The CSV file has invalid data or missing columns.")


if __name__ == "__main__":
    main()