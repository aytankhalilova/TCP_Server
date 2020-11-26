import re
import socket
import argparse
import sys
import requests 
import threading
from bs4 import BeautifulSoup
from colorama import Fore, Style

class Server:
    HOST = "127.0.0.1"
    PORT = 1060
    MAX_BYTES = 2048

    def __init__(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def transaction(self,sc,sockname):
        url = (sc.recv(self.MAX_BYTES)).decode()
        section = requests.get(url)
        
        print(f"[+] Scraping {url}")
        b_soup = BeautifulSoup(section.content,"html.parser")

        image_n = self.image_num(b_soup)
        paragraph_n = self.paragraph_num(b_soup)

        result = f"{image_n} {paragraph_n}"
        sc.send(result.encode())

        print(Fore.CYAN,Style.BRIGHT,"\n[+] The transaction ended successfully.")

    def image_num(self,b_soup):
        n = len(b_soup.find_all("img"))
        return n

    def paragraph_num(self, b_soup):
        c = 0
        parag_soup = b_soup.find_all('p')
        for i in parag_soup:
            if not i.find_all("p"):
                c += 1
        return c


    def start_process(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(1)

        print(Fore.RED,Style.BRIGHT,"[+] The server is listening at:", self.sock.getsockname())

        while True:
            sc, sockname = self.sock.accept()
            print(Fore.BLUE, Style.BRIGHT,'\n[+] Connection established from', sockname)

            thread = threading.Thread(target=self.transaction, args=(sc,sockname))
            thread.start_process()


class Client:
    HOST = "127.0.0.1"
    PORT = 1060
    MAX_BYTES = 2048

    def __init__(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def url_check(self,url):
        a = re.search("http[s]",url)
        if not a:
            url = "https://" + url
        
        return url

    def start_process(self,url):
        self.sock.connect((self.HOST,self.PORT))
        url = self.url_check(url)
        encoded_url = url.encode()
        self.sock.send(encoded_url)

        image_n, parag_n = (self.sock.recv(self.MAX_BYTES)).decode().split()
        print(Fore.YELLOW, Style.BRIGHT,f"Paragraphs: {Fore.MAGENTA}{parag_n}{Fore.YELLOW};{Style.BRIGHT} Images: {Fore.MAGENTA}{image_n}")

        self.sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("WEB SCRAPER")
    option1_2 = {"server": Server, "client": Client}
    parser.add_argument('role', choices = option1_2, help = "server or client")
    parser.add_argument("-p",metavar="PAGE", type=str, help="Web URL")
    args = parser.parse_args()

    class1 = option1_2[args.role]
    
    if args.role == "client":
        client_object = class1()
        client_object.start_process(args.p)
    
    elif args.role == "server":
         server_object = class1()
         server_object.start_process()

