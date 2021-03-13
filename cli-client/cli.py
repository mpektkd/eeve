import argparse
import textwrap
import json
import requests
import os

def msg(name=None):                                                            
    return "General Usage:ev_group13 SCOPE --param1 value1 [--param2 value2 ...]--format fff --apikey kkk\n"

parent_parser = argparse.ArgumentParser(add_help =False)
requirednames =parent_parser.add_argument_group('always required arguments:')

requirednames.add_argument(
        '--format',
        dest='format',
        action='store',
        required=True,
        help='format',
        choices = ['csv','json']
    )
requirednames.add_argument(
        '--apikey',
        dest='x',
        action='store',
        required=True,
        help='API Key',
        type= str
    )
parser = argparse.ArgumentParser(usage=msg())

# SCOPE        
subparser = parser.add_subparsers(dest='command',help='SCOPE')
healthcheck = subparser.add_parser('healthcheck', parents = [parent_parser],usage="ev_group13 healthcheck --format fff --apikey kkk\n")
resetsessions = subparser.add_parser('resetsessions',parents = [parent_parser],usage = "ev_group13 resetsessions --format fff --apikey kkk\n")
login = subparser.add_parser('login',parents = [parent_parser],usage = "ev_group13 login --username USERNAME --passw PASSWORD --format fff --apikey kkk\n")
logout = subparser.add_parser('logout',parents = [parent_parser],usage = "ev_group13 logout --format fff --apikey kkk\n")
SessionsPerPoint = subparser.add_parser('SessionsPerPoint',parents = [parent_parser],usage = "ev_group13 SessionsPerPoint --point POINT --datefrom YYMMDD --dateto YYMMDD --format fff --apikey kkk\n")
SessionsPerStation = subparser.add_parser('SessionsPerStation',parents = [parent_parser],usage = "ev_group13 SessionsPerStation --station STATION --datefrom YYMMDD --dateto YYMMDD --format fff --apikey kkk\n")
SessionsPerEV = subparser.add_parser('SessionsPerEV',parents = [parent_parser],usage = "ev_group13 SessionsPerEV --ev EV --datefrom YYMMDD --dateto YYMMDD --format fff --apikey kkk\n")
SessionsPerProvider = subparser.add_parser('SessionsPerProvider',parents = [parent_parser],usage = "ev_group13 SessionsPerProvider --provider PROVIDER --datefrom DATEFROM --dateto DATETO --format fff --format fff --apikey kkk\n")
Admin = subparser.add_parser('Admin',parents = [parent_parser],usage="ev_group13 Admin --MainParameter --Subparameters --format fff --apikey kkk\n")


#Admin_subparsers = Admin.add_parser(dest='command',help='Main Parameter')

login_required = login.add_argument_group('login required arguments')
login_required.add_argument('--username', type=str, required=True)
login_required.add_argument('--passw', type=str, required=True)

SessionsPerPoint_required = SessionsPerPoint.add_argument_group('SessionsPerpoint required arguments')
SessionsPerPoint_required.add_argument('--point', type=str, required=True)
SessionsPerPoint_required.add_argument('--datefrom', type=str, required=True)
SessionsPerPoint_required.add_argument('--dateto', type=str, required=True)

SessionsPerStation.add_argument('--station',type=str,required=True)
SessionsPerStation.add_argument('--datefrom', type=str, required=True)
SessionsPerStation.add_argument('--dateto', type=str, required=True)

SessionsPerEV.add_argument('--ev', type=str, required=True)
SessionsPerEV.add_argument('--datefrom', type=str, required=True)
SessionsPerEV.add_argument('--dateto', type=str, required=True)

SessionsPerProvider.add_argument('--provider', type=str, required=True)
SessionsPerProvider.add_argument('--datefrom', type=str, required=True)
SessionsPerProvider.add_argument('--dateto', type=str, required=True)

Admin.add_argument('--usermod', action='store_true')
Admin.add_argument('--username', type =str )
Admin.add_argument('--passw',type =str)
Admin.add_argument('--users',type = str)
Admin.add_argument('--sessionsupd', action = 'store_true')
Admin.add_argument('--source', type = str)
Admin.add_argument('--healthcheck', action='store_true')
Admin.add_argument('--resetsessions', action ='store_true')



