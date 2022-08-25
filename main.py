import colorama, httpx, json, time, threading, ctypes
from colorama import Fore, Style, init
import os

def clear_screen():
    try:
        os.system('cls')
    except:
        os.system('clear')
    return
init()
threads = input("Enter the amount of threads to use: ")
dispay_errs = False
display_errors = input("Do you want to show errors (y/n): ")
if display_errors.lower() == "y" or display_errors.lower() == "yes":
    display_errs = True
else:
    pass
clear_screen()
class Logger:
    def Success(text):
        lock = threading.Lock()
        lock.acquire()
        print(f'[{Fore.GREEN}${Fore.WHITE}] {text}')
        lock.release()
    
    def Error(text):
        lock = threading.Lock()
        lock.acquire()
        print(f'[{Fore.RED}-{Fore.WHITE}] {text}')
        lock.release()

    
class DiscordFetch:
    def __init__(self):
        self.tokens = []; self.total_tokens = 0; self.tokens_index = 0; self.xbox_codes_claimed = 0; self.display_err = display_errs
        with open("tokens.txt", "r") as dataa:
            self.data = dataa.readlines()
            for self.token in self.data:
                self.token = self.token.replace("\n", "")
                self.tokens.append(self.token)
                self.total_tokens += 1
        
    def startdiscord(self):
        try:
            self.token = self.tokens[self.tokens_index]
            self.tokens_index += 1
        except IndexError:
            while True:
                if self.total_tokens == self.tokens_index:
                    Logger.Success("Claimed All Codes")
                    time.sleep(1)
                    exit(0)
                else:
                    pass
        self.Code = DiscordFetch.XboxLiveGamepass(self.token)
        if self.Code == "error":
            Logger.Error("Error Fetching Xbox Code")
            return DiscordFetch.startdiscord()
        file = open("codes.txt", "a+")
        file.write(f"{self.Code}\n")
        file.close()
        return DiscordFetch.startdiscord()
    def update_console_headers(self):
        while True:
            ctypes.windll.kernel32.SetConsoleTitleW(f"[FREE] Pr0t0n X ADylan | Tokens Loaded: {self.total_tokens} | Xbox Code Claimed: {self.xbox_codes_claimed}")
    def XboxLiveGamepass(self, token):
        self.url = 'https://discord.com/api/v9/outbound-promotions/890374599315980288/claim'
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": self.token,
            "cookie": "__dcfduid=6f575b70191f11ed97da1f757024d5d7; __sdcfduid=6f575b71191f11ed97da1f757024d5d71201146a0fe8b2af2c79af28e32aea073ecc34c95ace9556676f8372725bf8a8;",
            "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAzLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE0MTAyMSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
        }
        try:
            self.promotion_code = httpx.post(self.url, headers=self.headers)
        except Exception as err:
            if self.display_err == True:
                print(err)
            return "error"
        try:
            self.promotion_code = self.promotion_code.json()['code']
        except Exception as err:
            if self.display_err == True:
                print(err)
            return "error"
        Logger.Success(self.promotion_code)
        self.xbox_codes_claimed += 1
        return self.promotion_code



if __name__ == "__main__":
    DiscordFetch = DiscordFetch()
    for i in range(1):
        threading.Thread(target=DiscordFetch.update_console_headers).start()
    for i in range(int(threads)):
        threading.Thread(target=DiscordFetch.startdiscord).start()
