# telegram-messages-forwarder
Copy all messages from your favorite public to private channel.

## Installation
To install this script you have to download project and install requirements:

### Linux
```
git clone https://github.com/dzikot/telegram-messages-forwarder
cd telegram-messages-forwarder
pip install -r requirements.txt
python forwarder.py
```

## Obtain standalone telegram app API credentials
- Login to https://my.telegram.org/
- Select `API development tools` link
- Create standalone application
- Copy app_id and app_hash

## Usage
> You need both App api_id and App api_hash to use script.

#### Environment variables
You could set API_ID and API_HASH environment variables to prevent entering API credentials manually.

#### Start
After starting script you will be prompted:
- To enter your Telegram APP credentials (if no environment variables found)
- Your account phone and then code sent to you by Telegram

forked from https://github.com/gurland/telegram-delete-all-messages