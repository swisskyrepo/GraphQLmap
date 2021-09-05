#!/usr/bin/env python3

try:
    import readline
except ImportError:
    import pyreadline as readline

from attacks import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GraphQLmap(object):
    author = "@pentest_swissky"
    version = "1.0"
    endpoint = "graphql"
    method = "POST"
    args = None
    url = None
    headers = None
    use_json = False

    def __init__(self, args_graphql):
        print("   _____                 _      ____  _                            ")
        print("  / ____|               | |    / __ \| |                           ")
        print(" | |  __ _ __ __ _ _ __ | |__ | |  | | |     _ __ ___   __ _ _ __  ")
        print(" | | |_ | '__/ _` | '_ \| '_ \| |  | | |    | '_ ` _ \ / _` | '_ \ ")
        print(" | |__| | | | (_| | |_) | | | | |__| | |____| | | | | | (_| | |_) |")
        print("  \_____|_|  \__,_| .__/|_| |_|\___\_\______|_| |_| |_|\__,_| .__/ ")
        print("                  | |                                       | |    ")
        print("                  |_|                                       |_|    ")
        print(" " * 30, end='')
        print(f"\033[1mAuthor\033[0m: {self.author} \033[1mVersion\033[0m: {self.version} ")
        self.args = args_graphql
        self.url = args_graphql.url
        self.method = args_graphql.method
        # add - def fixHeadersJSON()
        if self.args.headers != None:
            self.args.headers = fix_headers(self.args.headers)
        else:
            self.args.headers = None

        self.args.headers = json.loads(args_graphql.headers)
        self.use_json = True if args_graphql.use_json else False

        while True:
            query = input("GraphQLmap > ")
            cmdlist.append(query)
            if query == "exit" or query == "q":
                exit()

            elif query == "help":
                display_help()

            elif query == "debug":
                display_types(self.url, self.method, self.args.headers, self.use_json)

            elif query == "dump_new":
                dump_schema(self.url, self.method, 15, self.args.headers, self.use_json)

            elif query == "dump_old":
                dump_schema(self.url, self.method, 14, self.args.headers, self.use_json)

            elif query == "nosqli":
                blind_nosql(self.url, self.method, self.args.headers, self.use_json)

            elif query == "postgresqli":
                blind_postgresql(self.url, self.method, self.args.headers, self.use_json)

            elif query == "mysqli":
                blind_mysql(self.url, self.method, self.args.headers, self.use_json)

            elif query == "mssqli":
                blind_mssql(self.url, self.method, self.args.headers, self.use_json)

            else:
                exec_advanced(args_graphql.url, self.method, query, self.args.headers, self.use_json)


if __name__ == "__main__":
    readline.set_completer(auto_completer)
    readline.parse_and_bind("tab: complete")
    args = parse_args()
    GraphQLmap(args)
