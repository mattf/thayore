from qpid.messaging import Connection, MessagingError


broker = "localhost:5672"
address = "amq.topic"
connection = Connection(broker)

try:
    connection.open()
    session = connection.session()
    receiver = session.receiver(address)

    while True:
        message = receiver.fetch()
        print message.content
        session.acknowledge()

except MessagingError, e:
    print e

connection.close()
