#!/usr/bin/env python
#
# Copyright (C) 2015 Red Hat Inc.
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

''' Register a Trello webhook.
'''

import sys
import yaml

import trello

if len(sys.argv) != 4:
    print('Usage: %s <board id> <trello api key> <trello token>' % sys.argv[0])
    sys.exit(1)

config = yaml.load(open('config.yml').read())

client = trello.TrelloClient(sys.argv[2], token=sys.argv[3])

board = client.get_board(sys.argv[1])

print client.create_hook(config['webhook'], board.id)

# register-hook.py ends here
