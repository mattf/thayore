import time
import random
import optparse

from null import Null

from proton import *

import model


parser = optparse.OptionParser(
    "usage: %prog [options] <model.dot>",
    description="Simulate a process moving within the given model")
parser.add_option("-a", "--address", default=None,
                  help="AMQP 1.0 address, e.g. amqp://0.0.0.0")
parser.add_option("-i", "--identity", default=None,
                  help="Identity of this process")
parser.add_option("-s", "--seed", default=None,
                  help="Random seed")
parser.add_option("-t", "--time", default=None, type="int",
                  help="Time (sec since EPOCH) for first event")
parser.add_option("-q", "--quiet", default=False, action="store_true",
                  help="Silence per event console output")
parser.add_option("-c", "--count", default=-1, type="int",
                  help="If provided, number of events to generate otherwise infinite")
parser.add_option("-l", "--location", default=None,
                  help="Name of initial location")
parser.add_option("-d", "--debug", default=False, action="store_true",
                  help="Enable debug output")
opts, args = parser.parse_args()

if args:
    nodes = model.load(args.pop(0))
else:
    parser.error("model file required")

random.seed(opts.seed)

id = str(opts.identity or random.randint(0, 2**40))

if opts.debug:
    for n in nodes:
        print n.name, n.size, map(lambda n: n.name, n.edges)

def next(node):
    return random.choice(node.edges.keys())

def move(node):
    return random.choice(filter(lambda n: n.name != node.name, node.edges.keys()))

mng = opts.address and Messenger() or Null()
mng.start()

try:
    node = random.choice(nodes)
    if opts.location:
        node = reduce(lambda n, x: n.name == opts.location and n or x, nodes)
    now = opts.time and opts.time or round(time.time())
    sample_rate = .5 # in seconds
    acceleration = 10
    move_barrier = 30 * 60 # in seconds
    distance = node.size
    msg = Message()
    while opts.count < 0 or opts.count > 0:
        event = {'scannerID': node.name, 'uuid': id, 'time': now}
        print event
        msg.address = opts.address
        msg.properties = event
        mng.put(msg)
        mng.send()
        if distance:
            distance-=1
        else:
            node = now % move_barrier == 0 and move(node) or next(node)
            distance = node.size
        time.sleep(sample_rate / acceleration)
        now += sample_rate
        opts.count-=1
except MessagingError, e:
    print e

mng.stop()
