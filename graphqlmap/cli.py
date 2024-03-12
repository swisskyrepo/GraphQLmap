try:
    import readline
except ImportError:
    import pyreadline3 as readline

from graphqlmap.attacks import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GraphQLmap(object):
    author = "@pentest_swissky"
    version = "1.1"
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
        self.headers = None if not args_graphql.headers else json.loads(args_graphql.headers)
        self.use_json = True if args_graphql.use_json else False
        # self.proxy =  {
        #     "http"  : args_graphql.proxy, 
        # }
        self.proxy = args_graphql.proxy

        while True:
            query = input("GraphQLmap > ")
            cmdlist.append(query)
            if query == "exit" or query == "q":
                exit()

            elif query == "help":
                display_help()

            elif query == "debug":
                display_types(self.url, self.method, self.proxy, self.headers, self.use_json)

            elif query == "dump_via_introspection":
                dump_schema(self.url, self.method, 15, self.proxy, self.headers, self.use_json)

            elif query == "dump_via_fragment":
                dump_schema(self.url, self.method, 14, self.proxy, self.headers, self.use_json)

            elif query == "nosqli":
                blind_nosql(self.url, self.method, self.proxy, self.headers, self.use_json)

            elif query == "postgresqli":
                blind_postgresql(self.url, self.method, self.proxy, self.headers, self.use_json)

            elif query == "mysqli":
                blind_mysql(self.url, self.method, self.proxy, self.headers, self.use_json)

            elif query == "mssqli":
                blind_mssql(self.url, self.method, self.proxy, self.headers, self.use_json)

            else:
                print(self.headers)
                exec_advanced(self.url, self.method, query, self.headers, self.use_json, self.proxy)

def main():
    readline.set_completer(auto_completer)
    readline.parse_and_bind("tab: complete")
    args = parse_args()
    GraphQLmap(args)

if __name__ == "__main__":
    main()