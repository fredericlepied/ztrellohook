ztrellohook
===========

ztrellohook is a basic server to implement a notification system for a
trello board using 0mq.

Installation
++++++++++++

Using virtualenv and pip, you can provision the needed dependencies
using the following commands::
  
  $ virtualenv env
  $ . env/bin/activate
  $ pip install -r requirements.txt

Then copy ``config-sample.yml`` into ``config.yml`` and edit it to
suit your needs.

Trello credentials
++++++++++++++++++

If you don't have API keys, you can get them using the following URL:
https://trello.com/1/appKey/generate .

To obtain your token: https://trello.com/1/authorize?key=API-KEY-HERE&name=Trello+IRC&expiration=never&response_type=token .

Register your Trello webhook
++++++++++++++++++++++++++++

You need to have the webserver running before registering your webhook
as trello will call the webhook to validate that the url is correct::
  
  $ ./ztrellohook.py

To register your webhook, you can use the following command::

   $ ./register-hook.py <board id> <trello api key> <trello token>

More documentation at https://developers.trello.com/advanced-reference/webhook
