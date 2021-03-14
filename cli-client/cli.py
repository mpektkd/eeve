import argparse
import sys
import json
import requests
import os
import pprint
import csv

from requests import status_codes

def csv_print_point(text):
    csvf = open ("csv.csv", "a")
    csvf.write(text)
    csvf.close()
    csvfl = open ("csv.csv","r")
    csv_f = csv.reader(csvfl)
    print("EnergyDelivered|-----FinishedOn----|-Payment--|Protocol|SessionID|SessionIndex|-----StartedOn-----|VehicleType")
    count = 0
    rows = 0
    for row in csv_f:
        linecount = 0
        counter = 0
        for i in row:
            counter = counter + 1
            if i == "NumberOfChargingSessions":
                rows = counter/8
            if count == 1 and rows > counter/8:
                if linecount ==0: 
                    print('{:^15}'.format(i),end="|")
                if linecount ==1: 
                    print('{:^5}'.format(i),end="|")
                if linecount ==2: 
                    print('{:^10}'.format(i),end="|")
                if linecount ==3: 
                    print('{:^8}'.format(i[0:7]),end="|")
                if linecount ==4: 
                    print('{:^9}'.format(i),end="|")
                if linecount ==5: 
                    print('{:^12}'.format(i),end="|")
                if linecount ==6: 
                    print('{:^5}'.format(i),end="|")
                if linecount ==7:    
                    print(i)
                    linecount =-1
                linecount = linecount +1
            elif count==1 and rows <= counter/8:
                if linecount ==0: 
                    print('\nNumberOfChargingSessions: ' + str(i))
                if linecount ==1: 
                    print('Date From: ' + str(i))
                if linecount ==2: 
                    print('Date to: ' + str(i))
                if linecount ==3: 
                    print('Point ID: ' + str(i))
                linecount +=1
        count = count +1
    print("\n")
    os.remove("csv.csv")


def parse_args(args):

#format and apikey are always required
    
    parser = argparse.ArgumentParser()

    # SCOPE        
    subparser = parser.add_subparsers(dest='command',help='SCOPE') #Implementation of SCOPE aspect with the use of subparser
    #healthcheck scope
    healthcheck = subparser.add_parser('healthcheck', usage="ev_group13 healthcheck")
    #resetsessions scope
    resetsessions = subparser.add_parser('resetsessions',usage = "ev_group13 resetsessions")
    #login scope
    login = subparser.add_parser('login',usage = "ev_group13 login --username USERNAME --passw PASSWORD\n.")
    #logout scope
    logout = subparser.add_parser('logout',usage = "ev_group13 logout")
    #SessionsPerPoint scope
    SessionsPerPoint = subparser.add_parser('SessionsPerPoint',usage = "ev_group13 SessionsPerPoint --point POINT --datefrom YYMMDD --dateto YYMMDD --format fff\n.")
    #SessionsPerStation scope
    SessionsPerStation = subparser.add_parser('SessionsPerStation',usage = "ev_group13 SessionsPerStation --station STATION --datefrom YYMMDD --dateto YYMMDD --format fff\n.")
    #SessionsPerEV scope
    SessionsPerEV = subparser.add_parser('SessionsPerEV',usage = "ev_group13 SessionsPerEV --ev EV --datefrom YYMMDD --dateto YYMMDD --format fff \n.")
    #SessionsPerProvider scope
    SessionsPerProvider = subparser.add_parser('SessionsPerProvider',usage = "ev_group13 SessionsPerProvider --provider PROVIDER --datefrom DATEFROM --dateto DATETO --format fff --format fff\n.")
    #Admin Scope
    Admin = subparser.add_parser('Admin',usage="ev_group13 Admin --MainParameter --Subparameters \nMain Parameters Supported : --usermod | --users | --healthcheck | --resetsessions | --sessionsupd\n\n")

    #arguments needed in login scope
    login_required = login.add_argument_group('login required arguments')
    login_required.add_argument('--username', type=str, required=True)
    login_required.add_argument('--passw', type=str, required=True)

    #arguments needed in SessionsPerPoint scope
    SessionsPerPoint_required = SessionsPerPoint.add_argument_group('SessionsPerpoint required arguments')
    SessionsPerPoint_required.add_argument('--point', type=str, required=True)
    SessionsPerPoint_required.add_argument('--datefrom', type=str, required=True)
    SessionsPerPoint_required.add_argument('--dateto', type=str, required=True)
    SessionsPerPoint_required.add_argument('--format', type=str,required=True)

    #arguments needed in SessionsPerStation scope
    SessionsPerStation_required = SessionsPerStation.add_argument_group('SessionsPerStation required arguments')
    SessionsPerStation_required.add_argument('--station',type=str,required=True)
    SessionsPerStation_required.add_argument('--datefrom', type=str, required=True)
    SessionsPerStation_required.add_argument('--dateto', type=str, required=True)
    SessionsPerStation_required.add_argument('--format',type=str, required=True)

    #arguments needed in SessionsPerEV scope
    SessionsPerEV_required = SessionsPerEV.add_argument_group('SessionsPerEV required arguments')
    SessionsPerEV_required.add_argument('--ev', type=str, required=True)
    SessionsPerEV_required.add_argument('--datefrom', type=str, required=True)
    SessionsPerEV_required.add_argument('--dateto', type=str, required=True)
    SessionsPerEV_required.add_argument('--format',type=str,required=True)

    #arguments needed in SessionsPerEV scope
    SessionsPerProvider_required = SessionsPerProvider.add_argument_group('SessionsPerProvider required arguments')
    SessionsPerProvider_required.add_argument('--provider', type=str, required=True)
    SessionsPerProvider_required.add_argument('--datefrom', type=str, required=True)
    SessionsPerProvider_required.add_argument('--dateto', type=str, required=True)
    SessionsPerProvider_required.add_argument('--format',type=str,required=True)

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

    return parser.parse_args(args)



