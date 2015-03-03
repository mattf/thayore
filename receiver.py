import optparse

from proton import *

parser = optparse.OptionParser(
    "usage: %prog <address>",
    description="Receive published events from simulators")
opts, args = parser.parse_args()

mng = Messenger()
mng.start()

for a in args:
    print a
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
            print msg.address, msg.subject or "(no subject)", msg.properties, msg.body

mng.stop()
