import os

def main():
    print(f'The subscription id is: {os.environ.get("SUBSCRIPTION_ID")}')


if __name__ == "__main__":
    main()
