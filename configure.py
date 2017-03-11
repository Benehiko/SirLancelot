import discord, asyncio, logging, sys, json, os, traceback

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log' , encoding='utf-8' , mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(handler)

client = discord.Client()
loop = asyncio.get_event_loop()

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


async def add_server():
        try:
            url = await get_oauth_url()
            client.oauth_url = url
            print('Follow this url to authenticate the bot:' + url + '\n')
        except Exception as e:
            print(e)


async def leave_server():
    servers = client.servers
    await list_server(servers)
    selectedServer = int(input('Select a server:'))
    counter = 1   
    for server in servers:
       if counter == selectedServer:
            print(server)
            client.leave_server(server)
       counter += 1

async def list_server(servers):
        server
        counter = 1
        for server in servers:
           print(counter,".",server)
           counter += 1
        print('\n')

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
         
async def switch_server(arg):
    switcher = {
        '1': add_server,
        '2': leave_server,
        '3': list_server
    }    
    func = switcher.get(arg)
    return await func()

async def switch_bot(arg):
    switcher = {
        '1':change_username
    }
    
    func = switcher.get(arg)
    return await func()

@client.event
async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('Client logged in'.format(client.is_logged_in))
        menu = "Welcome to SirLancelot v1.0 configuration!\nPlease choose an option:\n"
        menu += "1. Server Menu\n"
        menu += "2. Bot Menu\n"
        menu += "3. Exit\n"
        server = "~-Server Menu-~\n"
        server += "1. Add Server\n"
        server += "2. Remove Server\n"
        server += "3. List Connected Servers\n"
        bot = "~-Bot Menu-~\n"
        bot += "1. Change Username\n"
      
        while True: 
            print(menu)
            var = input("")
            if var == '1':
                serverOption = input(server)
                await switch_server(serverOption)
            elif var == '2':
                botOption = input(bot)
                await switch_bot(botOption)
            elif var == '3':
                print('Bot Logging off and shutting down...')
                raise KeyboardInterrupt
        

try:
      loop.run_until_complete(client.start(conf['Token']))
except KeyboardInterrupt:
      loop.run_until_complete(client.logout())
      print('Logged out')
      # cancel all tasks lingering
finally:
      loop.close()
      

