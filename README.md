<<<<<<< HEAD
# PyDisaur demo
Official demo for Pydisaur, the fabulous Python URL Shortener who work with Discord!
=======
# PyDisaur
A fabulous Python URL Shortener who work with Discord!

[Demo](https://pydisaur.glitch.me/)

## Install

### Self-host
#### Discord steps
1. Go to [Discord Developpers site](https://discord.com/developers/applications).
2. Create an new app.
3. Go to OAuth section.
4. Add in Redirects section the callback URL (root URL + /callback)
5. Grab Client ID and Client Secret.

#### Terminal steps
1. Launch a terminal.
2. Type these commands (thats assumes you have Python 3 and PIP installed):
```
git clone https://github.com/Stylix58/pydisaur.git
cd pydisaur
pip3 install -r requirements.txt
```
3. Create a `.env` file with this content:
```
CLIENT_ID=ID of your Discord OAuth app
CLIENT_SECRET=Secret token of your Discord OAuth
ROOT_URL=Real URL of your hosted instance, wihout "/" at the end
```
**If you don't have created `.env`, PyDisaur will look for environnements variables instead!** (note: use the same envs than for `.env` but add `PYDISAUR_` behind every env.)

4. For launch it, type in your terminal `python3 main.py [PORT (by default, it is port 5000)] [true or false if your app use http or no (by default, it is true)]` and go to the given address.

## License
This application is licensed as [MIT License](./LICENSE).
>>>>>>> 40287c720fe8f6eb314432820b4283a1abb68702
