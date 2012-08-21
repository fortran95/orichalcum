
import shelve, ConfigParser, os, sys, json
from optparse import OptionParser,OptionGroup
import daemon,windows,xisupport,msgpack

BASEPATH = os.path.dirname(sys.argv[0])
if BASEPATH != '':
    BASEPATH += '/'

op = OptionParser()

op.add_option("-i","--input",action="store",dest="input",default=False,help="Set the input file to be handled.")
op.add_option("-r","--receiver",action="store",dest="receiver",default=False,help="Specify the receiver.")
op.add_option("-a","--account",action="store",dest="account",default=False,help="Specify which account to be used.")
op.add_option("-t","--tag",action="store",dest="tag",default="im",help="Change message tag(default: im).")
op.add_option("-x","--xi",action="store_true", dest="usexi", default=False,help="Use xi system to encrypt. OVERRIDES user's decision in inputbox if any!")
op.add_option("-f","--flush",action="store_true",dest="omit",default=False,help="CAUTION: Omit any input, only push Xi generated messages(if any).")

(options,args) = op.parse_args()

if not options.omit:

    accountfile = ConfigParser.ConfigParser()
    accountfile.read(os.path.join(BASEPATH,'configs','accounts.cfg'))

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
            userinput = windows.inputbox(options.receiver,options.account,(xisupport.XI_ENABLED and options.usexi),(host,user))
            message = userinput['text']
            user_usexi = userinput['xi']
            if message == False:
                print "User cancelled."
                exit()
        except Exception,e:
            print "Error getting input: %s" % e
            exit()
    else:
        try:
            fp = open(options.input,'r')
            message = fp.read()
            fp.close()
        except Exception,e:
            print "File reading error: %s" % e
            exit()

# xi.postoffice support here.
if xisupport.XI_ENABLED and (options.usexi or user_usexi):

    if not options.omit:
        tag = json.dumps({'host':host,'secret':secret,'bits':bits,'tag':options.tag}).encode('hex')
        xisupport.xi_queue(user,options.receiver,tag,message)

    handleds = xisupport.xi_handled(True)
    for p in handleds:
        try:
            tag      = json.loads(p[2].decode('hex'))

            host     = tag['host']
            user     = p[0] # SENDER
            secret   = tag['secret']
            receiver = p[1] # RECEIVER
            
            # BODY
            message  = msgpack.enpack(tag['tag'],p[3],True)

            bits     = tag['bits']

            print "[%s] to [%s] is pushing." % (user,receiver)

            print message

            daemon.push_message(host,user,secret,receiver,message,bits) # TODO make this special to easily distinguish with non-Xi processed messages
        except Exception,e:
            print "Failed a letter: %s" % e
            continue
elif not options.omit:
    message = msgpack.enpack(options.tag,message,False)
    print daemon.push_message(host,user,secret,options.receiver,message,bits)
