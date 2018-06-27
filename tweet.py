#!/usr/bin/python3

import sys
import os
import webbrowser
import json
import tweepy


def main():
    auth = authenticate()

    text = ' '.join(sys.argv[1:])

    if not len(text):
        print("Please specify text to tweet.")
        return

    api = tweepy.API(auth)
    api.update_status(text)


def authenticate():
    path = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(path, 'config.json')

    if os.path.isfile(config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
    else:
        config = {}

    if not (config.get('api_key') and config.get('api_secret')):
        config['api_key'] = input('API Key: ')
        config['api_secret'] = input('API Secret: ')

        with open(config_file, 'w') as file:
            json.dump(config, file)

    auth = tweepy.OAuthHandler(config['api_key'], config['api_secret'])

    if config.get('access_token') and config.get('access_secret'):
        auth.set_access_token(config['access_token'], config['access_secret'])
    else:
        url = auth.get_authorization_url()
        print('Please authorize the application, then enter your PIN below.')
        if not webbrowser.open(url, new=2):
            print(url)
            print(
                'Browser failed to open. If you are running WSL, add the '
                'following to your ~/.bashrc file, replacing BROWSER as '
                'appropriate:\n\n    export DISPLAY=:0\n    export BROWSER='
                '/mnt/c/Program\ Files/Opera/launcher.exe\n'
            )

        pin = input('PIN: ')
        auth.get_access_token(pin)

        config['access_token'] = auth.access_token
        config['access_secret'] = auth.access_token_secret

        with open(config_file, 'w') as file:
            json.dump(config, file)

    return auth


if __name__ == "__main__":
    main()
