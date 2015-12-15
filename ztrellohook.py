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
'''

import trello, requests, yaml, sys, time, shlex
import base64, hashlib, hmac, json, traceback

from txzmq import ZmqEndpoint
from txzmq import ZmqFactory
from txzmq import ZmqPubConnection
from twisted.internet import reactor, task, defer, protocol
from twisted.python import log
from twisted.words.protocols import irc
from twisted.application import internet, service
from twisted.web import server, resource

with open('config.yml') as f:
    _CONFIG = yaml.load(f.read())


def base64digest(data, secret):
    chksum = hmac.new(secret, data, hashlib.sha1)
    return base64.b64encode(chksum.digest())


def validate_request(body, url, secret, result):
    chksm = base64digest(body + url, secret)
    return base64digest(chksm, secret) == base64digest(result, secret)


class TrelloHook(resource.Resource):
    isLeaf = True

    def __init__(self):
        self.zmq_factory = None

    def render_GET(self, request):
        return 'titi'

    def render_POST(self, request):
        headers = request.getAllHeaders()
        if not 'x-trello-webhook' in headers:
            log.msg('no HTTP_X_TRELLO_WEBHOOK header: %s' % headers)
            request.setResponseCode(404)
            return 'Invalid page %s' % headers

        valid = False
        for key in _CONFIG["trello_api_secrets"]:
            valid = validate_request(request.content.getvalue(),
                                     _CONFIG.get('webhook', ''),
                                     key,
                                     headers['x-trello-webhook'])
            if valid:
                break
        if not valid:
            request.setResponseCode(404)
            log.msg('Not called from trello.com: %s' %
                    headers['x-trello-webhook'])
            log.msg('content: %s' % request.content.getvalue())
            return 'Not called from trello.com.'

        data = json.loads(request.content.getvalue())

        if data and self.zmq_factory:
            for conn in self.zmq_factory.connections:
                conn.publish(json.dumps({'trello': data}))

        return ''

if __name__ == '__main__':
    log.startLogging(sys.stderr)

    site = server.Site(TrelloHook())
    reactor.listenTCP(_CONFIG['port'], site)

    zf = ZmqFactory()
    e = ZmqEndpoint(_CONFIG['method'], _CONFIG['endpoint'])

    s = ZmqPubConnection(zf, e)

    site.resource.zmq_factory = zf

    reactor.run()

# ztrellohook.py ends here
