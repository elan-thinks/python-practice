print("Hello World")


def add(a, b):
    return a + b


def substract(a, b):
    return a - b


def main():
    print("🧮 Welcome to Simple Calculator!")
    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))

    print("Choose an operation: ")
    print("1. Add")
    print("2. Substract")
    choice = input("Enter 1 or 2 : ")

    if choice == "1":
        result = add(num1, num2)
        print(f"The result is {result}")
    elif choice == "2":
        result = substract(num1, num2)
        print(f"The result is {result}")
    else:
        print("❌ Invalid choice.")


if __name__ == "__main__":
    main()
