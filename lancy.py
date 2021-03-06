import discord, asyncio, logging, requests, sys, json
import marco_protection

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log' , encoding='utf-8' , mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(handler)

client = discord.Client()
protection = marco_protection.Protection()

def open_config_file():
        try:
            with open('config.arthur','r') as json_file:
                decoded = json.load(json_file)
            return decoded
        except Exception as e:
            print('Exception occured in open_config_file() as '+ e)
            return e

data = open_config_file()
token = data['Token']
yandex_tr = data['Yandex_tr']
yandex_di = data['Yandex_di']

async def get_eggs():
        try:
            with open('eggs.table','r') as f:
                eggs = json.load(f)
            return eggs
        except Exception as e:
            print(e)

async def add_egg(keyword,egg):
        try:
            new_egg = {'text': keyword, 'value': egg}
            data = await get_eggs() 
            data.append(new_egg)           
            with open('eggs.table','w') as eggs:
                json.dump(data, eggs)
            return True
        except Exception as e:
            return False

async def get_oauth_url():
         try:
            data = await client.application_info()
         except Exception as e:
            return "Couldn't retrieve invite link.Error: {}".format(e)
         return discord.utils.oauth_url(data.id)

async def connection_details():
        try:
            data = 'Server: ', len(client.servers) , 'Users: ' , len(set(client.get_all_members()))
        except Exception as e:
            return 'Could not retrieve server information' , e;
        return data

async def get_languages():
       try:
            output = 'List of supported languages can be found here:\n'
            output = 'https://tech.yandex.com/translate/doc/dg/concepts/api-overview-docpage/#languages'
            return output
       except Exception as e:
            return 'Something went wrong! Drastically wrong. I am the bot and I do not even know how to diagnose this. Tell my master to restart me.'

async def check_code(code1,code2):
      try:
        with open('codes.aurthor', 'r') as codes:
            word_list = []
            for line in codes:
                word_list.append(line.strip('\n\r'))

        if code1 in word_list and code2 in word_list:
            return True
        else:
            return False
      except Exception as e:
            return e
 
async def get_definition(string):
       try:
            
            s1 = string[14:16]
            t1 = string[17:19]
            text = string[20:]
            if await check_code(t1, s1):
                url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?'
                url += 'key='+yandex_di
                url += '&lang='+s1+'-'+t1
                url += '&text='+text.replace(" ", "%20")
                print(url)
                r = requests.get(url)
                dictionary = json.loads(r.text)
                print(dictionary)
                output = "Word Entered: " + dictionary['def']['text'] + '\n'
                              
                translation = dictionary['def']['tr']
                for word in translation['text'].itervalues():
                    output += 'Translation: ' + word+'\n'

                for synonym in translation['syn'].itervalues():
                    output += 'Synonym of Traslation: ' + synonym['text'] + '\n'
                    output += '--------------------------------\n'
                       
                return output
       except Exception as e:
            print('Dictionary exception happened: ',e)

async def get_translate(string):
       try:
            
            t1 = string[16:18]
            s1 = string[13:15]
            if await check_code(t1, s1):
                url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
                url += 'key='+yandex_tr
                url += '&lang=' + s1 + '-' +t1
                url += '&text=' + string[18:].replace(" ", "%20")
                #print(url)
            
                r = requests.post(url)
                code = r.status_code
                if code == 200:
                    out = 'Success !'
                    print(out + '\nMessage: ' + r.text)
                    dictionary = json.loads(r.text)
                    text = ''.join(dictionary['text'])
                    return text
                elif code == 401:
                    print('Invalid API Key')
                    return 'Err..contact your server admin and tell him the bot says error code 401'
                elif code == 402:
                    print('Blocked API Key')
                    return 'Err..contact your server admin and tell him the bot says error code 402'
                elif code == 404:
                    out = 'Exceeded the daily limit on the amount of translated text'
                    print(out)
                    return out
                elif code == 413:
                    out = 'Exceeded maximum text size'
                    print(out)
                    return out
                elif code == 422:
                    out = 'The text cannot be translated'
                    print(out)
                    return out
                elif code == 501:
                    out = 'The Specified translation direction is not supported'
                    return out
                else: 
                    return 'Wait what.. this is not right - where is the text to be translated? Oh I think something is wrong with the connection to Yandex servers~_~'
            else:
                    return 'Re-check your language codes. Somethings not right.'

       except Exception as e:
            return 'Exception: ' + e
       
