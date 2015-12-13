#!/usr/bin/env python
#
# Copyright (C) 2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''
IRC bot that forward 0mq messages to IRC chans.

It subscribes to a pub server and forward the message to the
configured IRC chans.
'''

from optparse import OptionParser

from txzmq import ZmqEndpoint
from txzmq import ZmqFactory
from txzmq import ZmqSubConnection
from twisted.internet import reactor


def main():
    parser = OptionParser("")
    parser.add_option("-m", "--method", dest="method",
                      help="0MQ socket connection: bind|connect")
    parser.add_option("-e", "--endpoint", dest="endpoint", help="0MQ Endpoint")
    parser.set_defaults(method="connect", endpoint="tcp://localhost:5555")

    (options, args) = parser.parse_args()

    zf = ZmqFactory()
    e = ZmqEndpoint(options.method, options.endpoint)

    s = ZmqSubConnection(zf, e)

    s.subscribe("")

    def doPrint(*args):
        print "message received: %r" % (args, )

    s.gotMessage = doPrint

    reactor.run()

main()

# zircbot.py ends here
