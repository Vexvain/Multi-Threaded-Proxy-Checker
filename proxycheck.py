# Multi-Threaded Proxy Checker
# :) Vexvain :)

from contextlib import suppress
from multiprocessing.pool import ThreadPool
import threading
import requests


class ProxyChecker:
    """Class used to check a proxy list for validity"""
    def __init__(self, proxylist, savefile, threads=200, timeout=25):
        # Declares variables
        self.proxylist = proxylist
        self.savefile = savefile
        self.threads = threads
        self.timeout = timeout
		# Creates a file I/O lock
		self.flock = threading.Lock()

    def start_check(self):
        # Multi-Threaded processes
        p = ThreadPool(processes=self.threads)  # Creates a pool of workers
        p.map(self.check_proxy, self.proxylist)  # Calls check_proxy with the proxy as parameter
        p.close()  # Closes the multi-threaded processes

    def check_proxy(self, proxy):
        # Adds proxy to the proxies dict to be used with requests
        proxies = {'http': 'http://' + proxy, 'https': 'https://' + proxy}
        # Suppresses any exceptions, such as proxy timeout
        with suppress(Exception):
            # Makes request to google using the proxy
            requests.get('https://www.google.com', proxies=proxies, timeout=self.timeout)
            # If request does not timeout then proxy is printed and written to file
            print(proxy)
			with self.flock():
            	with open(self.savefile, 'a') as f:
                	f.write(proxy + '\n')


def main():
    # Gets filename from user
    filename = input('Please enter the name of the proxy list: ')

    # Tries to open file
    try:
        with open(filename, 'r') as f:
            proxies = f.read().split('\n')
    except IOError:
        print('Invalid file')
        main()

    # Initalizes ProxyChecker with the proxy list and the savefile name
    c = ProxyChecker(proxylist=proxies, savefile='available.txt')
    # Starts the check
    c.start_check()

if __name__ == '__main__':
    main()
