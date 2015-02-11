import optparse

from qpid.messaging import Connection, MessagingError

parser = optparse.OptionParser(
    "usage: %prog [broker url]",
    description="Receive published events from simulators")
parser.add_option("-a", "--address", default="amq.topic",
                  help="Receive events on the given address")
opts, args = parser.parse_args()

broker = args and args.pop(0) or "localhost:5672"

connection = Connection(broker)
try:
    connection.open()
    session = connection.session()
    receiver = session.receiver(opts.address)

    while True:
        message = receiver.fetch()
        print message.content
        session.acknowledge()

except MessagingError, e:
    print e

connection.close()
