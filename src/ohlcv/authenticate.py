def authenticate_alpaca(env_path):

    api_key = input("Enter alpaca-py API key: ")
    secret_key = input("Enter alpaca-py SECRET key: ")

    with open (env_path + '/.env', 'w') as f:
        f.write(f'API_KEY={api_key}\n')
        f.write(f'SECRET_KEY={secret_key}\n')

    print('.env file created successfully')