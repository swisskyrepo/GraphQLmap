#!/usr/bin/python
import argparse
import json

import requests

cmdlist = ["exit", "help", "dump_via_fragment", "dump_via_introspection", "postgresqli", "mysqli", "mssqli", "nosqli", "mutation", "edges",
           "node", "$regex", "$ne", "__schema"]


def auto_completer(text, state):
    options = [x for x in cmdlist if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None


def jq(data):
    return json.dumps(data, indent=4, sort_keys=True)


def requester(url, method, payload, proxy, headers=None, use_json=False, is_batch=0):
    if method == "POST" or use_json:
        new_headers = {} if headers is None else headers.copy()
        
        data = None
        if is_batch == 0:
            data = {
                "query": payload.replace("+", " ")
            }
            new_data = data.copy()

            if use_json:
                new_headers['Content-Type'] = 'application/json'
                new_data = json.dumps(data)
            r = requests.post(url, data=new_data, verify=False, headers=new_headers, proxies=proxy)

        else:
            data = []
            for i in range(is_batch):
                data.append( {"query": payload} )
                
            r = requests.post(url, json=data, verify=False, headers=new_headers, proxies=proxy)


        if r.status_code == 500:
            print("\033[91m/!\ API didn't respond correctly to a POST method !\033[0m")
            return None
    else:
        r = requests.get(url + "?query={}".format(payload), verify=False, headers=headers, proxies=proxy)
    return r


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action='store', dest='url', help="URL to query : example.com/graphql?query={}")
    parser.add_argument('-v', action='store', dest='verbosity', help="Enable verbosity", nargs='?', const=True)
    parser.add_argument('--method', action='store', dest='method',
                        help="HTTP Method to use interact with /graphql endpoint", nargs='?', const=True, default="GET")
    parser.add_argument('--headers', action='store', dest='headers', help="HTTP Headers sent to /graphql endpoint",
                        nargs='?', const=True, type=str)
    parser.add_argument('--json', action='store', dest='use_json', help="Use JSON encoding, implies POST", nargs='?', const=True, type=bool)
    parser.add_argument('--proxy', action='store', dest='proxy',
                        help="HTTP proxy to log requests", nargs='?', const=True, default=None)

    results = parser.parse_args()
    if results.url is None:
        parser.print_help()
        exit()
    return results


def display_help():
    print("[+] \033[92mdump_via_introspection \033[0m: dump GraphQL schema (fragment+FullType)")
    print("[+] \033[92mdump_via_fragment      \033[0m: dump GraphQL schema (IntrospectionQuery)")
    print("[+] \033[92mnosqli      \033[0m: exploit a nosql injection inside a GraphQL query")
    print("[+] \033[92mpostgresqli \033[0m: exploit a sql injection inside a GraphQL query")
    print("[+] \033[92mmysqli      \033[0m: exploit a sql injection inside a GraphQL query")
    print("[+] \033[92mmssqli      \033[0m: exploit a sql injection inside a GraphQL query")
    print("[+] \033[92mexit        \033[0m: gracefully exit the application")
