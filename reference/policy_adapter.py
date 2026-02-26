#!/usr/bin/env python3
import json, math, sys
from collections import Counter

def entropy(xs):
    c=Counter(xs); n=sum(c.values()) or 1
    return -sum((v/n)*math.log2(v/n) for v in c.values())

def evaluate(receipts):
    types=[r.get('proof_type','unknown') for r in receipts]
    issuers=[r.get('issuer','unknown') for r in receipts]
    h=entropy(types)
    uniq=len(set(issuers))/max(1,len(issuers))
    if h>1.2 and uniq>0.7: tier='auto_release'
    elif h>0.7 and uniq>0.5: tier='optimistic_release'
    else: tier='manual_verification'
    return {'entropy':round(h,4),'issuer_independence':round(uniq,4),'tier':tier}

if __name__=='__main__':
    obj=json.load(open(sys.argv[1]))
    print(json.dumps(evaluate(obj.get('receipts',[])),indent=2))
