# Swan Discord Bot

Swan is a Discord bot developed using discord.py and SQLAlchemy. Its primary functionality is distributing a certain amount of test coins (a custom EVM-based cryptocurrency) in specific channels to users.

## Features

- Distributing test coins.
- Recording each user's number of test coins and the claim time.

## Installation

1. Clone this repository
    
    ``git clone https://github.com/filswan/swan-discord-bot.git``

2. Install dependencies

    ``pip install -r requirements.txt``
    ``pip install python-dotenv``

3. Create a `.env` file by following the `.env.example` file

4. Run the bot

    ``python main.py``

## Usage

Type the command `!claim` in Discord to claim test coins. Each user is allowed to claim once every six hours.

## License

This project is licensed under the terms of the MIT license. For more details, see the [LICENSE](LICENSE) file.
