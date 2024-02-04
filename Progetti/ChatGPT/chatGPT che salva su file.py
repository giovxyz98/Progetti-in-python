import openai
import string
import json
import os.path

path_execution = os.path.dirname(__file__)
api_key = "API KEY"


def input_nome_file():
    nome = input("Come vuoi chiamare il file:\n")
    for x in nome:
        if x in "_- ":
            continue
        if x in string.digits:
            print('Non è possibile inserire i numeri')
            input_nome_file()
        elif x not in string.ascii_letters:
            print('Devono essere presenti solo lettere')
            input_nome_file()
    return nome

def start():
    inizio=-1
    log_chatGPT="log_chatGPT"
    try: 
        inizio = int(input("\n\nVuoi salvare questa chat nel file di default o in un altro file a tuo piacimento:\n0 = Salva in file di default\n1 = Salva i file in un altro file\n"))
    except KeyboardInterrupt:
        print('\n\n--------------------------------------------------------Interrotto--------------------------------------------------------test5\n\n')
    except:
        print("\nDevi inserire i valori 0 o 1\n")
        start()
    if inizio == 0:
        log_chatGPT = "log_chatGPT"
    elif inizio==1:
        log_chatGPT=input_nome_file()
    else:
        print("Devi inserire i valori 0 o 1\n")
        start()

    return log_chatGPT

def creaFile(nome_file):
    dicooo= dict()
    file_path = f"{path_execution}\\Log chatGPT\\{nome_file}.json"
    file_exist = os.path.isfile(file_path)
    if(not file_exist):
        with open(file_path,"w") as fp:
            json.dump(dicooo,fp)
    return file_path

def leggi_da_file(file):
    dica = dict()
    with open(file,"r") as infile:
            content = infile.read()
            parsed = dict(json.loads(content))
            for i in parsed.keys():
                dica[i]=parsed[i]
    return dica

def scegli_file():
    scelta = -1
    try:  
        scelta = int(input())
    
    except KeyboardInterrupt:
        print('\n\n--------------------------------------------------------Interrotto--------------------------------------------------------test4\n\n')
    except:
        print("\nWarning: Devi inserire un numero\n")
    return scelta

def leggi_log():
    
    print("\nQuale file vuoi leggere (inserisci il numero):\n")
    
    files_path = dict()
    path=f"{path_execution}\\Log chatGPT"
    x = 0
    for i in os.listdir(path):
        files_path[x] = i
        x+=1
    for i in files_path.keys():
            print(f"{i} - {files_path[i]}")
    
    scelta= scegli_file()
    while  scelta >= len(files_path) or scelta < 0:
        print("\nWarning: Scegli tra i presenti\n")
        for i in files_path.keys():
            print(f"{i} - {files_path[i]}")
        scelta = scegli_file() 

    file_path = f"{path}\\{files_path[scelta]}"
    dica = leggi_da_file(file_path)
    return dica,file_path

def stampa(dica):
    for i in dica.keys():
        print(f"\n\nUser : \n{i} \n\nChatGPT: \n\n{dica[i]}\n\n----------------------------------Nuova domanda----------------------------------\n\n")

def scelta():
    cosa =-1
    try:  
            cosa = int(input("\nCiao sono chatGPT che cosa vuoi fare (Scegli tra le opzioni):\n\
0 - Leggere le vecchie conversazioni\n\
1 - Fare una nuova chat\n\
2 - Caricare chat e continuare la discussione\n"))

    except KeyboardInterrupt:
        
        print('\n\n------------------------------------------------------------------------------------Interrotto------------------------------------------------------------------------------------test2 \n\n')
    except:
        print("\nWarning: Devi inserire un numero\n")
        scelta()
    return cosa

def esegui_chatGPT(messages,dica,file):
    try:
        while True:
            
            message = input("\n\nUser : \n")
            if message:
                messages.append(
                    {"role": "user", "content": message},
                )
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=messages
                )
            reply = chat.choices[0].message.content
            print(f"\n\nChatGPT: {reply}\n\n----------------------------------Nuova domanda----------------------------------\n\n")
            messages.append({"role": "assistant", "content": reply})
            dica[message] = reply
            
            with open(file, "w") as outfile:
                json.dump(dica,outfile,indent=4)
    except KeyboardInterrupt:
        print('\n\n------------------------------------------------------------------------------------Interrotto------------------------------------------------------------------------------------ test1\n\n')

def carica_da_file(dica, messages):
    for domanda in dica.keys():
        messages.append(
                {"role": "user", "content": domanda},
                )
        messages.append({"role": "assistant", "content": dica[domanda]})
    return messages
        
        



scelto =-1

while scelto != 0 and scelto != 1 and scelto != 2:
    print("\nScegli tra le opzioni\n")
    scelto = scelta()
    
if scelto == 0:
    stampa(leggi_log()[0])
    input()
    input()
elif scelto == 1:
    log_chatGPT=start()
    file = creaFile(log_chatGPT)
    dica = leggi_da_file(file)
    openai.api_key = api_key
    messages = [ {"role": "system", "content": 
                "You are a intelligent assistant."} ]
    esegui_chatGPT(messages,dica,file)
elif scelto == 2:
    log = leggi_log()
    openai.api_key = api_key
    stampa(log[0])
    messages = [ {"role": "system", "content": 
                "You are a intelligent assistant."} ]
    chat = carica_da_file(log[0],messages)
    esegui_chatGPT(chat,log[0],log[1])
    
    
