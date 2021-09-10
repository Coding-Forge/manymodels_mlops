import os
from ml_service.utils.env_variables import Env

def main():
    e=Env()

    print(f'The subscription id is from using the .env: {e.subscription_id}')


if __name__ == "__main__":
    main()
