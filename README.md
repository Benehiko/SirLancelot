# SirLancelot
A Discord dictionary/translation bot that connects to translate.yandex (because google isn't free)

Sir Lancelot runs on Python 3.5

Some Libraries Sir Lancelot uses:
- [Discord.py](https://github.com/Rapptz/discord.py)
- Asyncio
- libffi-dev or libffi-devel (required by Discord.py)
- json
- logging
- requests

Installation:

  Current Supported OS:
  
    Anything running off of the Ubuntu framework using `apt install`
  
  Go to directory where the repository was cloned to. Open terminal in that directory and type:
    `./install.sh`
    
  It will ask for your sudo password as it will be installing the above packages.
  Let it run through and then test by running configure.py.
  If it gives errors on modules mising -- manually install them.
  
  Note: This bot runs on python3.5 --The install.sh script installs (upgrades) python3.5 with python3 pip.
  
Purpose of Bot:
  Initially I thought it would be fun to sit in discord and see what crazy translations you could come up with.
  But then it struck me - why not get a bot to be a grammar-nazi on discord. It would be so cool!
  Eventually even recording chats to store in a database for learning purposes - the bot would then start learning how people 
  spoke to each other on discord and then start replying in the same way 
  > (Like a mini AI)
  
Versions:

  v1.0: 
  
    First version to be released on March 11 2017.
    What can the bot do in this version?
      -Translate a sentence to the suggested languge
      
Commands:

    ;;;translate (lang from, lang to) [Sentence]
    
Translates a sentence by using the yandex API.
     eg. ;;;translate en,fr hi there!

    ;;;help
    
Prints the command list
    
    ;;;support
    
Gives a url to the supported languages and their codes
    
 Extra Notes:
 
  Yandex only supports up to 1,000,000 characters per day and 10,000,000 characters per month.
  Because of this - each server using this bot will need to create their own Yandex account for the API key.
  Getting started on Yandex: https://tech.yandex.com/translate/
  
 
 How to use this bot?
  
  First run the configure.py script using python3.5
  A menu will appear asking for initial details such as adding the bot to a server and the api key for Yandex.
  After this is done you can run the lancy.py script using python3.5.
  The bot should then be connected to the added server and using the api key for Yandex.
