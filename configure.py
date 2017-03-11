import discord, asyncio, logging, sys, traceback, json, os

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log' , encoding='utf-8' , mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(handler)

client = discord.Client()


def first_time():
          print('This is your first time running configure.py - Please follow the prompts')
          if os.path.isfile('config.arthur'):
                os.remove('config.arthur')
          token = input('Enter your bot token: ')
          yandex = input('Enter your yandex api key:')
          config_dump = {'Token': token, 'Yandex': yandex}
          a = json.dumps(config_dump)
          encoded = json.loads(a)
          with open('config.arthur' ,'w') as jd:
                json.dump(encoded, jd)
          print('File created. Reload the program')
          sys.exit(0)


def load_conf():
    if os.path.isfile('config.arthur') == False:
           first_time()

    try:
            with open('config.arthur', 'r') as json_data:
                decoded = json.load(json_data)
            return decoded
    except Exception as e:
            print('Exception caught while loading config file: ',e)
            
    sys.exit(1)  

print('Starting...')
while True:
        print('Do you want to load current settings or update?[load/update]')
        selection = input('Enter: ')
        if selection.lower() == 'update':
            first_time()
            break
        if selection.lower() == 'load':
            conf = load_conf()
            break

@asyncio.coroutine
async def get_oauth_url():
         try:
            data = await client.application_info()
         except Exception as e:
            return "Couldn't retrieve invite link.Error: {}".format(e)
         return discord.utils.oauth_url(data.id)

@asyncio.coroutine
async def add_server():
        try:
            url = await get_oath_url()
            client.oauth_url = url
            print('Follow this url to authenticate the bot:' + url)
        except Exception as e:
            print(e)

@asyncio.coroutine
async def leave_server():
    print(await list_server())
    selectedServer = input('Select a server.')
   
@asyncio.coroutine 
async def list_server():
        counter = 0
        for server in client.servers:
             counter += 1
             print(counter +'. '+server)

@asyncio.coroutine
async def change_username():
        try:
            name = input('Enter the new bot name: ')
            verify = input('Is this name fine: '+name+' ?[y/n]')
            if verify == 'y':
                argument = 'username='+name
                client.user.name = name
                await client.edit_profile(client.user.name)
                print('It has been done sire --> ', client.user.name)
        except Exception as e:
            print('Exception occured with :',e)
         
@client.event
async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('Client logged in'.format(client.is_logged_in))
        #client.login('Mjg2MjM3MjkyNDA0NjcwNDc2.C6QVpw.LjGummwnTicIgeI9-k0_1P_Nizg')
        menu = "Welcome to SirLancelot v1.0 configuration!\n Please choose an option:\n"
        menu += "1. Server Menu\n"
        menu += "2. Bot Menu\n"
        server = "~-Server Menu-~\n"
        server += "1. Add Server\n"
        server += "2. Remove Server\n"
        server += "3. List Connected Servers\n"
        bot = "~-Bot Menu-~\n"
        bot += "1. Change Username"
        
        print(menu)
        var = input("")
        if var == '1':
            print(server)
            switch_server(input(""))
        elif var == '2':
            print(bot)
            switch_bot(input(""))
                      
def switch_server(arg):
    switcher = {
        '1': await add_server(),
        '2': await leave_server(),
        '3': await list_server()
    }      
    func = switcher.get(arg)
    return func()
         
def switch_bot(arg):
    switcher = {
        '1':change_username(),
    }
    func = switcher.get(arg)
    return func


loop = asyncio.get_event_loop()
try:
      loop.run_until_complete(client.start(conf['Token']))
except KeyboardInterrupt:
      loop.run_until_complete(client.logout())
      print('Logged out')
      # cancel all tasks lingering
finally:
      loop.close()
