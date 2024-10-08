Sure, here's the updated README with the Koyeb deploy button and some added emojis:
# Telegram Shop Bot 🛍️

This repository contains the code for a Telegram Shop Bot built using Python and the `python-telegram-bot` library.

## Features ✨

*   Product browsing (free and paid shops) 🛒
*   User profiles 👤
*   Referral system 🤝
*   Deposit functionality 💰
*   Admin panel for bot management ⚙️
*   MongoDB integration for data storage 💾

## Getting Started 🚀

### Prerequisites 📋

*   Python 3.9 or higher 🐍
*   A Telegram bot token (get one from BotFather) 🤖
*   A MongoDB database 🗄️

### Installation 🛠️

1.  Clone the repository:
    ```bash
    git clone [https://github.com/sayyedkashifali/Telegramshop.git](https://github.com/sayyedkashifali/Telegramshop.git)
    ```

2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Configure the bot:
    *   Update `TOKEN` in `bot.py` with your bot token.
    *   Set up your MongoDB connection string in `database.py`.
    *   Configure other settings like `REQUIRED_CHANNEL` and `LOG_CHANNEL_ID` in `bot.py`.

4.  Deploy the bot:
    *   You can deploy the bot to Koyeb using the button below:

        [![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?name=tg-selling&type=git&repository=sayyedkashifali%2FTelegramshop&branch=main&builder=buildpack&run_command=python+bot.py&env%5BAPI_HASH%5D=de1077f45e29e6abebcd2b9dd196be1d&env%5BAPI_ID%5D=27317700&env%5BBOT_TOKEN%5D=8085073135%3AAAEpv0Vt56MPYpYAVmyjwmwUvGBcUFIzs6E&ports=8080%3Bhttp%3B%2F)

    *   Alternatively, you can deploy it to any other platform that supports Python and webhooks.

### Usage 🎮

1.  Start the bot by sending the `/start` command.
2.  Use the buttons in the main menu to navigate through the bot's features.
3.  Access the admin panel using the `/admin` command.

## Contributing 🤝

Contributions are welcome! Feel free to open issues or submit pull requests.

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

