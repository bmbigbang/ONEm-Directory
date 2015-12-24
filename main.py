# -*- coding: utf-8 -*-


from misc import finder,alphabet
from places import Directory
from helper import Helper
from options import Options,Chunks
from corrector import Corrector
from outline import Outline
 
class Main(object):
    def __init__(self):
        self.main = Corrector()
        self.match = ""
        self.commands = []
        self.option = Options()
        self.display = Chunks("")
        self.display.create_Chunks()
        self.last_Display = ""
        self.find = Chunks("")
        self.find.create_Chunks()
        self.table = Outline()

    def run(self):
        hlp = Helper();br=True;results={};resultsort=[];correcting = False
        while br:  
            if correcting:
                pass
            else:
                command = raw_input("SMS in: ")
            t,option,word = self.process(unicode(command))
            words = t[0];disting = t[1][-1]

            if option:
                self.option = option;self.match = word
                if len(self.display) > 0 :
                    self.last_Display = self.display
                self.display = Chunks(self.option.print_Options())
                self.display.create_Chunks(heading="By ({0}) Did you mean: ".format(word),
                           footing="Please choose.")
                print self.display.goto_Chunk(); continue
            
            if len(self.option)>0 and len(words[0])==1:
                ch = self.option.select_Option(words[0])
                if ch!=None and len(resultsort)==0:
                    self.main.correctedHistory[self.match]=self.option[ch][2]
                    disting = t[1][-2]; 
                    k = disting['tokens'].index(self.match)
                    disting['tokens'][k] = self.option[ch][2]
                    try:
                        k = disting['words'].index(self.match)
                        disting['words'][k] = self.option[ch][2]
                        words = disting['words']
                    except:
                        disting['words'].append(self.option[ch][2])
                        words = disting['words']
                    if self.option[ch][2] == "find":
                        word = "find";self.option = Options()
                    else:
                        self.option = Options();correcting = True
                        command = " ".join(disting['tokens']); continue    
            correcting = False
                               
            if word == "find" or "find" in words:
                del disting['tokens'][disting['tokens'].index("find")]
                if word == "find":
                    self.find = self.last_Display
                else:
                    self.find = self.display
                expand = self.find.find_Chunks(" ".join(disting['tokens']))
                if expand!=False:
                    self.find.chunk_list = expand
                    print self.find.goto_Chunk()
                else:
                    print "No results found"
                continue
            
            for k in range(len(words)):
                dirfin = finder(r'directory|places',words[k])   
                if dirfin.found():
                    del words[k]
                    if "list" in words:
                        self.display = Chunks(",".join(hlp.dirtypes()).replace("_"," "))
                        self.display.create_Chunks(heading="List of types of places:")
                        print self.display.goto_Chunk()
                        break
                    direc=Directory(words)
                    results,resultsort = direc.run(disting)
                    if results == None:
                        words=[];break
                    for i in resultsort:
                        self.option.add_Option(content="{0} - Ratings : {1}".format(i[0].encode('utf-8'),str(i[1])))
                    self.display = Chunks(self.option.print_Options())
                    self.display.create_Chunks(heading="Available places found nearby:",
                              footing="Please choose an option. ")
                    print self.display.goto_Chunk()
                    words = [];break
                if len(self.option)>0 and len(words[k])==1:
                    ch = self.option.select_Option(words[k])
                    if ch!=None and len(resultsort)>0:
                        text = "{0} - Ratings : {1}".format(resultsort[ch][0],resultsort[ch][1])
                        text += "\n" +" Telephone Number: " + results[resultsort[ch][0]][1]
                        text += "\n Address: "+results[resultsort[ch][0]][0]
                        self.display = Chunks(text)
                        self.display.create_Chunks()
                        print self.display.goto_Chunk()
                        self.option = Options();continue
                
                outfin = finder(r'outline',words[k])
                if outfin.found():
                    del words[k]
                    with open("textblock.txt","rb") as f:
                        textblock= f.read().decode("string_escape")
                    for i in range(len(textblock)):
                        if textblock[i:i+2] == "\u":   
                            textblock= textblock[:i]+unichr(int(textblock[i+2:i+6],base=16)).encode("utf-8")  +textblock[i+6:]
                    f.close()
                    self.table.add_TxtBlock(textblock)
                    if self.table.run(words,disting['numbers']) != False:
                        self.display = self.table.run(words,disting['numbers'])
                        print self.display.goto_Chunk(); break
                
                exifin = finder(r'exit',words[k])
                if exifin.found():
                    br=False;words=[];break   
                helpfin = finder(r'help',words[k])
                if helpfin.found():
                    print hlp;words=[];break
                
                if "next" in words[k]:
                    print self.display.next_Chunk(); break
                
                if "goto" in words[k]:
                    try:
                        n = disting['numbers'][0]
                        num = int(n)
                    except:
                        num = 1000
                    print self.display.goto_Chunk(num); break

    def process(self,command):
        opts = [];self.main.disting(command)
        for i in self.main.cur()['words']+self.main.cur()['splits']:
            for j in self.main.match(i):
                if j[0]=='None':
                    continue
                if j[1]==0:
                    try:
                        k = self.main.cur()['words'].index(i)
                        self.main.cur()['words'][k] = j[0]
                    except:
                        self.main.cur()['words'].append(j[0])
                    continue
                        
                if opts == []:
                    opts = Options()
                opts.add_Option(content="{0}".format(j[0]))
            
            if opts:
                return [self.main.cur()['words'],self.main.history],opts,i
                
        return [self.main.cur()['words'],self.main.history],opts,""
        
test3 = Main()
test3.run()





        
