import time
import random

import model

nodes = model.load('layout.dot')

for n in nodes:
    print n.name, n.size, map(lambda n: n.name, n.edges)

def next(node):
    return random.choice(node.edges.keys())

def move(node):
    return random.choice(filter(lambda n: n.name != node.name, node.edges.keys()))

node = random.choice(nodes)
node = reduce(lambda n, x: n.name == 'foyer' and n or x, nodes)
now = 0
sample_rate = .5 # in seconds
acceleration = 10
move_barrier = 30 * 60 # in seconds
distance = node.size
while True:
    now += sample_rate
    print now, node.name
    if distance:
        distance-=1
    else:
        node = now % move_barrier == 0 and move(node) or next(node)
        distance = node.size
    time.sleep(sample_rate / acceleration)
