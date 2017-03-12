import json, asyncio, os

class Protection(object):
    
    decoded = ""    

    def makeFile(self):
        with open('translations.arthur','w', encoding='utf8') as f:
                    json.dump([], f)

    def openFile(self):
        if os.path.isfile('translations.arthur') == False:
            self.makeFile()
        
        with open('translations.arthur', 'r', encoding='utf8') as usedData:
                    decoded = json.load(usedData) 
        
        return decoded

    def is_translated(self,sentence):
        usedData = self.openFile()
        for s in usedData:
            if sentence == s['text']:
                return True
            else:
                return False

    async def get_translated(self,sentence):
        decoded = self.openFile()
        for recieved in decoded:
            if recieved['text'] == sentence:
                print("Found the word ୧༼ ͡◉ل͜ ͡◉༽୨ :", recieved['tr'])
                return recieved['tr']

    async def add(self,sentence, translated):
        new_entry = {'text' : sentence, 'tr' : translated}
        print("Translated: ", translated)
        decoded = self.openFile()
        decoded.append(new_entry)
        with open('translations.arthur', 'w', encoding='utf8') as f:
            json.dump(decoded, f)
        
