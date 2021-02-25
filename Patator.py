import requests, random, os, json
from colorama import Fore, Style, init
from threading import Thread
init()

class Console():
    def __init__(self, title = 'github.com/its-vichy'):
        self.console_title = title

    def print_logo(self):
        os.system(f'title [Vichy] Patator V2 ~ {self.console_title}')
        os.system('cls' if os.name == 'nt' else 'clear')
        print('''       
         ____       _        _              __     ______  
        |  _ \ __ _| |_ __ _| |_ ___  _ __  \ \   / /___ \ 
        | |_) / _` | __/ _` | __/ _ \| '__|  \ \ / /  __) |
        |  __/ (_| | || (_| | || (_) | |      \ V /  / __/ 
        |_|   \__,_|\__\__,_|\__\___/|_|       \_/  |_____| github.com/its-vichy
                                                        
        [1] Webhook Spammer.
        [2] Token Joiner. (soon)
        '''.replace('its-vichy', f'{Fore.RED}its-vichy{Fore.WHITE}').replace('1', f'{Fore.CYAN}1{Fore.WHITE}').replace('2', f'{Fore.CYAN}2{Fore.WHITE}'))

    def printer(self, badge, text, finish = '.', color = Fore.CYAN, Isinput = False):
        if Isinput == True:
            return input(f'{Fore.WHITE}[{color}{badge}{Fore.WHITE}] {text}{Fore.WHITE} ~~> ')
        else:
            print(f'{Fore.WHITE}[{color}{badge}{Fore.WHITE}] {text}{Fore.WHITE}{finish}')

class Proxy():
    def __init__(self, proxy_file = './Config/Proxies.txt'):
        self.proxy_file = proxy_file
        self.proxy_list = []
        self.console = Console()

    def get_proxy_number(self):
        return len(self.proxy_list)

    def load_proxy(self):
        with open(self.proxy_file, 'r+') as proxy_files:
            for proxy in proxy_files:
                proxy = proxy.split('\n')[0]
                if proxy not in self.proxy_list:
                    self.proxy_list.append(proxy)
        
        self.console.printer('*', f'{self.get_proxy_number()} proxies was load from {self.proxy_file} file', color= Fore.MAGENTA)

    def scrape_proxy(self):
        before_number = self.get_proxy_number()
        i = 0
        http = 0
        http_s = 0
        socks4 = 0
        socks5 = 0
        unknow = 0
        with open('./Config/Config.json') as config_file:
            config = json.load(config_file)

            for Owner, Url in config['ProxyScrapeUrls'].items():
                Proxies = requests.get(Url).text.split('\n')
                i += 1
                
                for Proxy in Proxies:
                    Proxy = Proxy.strip()
                    if Owner.split('-')[1] == 'All':
                        if Proxy not in self.proxy_list:
                            self.proxy_list.append(Proxy)
                            unknow += 1
                    if Owner.split('-')[1] == 'Http':
                        if Proxy not in self.proxy_list:
                            self.proxy_list.append(Proxy)
                            http += 1
                    if Owner.split('-')[1] == 'Https':
                        if Proxy not in self.proxy_list:
                            self.proxy_list.append(Proxy)
                            http_s += 1
                    if Owner.split('-')[1] == 'Socks4':
                        if Proxy not in self.proxy_list:
                            self.proxy_list.append(f'socks4://{Proxy}')
                            socks4 += 1
                    if Owner.split('-')[1] == 'Socks5':
                        if Proxy not in self.proxy_list:
                            self.proxy_list.append(f'socks5://{Proxy}')
                            socks5 += 1

        self.console.printer('*', f'{self.get_proxy_number() - before_number} proxies was scraped from {i} url(s) ({unknow} Unknow | {http} http | {http_s} https | {socks4} socks4 | {socks5} socks5)', color= Fore.MAGENTA)
            
    def get_random_proxy(self):
        proxy = random.choice(self.proxy_list)
        return proxy, dict({'http' : proxy, 'https' : proxy})

    def remove_proxy(self, proxy):
        self.proxy_list.remove(proxy)

class Spammer():
    def __init__(self, console, webhook_threads, spammer_threads, proxy_manager, token_file = './Config/Tokens.txt', webhook_file = './Config/Hook.txt'):
        self.token_file = token_file
        self.hook_file = webhook_file
        self.proxy_manager = proxy_manager
        self.console = console
        self.hook_list = []

    def load_hook(self):
        i = 0
        with open(self.hook_file, 'r+') as hook_files:
            for hook in hook_files:
                hook = hook.split('\n')[0]
                if hook not in self.hook_list:
                    self.hook_list.append(hook)
                    i += 1
        self.console.printer('*', f'{i} hook(s) was load from {self.hook_file} file', color= Fore.MAGENTA)

    def Spam_Webhook(self):
        while True:
            try:
                hook = random.choice(self.hook_list)
                raw, proxy = self.proxy_manager.get_random_proxy()
                
                Resp = requests.post(hook, headers= {'content-type': 'application/json'}, data= json.dumps({'content': '@everyone LMAO'}), proxies=dict(proxy), timeout= 3500).status_code

                if Resp == 204:
                    self.console.printer('+', f'Hook sent with {raw}', ' !', Fore.GREEN)
                    #print(f'Hook sent with {raw}')
                elif Resp == 429:
                    self.console.printer('~', f'Rate limited with {raw}', ' :(', Fore.YELLOW)
                    #print(f'Rate limited with {raw}')
                else:
                    self.console.printer('!', f'CloudFare banned with proxy {raw}', ' !', Fore.RED)
                    #print(f'CloudFare banned with proxy {raw}')

            except requests.exceptions.ProxyError as err:
                pass
            except requests.exceptions.ConnectionError as err:
                pass
            except requests.exceptions.InvalidURL as err:
                pass

    def start_spammer(self, threads_number, choice):
        ThreadList = []
        
        if choice == 1:
            TargetCmd = self.Spam_Webhook

        for i in range(threads_number):
            T = Thread(target=TargetCmd)
            ThreadList.append(T)

        for Threads in ThreadList:
            Threads.start()

class Main():
    def __init__(self, user_token, webhook_threads, spammer_threads):
        self.webhook_threads = webhook_threads
        self.spammer_threads = spammer_threads
        self.user_token      = user_token
        self.console         = Console()
        self.proxy_manager   = Proxy()
        self.spammer         = Spammer(self.console, self.webhook_threads, self.spammer_threads, self.proxy_manager)

    def initialize(self):
        self.console.print_logo()
        self.proxy_manager.load_proxy()
        self.proxy_manager.scrape_proxy()

    def Parser(self):
        while True:
            Resp = int(self.console.printer('?', 'Choose an option', color= Fore.YELLOW, Isinput= True))

            if Resp == 1:
                self.console.printer('*', f'Starting webhook spammer with {self.webhook_threads} thread(s)', color= Fore.MAGENTA)
                self.spammer.load_hook()
                self.spammer.start_spammer(self.webhook_threads, Resp)

with open('./Config/Config.json', 'r+') as config_file:
    config = json.load(config_file)

    Tool = Main(config['Token'], config['WebhoockThreads'], config['SpammerThreads'])
    Tool.initialize()
    Tool.Parser()