#!/usr/bin/env python

import StringIO

import eventlet
import eventlet.wsgi
eventlet.monkey_patch()

import avro.ipc

import protocol

HOST = '127.0.0.1'
PORT = 8130

class EchoResponder(avro.ipc.Responder):
    def invoke(self, message, request):
        handler = 'handle_%s' % message.name
        if not hasattr(self, handler):
            raise Exception('I can\'t handle this message! (%s)' % message.name)
        return getattr(self, handler)(message, request)

    def handle_split(self, message, request):
        query = request['query']
        halfway = len(query) / 2
        return query[:halfway]

    def handle_echo(self, message, request):
        return request['query']

responder = EchoResponder(protocol.EchoProtocol)

def wsgi_handler(env, start_response):
    ## Only allow POSTs, which is what Avro should be doing
    if not env['REQUEST_METHOD'] == 'POST':
        start_response('500 Error', [('Content-Type', 'text/plain')])
        return ['Invalid REQUEST_METHOD\r\n']

    ## Pull the avro rpc message off of the POST data in `wsgi.input`
    reader = avro.ipc.FramedReader(env['wsgi.input'])
    request = reader.read_framed_message()
    response = responder.respond(request)

    ## avro.ipc.FramedWriter really wants a file-like object to write out to
    ## but since we're in WSGI-land we'll write to a StringIO and then output the
    ## buffer in a "proper" WSGI manner
    out = StringIO.StringIO()
    writer = avro.ipc.FramedWriter(out)
    writer.write_framed_message(response)

    start_response('200 OK', [('Content-Type', 'avro/binary')])
    return [out.getvalue()]

def main():
    listener = eventlet.listen((HOST, PORT))
    eventlet.wsgi.server(listener, wsgi_handler)
    return 0

if __name__ == '__main__':
    exit(main())

