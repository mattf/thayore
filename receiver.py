import optparse

import json

from proton import *

parser = optparse.OptionParser(
    "usage: %prog <address>",
    description="Receive published events from simulators")
opts, args = parser.parse_args()

mng = Messenger()
mng.start()

for a in args:
    mng.subscribe(a)

msg = Message()
while True:
    mng.recv()
    while mng.incoming:
        try:
            mng.get(msg)
        except Exception, e:
            print e
        else:
            print json.dumps(msg.properties)

mng.stop()
