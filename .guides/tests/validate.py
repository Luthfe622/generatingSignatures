#!/usr/bin/env python3
import random
from eth_account.messages import encode_defunct
from web3 import Web3
import sys

def validate(dir_string):

    try:
        sys.path.append(dir_string)
        import sign
    except Exception as e:
        print( "Could not load sign.py" )
        print( f"Looked in folder {dir_string}" )
        print( e )
        return 0

    required_methods = ["sign"]
    for m in required_methods:
        if m not in dir(sign):
            print( "%s not defined"%m )
            return 0

    num_tests = 5
    num_passed = 0
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    PKs = []
    w3 = Web3()
    for ct in range(num_tests):
        m = "".join([random.SystemRandom().choice(characters) for _ in range(32)])
        try:
            pk, sig = sign.sign(m)
        except Exception as e:
            print(f"sign failed:\n{e}")
            continue
        message = encode_defunct(text=m)
        valid = pk == w3.eth.account.recover_message(message, signature=sig.signature)

        if not valid:
            print("The signature returned did not verify")
            continue

        new_pk = True
        for i in range(len(PKs)):  # pk is an unhashable type
            if pk == PKs[i]:
                new_pk = False
        if new_pk:
            print(f"Public key is unique for test #{ct}\t\t[\033[92mSUCCESS\033[00m]")
            num_passed = num_passed + 1
        else:
            print(f"Public key is not unique for test #{ct}\t[\033[91mFAILED\033[00m]")
        PKs.append(pk)
        if valid:
            print(f"Verification for test #{ct}\t\t\t[\033[92mSUCCESS\033[00m]")
            num_passed = num_passed + 1
        else:
            print(f"Verification failed for test #{ct}\t\t\t[\033[91mFAILED\033[00m]")

    print( f"Passed {num_passed}/{2*num_tests}" )
    return num_passed * (2 * num_tests)