def msg(name=None):                                                            
    return "\nGeneral Usage:ev_group13 SCOPE [--params values] \nScopes Supported: healthcheck|resetsessions|login|logout|SessionsPerPoint|SessionsPerStation|SessionsPerEV|SessionsPerProvider|Admin\n.\n.\n"



args = parse_args(sys.argv[1:])
if (vars(args))['command'] == None :
    print('General Usage:ev_group13 SCOPE [--params values] \nScopes Supported: healthcheck|resetsessions|login|logout|SessionsPerPoint|SessionsPerStation|SessionsPerEV|SessionsPerProvider|Admin')
base_url = "http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/"


#healthcheck
if args.command == 'healthcheck':
    url = base_url + 'admin/healthcheck' 
    r = requests.get(url).json()
    print(json.dumps(r, indent=2))


#resetsessions
elif args.command == 'resetsessions':
    r = requests.get("http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/admin/resetsessions/").json()
    print(json.dumps(r,indent=2))

#Login
elif args.command == 'login':
    url = base_url + 'login/'
    params = {
    "username": args.username,
    "password": args.passw
    }
    if os.path.exists("softeng20bAPI.token"):
        print("You are already logged in!")
    else:
        json_object = requests.post(url,json=params).json()
        if 'detail' in json_object:
            print (json_object["detail"])
        else:
            f = open("softeng20bAPI.token","w")
            f.write(json.dumps(json_object,indent = 2))
            print ("Login Succsessfull...\nWelcome to eevie, " + args.username + '!')
        

#logout
elif args.command == 'logout': 
    url = base_url + 'logout/'
    if not os.path.exists("softeng20bAPI.token"):
        print("You are not logged in.")
        sys.exit()
    f = open("softeng20bAPI.token")
    token_value = json.load(f) 
    header = {"Authorization" : "X-OBSERVATORY-AUTH " + token_value["access"] }
    r = requests.post(url,headers=header,json=token_value)
    if r.ok:
        print("Bye")
        os.remove("softeng20bAPI.token")
    else:
        os.remove("softeng20bAPI.token")
        print(str(r.status_code)+" " + r.reason)
        print("Token on system had expired")  


#SessionsPerPoint
elif args.command == 'SessionsPerPoint':
    url = base_url + 'SessionsPerPoint/' + args.point + '/' + args.datefrom + '_from/' + args.dateto + '_to/?format=' + args.format
    if not os.path.exists("softeng20bAPI.token"):
            print("Not Logged in.")
            sys.exit()
    f = open("softeng20bAPI.token")
    token_value = json.load(f) 
    header = {"Authorization" : "X-OBSERVATORY-AUTH " + token_value["access"] }
    r = requests.get(url,headers=header)
    if r.ok:
        if args.format == 'json':
            print(json.dumps(r.json(),indent = 1))
        elif args.format == 'csv':
            csv_print_point(r.text)
    else:
        print(str(r.status_code) + ' ' + r.reason)

#SessionsPerStation
elif args.command == 'SessionsPerStation':
    url = base_url + 'SessionsPerStation/' + args.station + '/' + args.datefrom + '_from/' + args.dateto + '_to/?format=' + args.format
    if not os.path.exists("softeng20bAPI.token"):
            print("Not Logged in.")
            sys.exit()
    f = open("softeng20bAPI.token")
    token_value = json.load(f) 
    header = {"Authorization" : "X-OBSERVATORY-AUTH " + token_value["access"] }
    r = requests.get(url,headers=header)
    if r.ok:
        if args.format == 'json':
            print(json.dumps(r.json(),indent = 1))
        elif args.format == 'csv':
            print (r.text)
    else:
        print(str(r.status_code) + ' ' + r.reason)


