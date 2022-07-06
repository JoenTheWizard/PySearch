try:
    from googlesearch import search
except ImportError as e:
    print(e,"\nTry install module by 'pip install google' and try again (package also requires 'pip install beautifulsoup4'")

programRun = True
PAUSE_VAL = 5
TLD = "com"
def ansi(n):
    return f'\033[{n}m'

def options(opt):
    global TLD
    global PAUSE_VAL
    if opt == '1':
        print(f"Change TLD value (TLD = {TLD}):")
        TLD = input('> ')
        print(f"Changed TLD value to {TLD}")
    elif opt == '2':
        print(f"Change request delay value (Pause = {PAUSE_VAL}):")
        PAUSE_VAL = int(input('> '))
        print(f"Changed Pause value to {PAUSE_VAL}")

def search_txt(q):
    j=1
    print("Searching please wait...")
    for query in search(q,tld=TLD,num=10,stop=10,pause=PAUSE_VAL):
        print(f'{j} -- {query}')
        j+=1
def search_file(file):
    f = open(file,"r")
    print('Searching in progres...')
    j=1
    for m in f.read().split('\n'):
        if m.strip() != '':
            print(f"Searching: {j} -- {m}")
            j+=1
            print('-'*30)
            for sr in search(m, tld=TLD,num=10,stop=10,pause=PAUSE_VAL):
                print(sr)
            print('-'*30)

def programMain():
    global programRun
    while programRun:
        print(ansi(36),"""
██████╗░██╗░░░██╗  ░██████╗███████╗░█████╗░██████╗░░█████╗░██╗░░██╗
██╔══██╗╚██╗░██╔╝  ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██║░░██║
██████╔╝░╚████╔╝░  ╚█████╗░█████╗░░███████║██████╔╝██║░░╚═╝███████║
██╔═══╝░░░╚██╔╝░░  ░╚═══██╗██╔══╝░░██╔══██║██╔══██╗██║░░██╗██╔══██║
██║░░░░░░░░██║░░░  ██████╔╝███████╗██║░░██║██║░░██║╚█████╔╝██║░░██║
╚═╝░░░░░░░░╚═╝░░░  ╚═════╝░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
Created by JoenTheWizard

1 - Search by query
2 - Search by file
3 - Options
'Quit'/'Close' - quits program
        """,ansi(0))
        inp = input('Select one of the following options: ')
        if inp == '1':
            print("Selection '1' - Enter your search query below:")
            q = input()
            search_txt(q)
        elif inp == '2':
            print("Selection '2' - Enter your file path below (each query must be seperated by a new line):")
            search_file(input())
        elif inp == '3':
            print(f"""
1 - TLD (Top-level domain) = {TLD}
2 - Pause = {PAUSE_VAL}
3 (or any other key) - Go back
            """)
            options(input('> '))
        elif inp.lower()=='quit' or inp.lower()=='close' or inp.lower() == 'q':
            programRun = False

if __name__ == "__main__":
    programMain()
