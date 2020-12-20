## TikTokCord ♪
Automatically send in-app videos of tiktoks sent in any chat!

### Installation ⚙️

1. Download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Create a bot at [https://discord.com/developers/applications/](https://discord.com/developers/applications/) (Make sure you enable all intents)
3. Clone the repo
   ```sh
   git clone https://github.com/saucesteals/TikTokCord.git
   ```
4. CD into the cloned repo
   ```sh
   cd TikTokCord
   ```
5. Install requirements
   ```sh
   pip/pip3 install -r requirements.txt
   ```
6. Fill in the template in `env.example`
7. Rename `env.example` to `.env`
8. Start it!
   ```sh
   python/python3 main.py
   ```


#### Optional - Direct message replies (Looks cooler 😎)
1. Clone the latest build of discord.py
   ```sh
   git clone https://github.com/Rapptz/discord.py.git
   ```
2. CD into the cloned repo
   ```sh
   cd discord.py
   ```
3. Install the latest build with pip
   ```sh
   pip/3 install -U .
   ```
4. Go back and restart the bot!


## Usage

* To enable or disable the bot in a server, use the command `!toggle` (or with a custom prefix if you set one during installation).

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## License

Distributed under the MIT License. See `LICENSE` for more information.