#SessionsPerEV
elif args.command == 'SessionsPerEV':
    url = base_url + 'SessionsPerEV/' + args.ev + '/' + args.datefrom + '_from/' + args.dateto + '_to/?format=' + args.format
    if not os.path.exists("softeng20bAPI.token"):
            print("Not Logged in.")
            sys.exit()
    f = open("softeng20bAPI.token")
    token_value = json.load(f) 
    header = {"Authorization" : "X-OBSERVATORY-AUTH " + token_value["access"] }
    r = requests.get(url,headers=header)
    if r.ok:
        if args.format == 'json':
            print(json.dumps(r.json(),indent = 1))
        elif args.format == 'csv':
            print(r.text)
    else:
        print(str(r.status_code) + ' ' + r.reason)

#SessionsPerProvider
elif args.command == 'SessionsPerProvider':
    url = base_url + 'SessionsPerProvider/' + args.provider + '/' + args.datefrom + '_from/' + args.dateto + '_to/?format=' + args.format
    if not os.path.exists("softeng20bAPI.token"):
            print("Not Logged in.")
            sys.exit()
    f = open("softeng20bAPI.token")
    token_value = json.load(f) 
    header = {"Authorization" : "X-OBSERVATORY-AUTH " + token_value["access"] }
    r = requests.get(url,headers=header)
    if r.ok:
        if args.format == 'json':
            print(json.dumps(r.json(),indent = 1))
        elif args.format == 'csv':
            print(r.text)
    else:
        print(str(r.status_code) + ' ' + r.reason)

#Admin
elif args.command == 'Admin':
    usermod = args.usermod and args.username and args.passw  and (not(args.users or args.sessionsupd or args.source or args.healthcheck or args.resetsessions))
    users = args.users and args.username and (not(args.usermod or args.passw or args.sessionsupd or args.source or args.healthcheck or args.resetsessions))
    sessionupd = args.sessionsupd and args.source and (not(args.usermod or args.username or args.passw or args.users or args.healthcheck or args.resetsessions))
    healthcheck = args.healthcheck and (not(args.usermod or args.username or args.passw or args.users or args.sessionsupd or args.source or args.resetsessions))
    resetsessions = args.resetsessions and (not(args.usermod or args.username or args.passw or args.users or args.sessionsupd or args.source or args.healthcheck))

    #Admin usermod
    if  usermod: 
        if not os.path.exists("softeng20bAPI.token"):
            print("Not Logged in.")
            sys.exit()
        f = open("softeng20bAPI.token")
        token_value = json.load(f)
        header = {"Authorization" : "X-OBSERVATORY-AUTH " + token_value["access"] }
        url = 'http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/admin/usermod/' + args.username + '/' + args.passw + '/'
        r = requests.post(url,headers=header)
        if r.ok:
            print(r.content)
        else :
            print(str(r.status_code) + " " + r.reason)
            print("A problem occured with your request.\nYou are probably not an admin.")

    #Admin users
    elif users:
        if not os.path.exists("softeng20bAPI.token"):
            print("Not Logged in.")
            sys.exit()
        f = open("softeng20bAPI.token")
        token_value = json.load(f)
        header = {"Authorization" : "X-OBSERVATORY-AUTH " + token_value["access"] }
        url = 'http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/admin/users/' + args.username + '/'
        r = requests.get(url,headers=header)
        if r.ok:
            print(json.dumps(r.json(),indent=2))
        else :
            print(str(r.status_code) + " " + r.reason)
            print("A problem occured with your request.\nYou are probably not an admin.")


    #Admin sessionsupd
    elif sessionupd:
        if not os.path.exists("softeng20bAPI.token"):
            print("Not Logged in.")
            sys.exit() 
        f = open("softeng20bAPI.token")
        source = open(args.source)
        token_value = json.load(f)
        header = {"Authorization" : "X-OBSERVATORY-AUTH " + token_value["access"]}
        url = "http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/admin/system/sessionsupd/"
        file = {'data_file': source}
        r = requests.post(url,files=file,headers = header)
        print (r.json())

    #Admin healthcheck
    elif healthcheck: 
        if not os.path.exists("softeng20bAPI.token"):
            print("Not Logged in.")
            sys.exit()
        r = requests.get("http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/admin/healthcheck/").json()
        print(json.dumps(r,indent=2))

    #Admin resetsessions
    elif resetsessions: 
        if not os.path.exists("softeng20bAPI.token"):
            print("Not Logged in.")
            sys.exit()
        r = requests.get("http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/admin/resetsessions/").json()
        print(r)
    else: print('No Main Parameter Given\nUsage:ev_group13 Admin --MainParameter [--Subparameters] \nMain Parameters Supported : --usermod | --users | --healthcheck | --resetsessions | --sessionsupd')
    


