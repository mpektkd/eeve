import argparse
import sys
import json
import requests
import os
import pprint

from requests import status_codes



def msg(name=None):                                                            
    return "\nGeneral Usage:ev_group13 SCOPE [--params values] --format fff --apikey kkk\nScopes Supported: healthcheck|resetsessions|login|logout|SessionsPerPoint|SessionsPerStation|SessionsPerEV|SessionsPerProvider|Admin\n.\n.\n"


parent_parser = argparse.ArgumentParser(add_help =False)

#format and apikey are always required
requirednames =parent_parser.add_argument_group('always required arguments')

requirednames.add_argument(
        '--format',
        dest='format',
        action='store',
        required=True,
        help='format',
        choices = ['csv','json'] #format argument takes only csv or json as value
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
subparser = parser.add_subparsers(dest='command',help='SCOPE') #Implementation of SCOPE aspect with the use of subparser
#healthcheck scope
healthcheck = subparser.add_parser('healthcheck', parents = [parent_parser],usage="ev_group13 healthcheck --format fff --apikey kkk\n")
#resetsessions scope
resetsessions = subparser.add_parser('resetsessions',parents = [parent_parser],usage = "ev_group13 resetsessions --format fff --apikey kkk\n")
#login scope
login = subparser.add_parser('login',parents = [parent_parser],usage = "ev_group13 login --username USERNAME --passw PASSWORD --format fff --apikey kkk\n")
#logout scope
logout = subparser.add_parser('logout',parents = [parent_parser],usage = "ev_group13 logout --format fff --apikey kkk\n")
#SessionsPerPoint scope
SessionsPerPoint = subparser.add_parser('SessionsPerPoint',parents = [parent_parser],usage = "ev_group13 SessionsPerPoint --point POINT --datefrom YYMMDD --dateto YYMMDD --format fff --apikey kkk\n")
#SessionsPerStation scope
SessionsPerStation = subparser.add_parser('SessionsPerStation',parents = [parent_parser],usage = "ev_group13 SessionsPerStation --station STATION --datefrom YYMMDD --dateto YYMMDD --format fff --apikey kkk\n")
#SessionsPerEV scope
SessionsPerEV = subparser.add_parser('SessionsPerEV',parents = [parent_parser],usage = "ev_group13 SessionsPerEV --ev EV --datefrom YYMMDD --dateto YYMMDD --format fff --apikey kkk\n")
#SessionsPerProvider scope
SessionsPerProvider = subparser.add_parser('SessionsPerProvider',parents = [parent_parser],usage = "ev_group13 SessionsPerProvider --provider PROVIDER --datefrom DATEFROM --dateto DATETO --format fff --format fff --apikey kkk\n")
#Admin Scope
Admin = subparser.add_parser('Admin',parents = [parent_parser],usage="ev_group13 Admin --MainParameter --Subparameters --format fff --apikey kkk\n\nMain Parameters Supported : --usermod | --users | --healthcheck | --resetsessions | --sessionsupd\n\n")

#arguments needed in login scope
login_required = login.add_argument_group('login required arguments')
login_required.add_argument('--username', type=str, required=True)
login_required.add_argument('--passw', type=str, required=True)

#arguments needed in SessionsPerPoint scope
SessionsPerPoint_required = SessionsPerPoint.add_argument_group('SessionsPerpoint required arguments')
SessionsPerPoint_required.add_argument('--point', type=str, required=True)
SessionsPerPoint_required.add_argument('--datefrom', type=str, required=True)
SessionsPerPoint_required.add_argument('--dateto', type=str, required=True)

#arguments needed in SessionsPerStation scope
SessionsPerStation_required = SessionsPerStation.add_argument_group('SessionsPerStation required arguments')
SessionsPerStation_required.add_argument('--station',type=str,required=True)
SessionsPerStation_required.add_argument('--datefrom', type=str, required=True)
SessionsPerStation_required.add_argument('--dateto', type=str, required=True)

#arguments needed in SessionsPerEV scope
SessionsPerEV_required = SessionsPerEV.add_argument_group('SessionsPerEV required arguments')
SessionsPerEV_required.add_argument('--ev', type=str, required=True)
SessionsPerEV_required.add_argument('--datefrom', type=str, required=True)
SessionsPerEV_required.add_argument('--dateto', type=str, required=True)

#arguments needed in SessionsPerEV scope
SessionsPerProvider_required = SessionsPerProvider.add_argument_group('SessionsPerProvider required arguments')
SessionsPerProvider_required.add_argument('--provider', type=str, required=True)
SessionsPerProvider_required.add_argument('--datefrom', type=str, required=True)
SessionsPerProvider_required.add_argument('--dateto', type=str, required=True)

#arguments needed in Admin scope
Admin.add_argument('--usermod', action='store_true') #Main parameter
Admin.add_argument('--username', type =str ) #Secondary parameter
Admin.add_argument('--passw',type =str) #Secondary parameter
Admin.add_argument('--users', action ='store_true')#Main parameter
Admin.add_argument('--sessionsupd', action = 'store_true') #Secondary parameter
Admin.add_argument('--source', type = str) #Secondary parameter
Admin.add_argument('--healthcheck', action='store_true') # Main parameter
Admin.add_argument('--resetsessions', action ='store_true') # Main parameter

#Parse arguments given
args = parser.parse_args()



if args.command == 'healthcheck':  #healthcheck API 
    r = requests.get("http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/admin/healthcheck/").json()
    print(json.dumps(r, indent=2))
elif args.command == 'resetsessions': #resetsessions API Call
    print('resetsessionsapi')
    if args.format == 'csv': print('csv')
    else: print('json')
elif args.command == 'login': #login API Call
    params = {
    "username": args.username,
    "password": args.passw
    }
    if os.path.exists("softeng20bAPI.token"):
        print("You are already logged in!")
    else:
        
        json_object = requests.post("http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/login/",json=params).json()
        if 'detail' in json_object:
            print (json_object["detail"])
        else:
            f = open("softeng20bAPI.token","w")
            f.write(json.dumps(json_object,indent = 2))
            print ("Login Succsessfull...\nWelcome to eevie, " + args.username + '!')
        
    
elif args.command == 'logout': #logout 
    if not os.path.exists("softeng20bAPI.token"):
        print("You are not logged in.")
        sys.exit()
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
    if not os.path.exists("softeng20bAPI.token"):
            print("Not Logged in.")
            sys.exit()
    url = 'http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/SessionsPerPoint/' + args.point + '/' + args.datefrom + '_from/' + args.dateto + '_to/?format=' + args.format
    f = open("softeng20bAPI.token")
    token_value = json.load(f) 
    header = {"Authorization" : "JWT " + token_value["access"] }
    r = requests.get(url,headers=header)
    if r.ok:
        if args.format == 'json':
            print(json.dumps(r.json(),indent = 1))
        elif args.format == 'csv':
            print (r.text)
    else:
        print(str(r.status_code) + ' ' + r.reason)

elif args.command == 'SessionsPerStation':
    if not os.path.exists("softeng20bAPI.token"):
            print("Not Logged in.")
            sys.exit()
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
    if not os.path.exists("softeng20bAPI.token"):
            print("Not Logged in.")
            sys.exit()
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
    if not os.path.exists("softeng20bAPI.token"):
            print("Not Logged in.")
            sys.exit()
    url = 'http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/SessionsPerProvider/' + args.provider + '/' + args.datefrom + '_from/' + args.dateto + '_to/?format=' + args.format
    f = open("softeng20bAPI.token")
    token_value = json.load(f) 
    header = {"Authorization" : "JWT " + token_value["access"] }
    r = requests.get(url,headers=header)
    if r.ok:
        print(r.text)
    else:
        print(str(r.status_code) + ' ' + r.reason)
elif args.command == 'Admin':
    if not os.path.exists("softeng20bAPI.token"):
            print("Not Logged in.")
            sys.exit()

    usermod = args.usermod and args.username and args.passw  and (not(args.users or args.sessionsupd or args.source or args.healthcheck or args.resetsessions))
    users = args.users and args.username and (not(args.usermod or args.passw or args.sessionsupd or args.source or args.healthcheck or args.resetsessions))
    sessionupd = args.sessionsupd and args.source and (not(args.usermod or args.username or args.passw or args.users or args.healthcheck or args.resetsessions))
    healthcheck = args.healthcheck and (not(args.usermod or args.username or args.passw or args.users or args.sessionsupd or args.source or args.resetsessions))
    resetsessions = args.resetsessions and (not(args.usermod or args.username or args.passw or args.users or args.sessionsupd or args.source or args.healthcheck))
    if  usermod: 
        f = open("softeng20bAPI.token")
        token_value = json.load(f)
        header = {"Authorization" : "JWT " + token_value["access"] }
        url = 'http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/admin/usermod/' + args.username + '/' + args.passw + '/'
        r = requests.post(url,headers=header)
        if r.ok:
            print(json.dumps(r.json(),indent=2))
        else :
            print(str(r.status_code) + " " + r.reason)
            print("A problem occured with your request.\nYou are probably not an admin.")
    elif users:
        f = open("softeng20bAPI.token")
        token_value = json.load(f)
        header = {"Authorization" : "JWT " + token_value["access"] }
        url = 'http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/admin/users/' + args.username + '/'
        r = requests.get(url,headers=header)
        if r.ok:
            print(json.dumps(r.json(),indent=2))
        else :
            print(str(r.status_code) + " " + r.reason)
            print("A problem occured with your request.\nYou are probably not an admin.")
    elif sessionupd: 
        f = open("softeng20bAPI.token")
        source = open(args.source)
        token_value = json.load(f)
        header = {"Authorization" : "JWT " + token_value["access"]}
        url = "http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/admin/system/sessionsupd/"
        file = {'data_file': source}
        r = requests.post(url,files=file,headers = header)
        print (r.json())
    elif healthcheck: 
        r = requests.get("http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/admin/healthcheck/").json()
        print(r["status"])
    elif resetsessions: 
        r = requests.get("http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/admin/resetsessions/").json()
    else: print('Not correct usage')
    


