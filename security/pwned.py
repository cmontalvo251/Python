#!/usr/bin/env python
import hashlib ##Hashing algorithm
import sys
import requests ##pull stuff from an url

###Routine to actually check passwords
def lookup_pwned_api(pwd):
    sha1pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
    head, tail = sha1pwd[:5], sha1pwd[5:]
    print "SHA1 = ",head,tail
    url = 'https://api.pwnedpasswords.com/range/' + head
    res = requests.get(url)
    if res.status_code != 200: ##It looks like 200 is success and everything else is not
        raise RuntimeError('Error fetching "{}": {}'.format(url, res.status_code))

    for line in res.text.splitlines():
        print head,line
    hashes = (line.split(':') for line in res.text.splitlines())
    count = next((int(count) for t, count in hashes if t == tail), 0)

    return sha1pwd, count

####Main routine with args
#def main(args): #I don't like doing it this way
args = sys.argv[1:]
if len(args) == 0:
    print "No passwords given"
    sys.exit()
print "Passwords = ",args
ec = 0
for pwd in args:
    pwd = pwd.strip()
    print "Trying password = ",pwd
    try:
        sha1pwd, count = lookup_pwned_api(pwd)
        
        if count:
            foundmsg = "{0} was found with {1} occurrences (hash: {2})"
            print(foundmsg.format(pwd, count, sha1pwd))
            ec = 1
        else:
            print("{} was not found".format(pwd)) ##This is also really cool
    except UnicodeError:
        errormsg = sys.exc_info()[1]
        print("{0} could not be checked: {1}".format(pwd, errormsg))
        ec = 1

#########
# if __name__ == '__main__':
#     sys.exit(main(sys.argv[1:])) ##Oh wow this is genius but I don't like it
