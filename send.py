
import shelve, ConfigParser, os, sys, json
from optparse import OptionParser,OptionGroup
import daemon,windows

BASEPATH = os.path.dirname(sys.argv[0])
if BASEPATH != '':
    BASEPATH += '/'

op = OptionParser()

op.add_option("-i","--input",action="store",dest="input",default=False,help="Set the input file to be handled.")
op.add_option("-r","--receiver",action="store",dest="receiver",default=False,help="Specify the receiver.")
op.add_option("-a","--account",action="store",dest="account",default=False,help="Specify which account to be used.")
op.add_option("-t","--tag",action="store",dest="tag",default="im",help="Change message tag(default: im).")

(options,args) = op.parse_args()

accountfile = ConfigParser.ConfigParser()
accountfile.read(BASEPATH + 'configs/accounts.cfg')

if options.account == False:
    print "Please specify account name(defined in configs/accounts.cfg) using -a/--account."
    exit()
if options.receiver == False:
    print "Please specify the receiver using -r/--receiver."
    exit()
if accountfile.has_section(options.account) == False:
    print "Account [%s] does not exists." % options.account
    exit()

host = accountfile.get(options.account,'host')
user = accountfile.get(options.account,'user')
secret=accountfile.get(options.account,'secret')
bits = accountfile.get(options.account,'bits')

# Read file to get message
if options.input == False:
    try:
        message = windows.inputbox(options.receiver,options.account)
        if message == False:
            print "User cancelled."
            exit()
    except Exception,e:
        pass
else:
    try:
        fp = open(options.input,'r')
        message = fp.read()
        fp.close()
    except Exception,e:
        print "File reading error: %s" % e
        exit()
        
print "-------- Will now push the message --------"

# Pack message.
message = json.dumps({'tag':options.tag,'message':message})

print daemon.push_message(host,user,secret,options.receiver,message,bits)