async def get_all_channels():
    try:
      channels = client.get_all_channels()
      return channels
    except Exception as e:
        return 'Exception: ', e

async def find_in_json(word, jason):
    for words in jason:
        if words['text'] in word:
            return words['value']
    return " "

@client.event
async def on_message(message):
    msg = message.content.lower()
    if msg.startswith(';;;translate'):
        sent_message = await client.send_message(message.channel, 'Translating...')
        var = protection.is_translated(msg[18:])
        if var:
            translated = await protection.get_translated(msg[18:])
        else:
            translated = await get_translate(msg)
            await protection.add(msg[18:], translated)

        eggs = await get_eggs()
        emoji = await find_in_json(msg[18:], eggs)
        translated = translated +"    "+ emoji
        await client.edit_message(sent_message, translated, embed=None)

    if msg.startswith(';;;eggs'):
        print(msg[8:11])
        if msg[8:11] == 'add':
            print('Adding egg')
            add = msg[12:]
            egg = add[add.find(',')+1:]
            keyword = add[:add.find(',')-1]
            if await add_egg(keyword,egg):
                sent_message = await client.send_message(message.channel, 'Egg Added!')
            else:
                sent_message = await client.send_message(message.channel, 'Hmm.. Something happened and now it is broken')           
        elif msg[8:] in 'remove':
            remove = msg[14:]
         
    if message.content.startswith(';;;help'):
        string = 'SirLancelot v1.0 \n Some Commands: \n' 
        string += ';;;translate [param_translate_from, param_translate_to]\nlet the bot know you want something translated.\n'
        string += 'The paramater we use is ISO 639-1 Code for Language codes.\nFind all language codes here:\n'
        string += 'https://www.loc.gov/standards/iso639-2/php/code_list.php\n'
        string += '--------------------------------------\n'
        string += 'Example: ;;;translate en,fr\n'
        string += '--------------------------------------\n'
        string += ';;;help : Get this message.\n'
        string += '--------------------------------------\n'
        string += ';;;supported\n'
        string += 'Gives list of supported languages\n'
        string += '--------------------------------------\n'
        string += 'Some Limitations:\n'
        string += '  -The API uses Yandex translation (because google are money hungry monkeys)\n'
        string += '  -Sir Lancelot cannot convert more than 1Million characters per day and 10Million per month\n'
        string += '  -Sir Lancelot is a knight and does not take nonsense from anyone\n'
        await client.send_message(message.channel, string)
 
    if message.content.startswith(';;;supported'):
        await client.send_message(message.channel, await get_languages())

    if message.content.startswith(';;;dictionary'):
        sent_message = await client.send_message(message.channel, 'Defining...')
        await client.edit_message(sent_message, new_content=await get_definition(message.content), embed=None)

@client.event
async def on_ready():
        print('Client logged in'.format(client.is_logged_in))
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print(await connection_details())
        
@client.event
async def on_server_join():
        print('Server joined!')
        await client.change_presence(game=discord.Game(name='NoneOfYourBusiness'))

loop = asyncio.get_event_loop()
try:
      loop.run_until_complete(client.start(token))
except KeyboardInterrupt:
      loop.run_until_complete(client.logout())
      print('Logged out')
      # cancel all tasks lingering
finally:
      loop.close()
#client.run('Mjg2MjM3MjkyNDA0NjcwNDc2.C6P6Ug.NFWm0Qf4d2FmhIetjw2rePgi_V4')
