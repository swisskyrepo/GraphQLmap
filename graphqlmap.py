#!/usr/bin/python
import argparse
import json
import re
import readline
import requests
import sys
import time
from utils import *
from attacks import *

class GraphQLmap(object):
    author   = "@pentest_swissky"
    version  = "1.0"
    endpoint = "graphql"
    method   = "POST"
    args = None
    url  = None

    def __init__(self, args):
        print("   _____                 _      ____  _                            ")
        print("  / ____|               | |    / __ \| |                           ")
        print(" | |  __ _ __ __ _ _ __ | |__ | |  | | |     _ __ ___   __ _ _ __  ")
        print(" | | |_ | '__/ _` | '_ \| '_ \| |  | | |    | '_ ` _ \ / _` | '_ \ ")
        print(" | |__| | | | (_| | |_) | | | | |__| | |____| | | | | | (_| | |_) |")
        print("  \_____|_|  \__,_| .__/|_| |_|\___\_\______|_| |_| |_|\__,_| .__/ ")
        print("                  | |                                       | |    ")
        print("                  |_|                                       |_|    ")
        print(" "*30 + f"\033[1mAuthor\033[0m: {self.author} \033[1mVersion\033[0m: {self.version} ")
        self.args = args
        self.url = args.url
        self.method = args.method

        while True:
            query = input("GraphQLmap > ")
            cmdlist.append(query)
            if query == "exit" or query == "q": 
                exit()

            elif query == "help":
                display_help()
            
            elif query == "debug":
                display_types(self.url, self.method)

            elif query == "dump_new":
                dump_schema(self.url, self.method, 15)

            elif query == "dump_old":
                dump_schema(self.url, self.method, 14)

            elif query == "nosqli":
                blind_nosql(self.url, self.method)

            elif query == "postgresqli":
                blind_postgresql(self.url, self.method)

            elif query == "mysqli":
                blind_mysql(self.url, self.method)
                
            elif query == "mssqli":
                blind_mssql(self.url, self.method)

            else:
                exec_advanced(args.url, self.method, query)

if __name__ == "__main__":
    readline.set_completer(auto_completer)
    readline.parse_and_bind("tab: complete")
    args = parse_args()
    GraphQLmap(args)