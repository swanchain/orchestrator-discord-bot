# Swan Discord Bot

Swan is a Discord bot developed using discord.py and SQLAlchemy. It's primary functionality is to distribute a certain amount of test coins (a custom EVM-based cryptocurrency) in specific channels to users.

## Features

- Distributing test coins.
- Recording the amount of test coins each user claims and the time of claim.

## Installation

1. Clone this repository

``git clone https://github.com/your_username/swan-discord-bot.git``

2. Install dependencies

``pip install -r requirements.txt``

3. Create a `.env` file and add your database URL and Discord bot token:

``DATABASE_URL=postgresql://username:password@localhost/discord_bot
BOT_TOKEN=your-bot-token``

4. Run the bot

``python main.py``

## Usage

Type the command `!claim` in Discord to claim test coins. Each user is allowed to claim once every six hours.

## License

This project is licensed under the terms of the MIT license. For more details, see the [LICENSE](LICENSE) file.

## Contact

If you have any questions or suggestions, feel free to open an issue or contact me through the following means:

- Email: your_email@example.com
- Discord: Your Discord ID
