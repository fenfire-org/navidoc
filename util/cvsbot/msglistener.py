from twisted.internet.protocol import Protocol, Factory

class MsgListener(Protocol):
    buffer = ''
    def dataReceived(self, data):
        self.buffer += data

    def doCommitMessage(self, mp):
        by = mp.getReceivedFrom
        msg = mp.getCommitMessage
	project = mp.getProject
        mp.getAddedFiles()
        mp.getModifiedFiles()
        mp.getRemovedFiles()
        return mp.formatMessage(by(), msg(), project())


    def connectionLost(self, reason):
        """Connection is lost, so we can flood the channels."""
        botf = self.factory.bot
        mp = self.factory.mp(self.buffer)
        botf.instance.notice(botf.channel, self.doCommitMessage(mp))

class MsgListenerFactory(Factory):
    protocol = MsgListener

    def __init__(self, bot, mp):
        self.bot = bot
        self.mp = mp
        
    # XXX, need to check here, whether the connection is coming
    # from an acceptable host or not.