args = parser.parse_args()



if args.command == 'healthcheck':
    r = requests.get("http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/admin/healthcheck/").json()
    print(r["status"])
elif args.command == 'resetsessions':
    print('resetsessionsapi')
    if args.format == 'csv': print('csv')
    else: print('json')
elif args.command == 'login':
    params = {
    "username": args.username,
    "password": args.passw
    }
    if os.path.exists("softeng20bAPI.token"):
        print("You are already logged in!")
    else:
        f = open("softeng20bAPI.token","w")
        json_object = requests.post("http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/login/",json=params).json()
        f.write(json.dumps(json_object))
        
    
elif args.command == 'logout':
    f = open("softeng20bAPI.token")
    token_value = json.load(f) 
    header = {"Authorization" : "JWT " + token_value["access"] }
    r = requests.post("http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/logout/",headers=header,json=token_value)
    if r.ok:
        print("Bye")
        os.remove("softeng20bAPI.token")
    else:
        print(str(r.status_code)+" " + r.reason)     

elif args.command == 'SessionsPerPoint':
    url = 'http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/SessionsPerPoint/' + args.point + '/' + args.datefrom + '_from/' + args.dateto + '_to/?format=' + args.format
    f = open("softeng20bAPI.token")
    token_value = json.load(f) 
    header = {"Authorization" : "JWT " + token_value["access"] }
    r = requests.get(url,headers=header)
    if r.ok:
        print(r.text)
    else:
        print(str(r.status_code) + ' ' + r.reason)

elif args.command == 'SessionsPerStation':
    url = 'http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/SessionsPerStation/' + args.station + '/' + args.datefrom + '_from/' + args.dateto + '_to/?format=' + args.format
    f = open("softeng20bAPI.token")
    token_value = json.load(f) 
    header = {"Authorization" : "JWT " + token_value["access"] }
    r = requests.get(url,headers=header)
    if r.ok:
        print(r.text)
    else:
        print(str(r.status_code) + ' ' + r.reason)



elif args.command == 'SessionsPerEV':
    url = 'http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/SessionsPerEV/' + args.ev + '/' + args.datefrom + '_from/' + args.dateto + '_to/?format=' + args.format
    f = open("softeng20bAPI.token")
    token_value = json.load(f) 
    header = {"Authorization" : "JWT " + token_value["access"] }
    r = requests.get(url,headers=header)
    if r.ok:
        print(r.text)
    else:
        print(str(r.status_code) + ' ' + r.reason)

elif args.command == 'SessionsPerProvider':
    print("/sessionsperProvider")
    if args.format == 'csv': print('csv')
    else: print('json')
elif args.command == 'Admin':
    usermod = args.usermod and args.username and args.passw  and (not(args.users or args.sessionsupd or args.source or args.healthcheck or args.resetsessions))
    users = args.users and args.username and (not(args.usermod or args.passw or args.sessionsupd or args.source or args.healthcheck or args.resetsessions))
    sessionupd = args.sessionsupd and args.source and (not(args.usermod or args.username or args.passw or args.users or args.healthcheck or args.resetsessions))
    healthcheck = args.healthcheck and (not(args.usermod or args.username or args.passw or args.users or args.sessionsupd or args.source or args.resetsessions))
    resetsessions = args.resetsessions and (not(args.usermod or args.username or args.passw or args.users or args.sessionsupd or args.source or args.healthcheck))
    
    if usermod: 
        print ("/usermod")
        if args.format == 'csv': print('csv')
        else: print('json')
    elif users:
        print ("/users")
        if args.format == 'csv': print('csv')
        else: print('json')
    elif sessionupd: 
        print ("/sessionsupd")
        if args.format == 'csv': print('csv')
        else: print('json')
    elif healthcheck: 
        r = requests.get("http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/admin/healthcheck/").json()
        print(r["status"])
        else: print('json')
    elif resetsessions: 
        print ("resetsessions")
        if args.format == 'csv': print('csv')
        else: print('json')
    else: print('Not correct usage')
    


