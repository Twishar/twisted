
from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol


class QuoteProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numConnections += 1

    def dataReceived(self, data):
        print("Number of active connections: {}".format(self.factory.numConnections))
        print("> Received: ``{}''\n> Sending: ``{}''".format(data, self.getQuote()))
        self.transport.write(self.getQuote())
        self.updateQuote(data)

    def connectionLost(self, reason):
        self.factory.numConnections -= 1

    def getQuote(self):
        return self.factory.quote

    def updateQuote(self, quote):
        self.factory.quote = quote


class QuoteFactory(Factory):
    numConnections = 0
    protocol = QuoteProtocol

    def __init__(self, quote=None):
        self.quote = quote or "An apple a day keeps the doctor away kek"

    def buildProtocol(self, addr):
        return QuoteProtocol(self)


reactor.listenTCP(8000, QuoteFactory())
reactor.run()
