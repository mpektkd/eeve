import argparse
import textwrap

def msg(name=None):                                                            
    return "General Usage:ev_group13 SCOPE --param1 value1 [--param2 value2 ...]--format fff --apikeykkk\n"

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
parser = argparse.ArgumentParser(usage=msg(),parents = [parent_parser])

# SCOPE        
subparser = parser.add_subparsers(dest='command',help='SCOPE')
healthcheck = subparser.add_parser('healthcheck', parents = [parent_parser],usage="ev_group13 healthcheck --format fff --apikeykkk\n")
resetsessions = subparser.add_parser('resetsessions',parents = [parent_parser],usage = "ev_group13 resetsessions --format fff --apikeykkk\n")
login = subparser.add_parser('login',parents = [parent_parser],usage = "ev_group13 login --username Username --passw Password --format fff --apikeykkk\n")
logout = subparser.add_parser('logout',parents = [parent_parser],usage = "ev_group13 logout --format fff --apikeykkk\n")
SessionsPerPoint = subparser.add_parser('SessionsPerPoint',parents = [parent_parser],usage = "ev_group13 SessionsPerPoint --point Point --datefrom DateFrom --dateto DateTo --format fff --apikeykkk\n")
SessionsPerStation = subparser.add_parser('SessionsPerStation',parents = [parent_parser],usage = "ev_group13 SessionsPerStation --format fff --apikeykkk\n")
SessionsPerEV = subparser.add_parser('SessionsPerEV',parents = [parent_parser],usage = "ev_group13 resetsessions --format fff --apikeykkk\n")
SessionsPerProvider = subparser.add_parser('SessionsPerProvider',parents = [parent_parser],usage = "ev_group13 resetsessions --format fff --apikeykkk\n")
Admin = subparser.add_parser('Admin',parents = [parent_parser],usage="ev_group13 Admin --MainParameter --Subparameters --format fff --apikeykkk\n")


#Admin_subparsers = Admin.add_parser(dest='command',help='Main Parameter')

login_required = login.add_argument_group('login required arguments')
login_required.add_argument('--username', type=str, required=True)
login_required.add_argument('--passw', type=str, required=True)

SessionsPerPoint.add_argument('--point', type=str, required=True)
SessionsPerPoint.add_argument('--datefrom', type=str, required=True)
SessionsPerPoint.add_argument('--dateto', type=str, required=True)

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
    print("healthcheckapi")
elif args.command == 'resetsessions':
    print('resetsessionsapi')
elif args.command == 'login':
    print("loginapi/nToken must be saved at {HOME}/softeng20bAPI.token")
elif args.command == 'logout':
    print("logoutapi/nsession token must be deleted")
elif args.command == 'SessionsPerPoint':
    print("/sessionsperpoint")
elif args.command == 'SessionsPerStation':
    print("/sessionsperstation")
elif args.command == 'SessionsPerEV':
    print("/sessionsperEV")
elif args.command == 'SessionsPerProvider':
    print("/sessionsperProvider")
elif args.command == 'Admin':
    usermod = args.usermod and args.username and args.passw  and (not(args.users or args.sessionsupd or args.source or args.healthcheck or args.resetsessions))
    users = args.users and args.username and (not(args.usermod or args.passw or args.sessionsupd or args.source or args.healthcheck or args.resetsessions))
    sessionupd = args.sessionsupd and args.source and (not(args.usermod or args.username or args.passw or args.users or args.healthcheck or args.resetsessions))
    healthcheck = args.healthcheck and (not(args.usermod or args.username or args.passw or args.users or args.sessionsupd or args.source or args.resetsessions))
    resetsessions = args.resetsessions and (not(args.usermod or args.username or args.passw or args.users or args.sessionsupd or args.source or args.healthcheck))
    
    if usermod: print ("/usermod")
    elif users: print ("/users")
    elif sessionupd: print ("/sessionsupd")
    elif healthcheck: print ("/healthcheck")
    elif resetsessions: print ("resetsessions")
    else: print('Not correct usage')
    


