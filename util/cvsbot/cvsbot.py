# Twisted, the Framework of Your Internet
# Copyright (C) 2001 Matthew W. Lefkowitz
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU General Public
# License as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
from twisted.internet.protocol import Protocol, Factory
from twisted.protocols import irc
from twisted.internet import reactor, protocol
from twisted.internet.app import Application

import time
import os.path


class Bot(irc.IRCClient):
    """An IRC bot."""
    def __init__(self, nick):
        self.nickname = nick

    def signedOn(self):
        self.join(self.factory.channel)

class BotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    # the class of the protocol to build
    protocol = Bot
    instance = None   

    def buildProtocol(self, addr):
        p = self.protocol(self.nick)
        p.factory = self
        self.instance = p 
        return p

    def __init__(self, botnick, channel):
        self.nick = botnick
        self.channel = channel
 
    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()

if __name__ == '__main__':
    from twisted.internet.app import Application
    import gzz_mail_parser, msglistener


    mp = gzz_mail_parser.GZZMailParser
    botf = BotFactory('cvsbot', '#fenfire')
    mlf = msglistener.MsgListenerFactory(botf, mp)

    app = Application("cvsbot")

    app.connectTCP("irc.jyu.fi", 6667, botf)
    app.listenTCP(9999, mlf)
    app.run()


