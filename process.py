import time
import random
import optparse

from null import Null

from qpid.messaging import Connection, Message, MessagingError

import model


parser = optparse.OptionParser(
    "usage: %prog [options] <model.dot>",
    description="Simulate a process moving within the given model")
parser.add_option("-b", "--broker", default=None,
                  help="If provided, events are published to the broker")
parser.add_option("-a", "--address", default="amq.topic",
                  help="Published events are sent to the given address")
parser.add_option("-i", "--identity", default=None,
                  help="Identity of this process")
opts, args = parser.parse_args()

if args:
    nodes = model.load(args.pop(0))
else:
    parser.error("model file required")

id = str(opts.identity or random.randint(0, 2**40))

for n in nodes:
    print n.name, n.size, map(lambda n: n.name, n.edges)

def next(node):
    return random.choice(node.edges.keys())

def move(node):
    return random.choice(filter(lambda n: n.name != node.name, node.edges.keys()))

connection = opts.broker and Connection(opts.broker) or Null()

try:
    connection.open()
    session = connection.session()
    sender = session.sender(opts.address)

    node = random.choice(nodes)
    node = reduce(lambda n, x: n.name == 'foyer' and n or x, nodes)
    now = 0
    sample_rate = .5 # in seconds
    acceleration = 10
    move_barrier = 30 * 60 # in seconds
    distance = node.size
    while True:
        now += sample_rate
        print id, now, node.name
        sender.send(Message([id, now, node.name]))
        if distance:
            distance-=1
        else:
            node = now % move_barrier == 0 and move(node) or next(node)
            distance = node.size
        time.sleep(sample_rate / acceleration)
except MessagingError, e:
    print e

connection.close()
