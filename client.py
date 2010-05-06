#!/usr/bin/env python

import optparse
import time

import avro.ipc

import protocol

HOST = '127.0.0.1'
PORT = 8130

def send_echo(client, query):
    start = time.time()
    requestor = avro.ipc.Requestor(protocol.EchoProtocol, client)
    print '>>> Echo: %s' % requestor.request('echo', {'query' : query})
    finish = time.time()
    print '(took %s)' % (finish - start)
    return 0

def send_split(client, query):
    start = time.time()
    requestor = avro.ipc.Requestor(protocol.EchoProtocol, client)
    print '>>> Split: %s' % requestor.request('split', {'query' : query})
    finish = time.time()
    print '(took %s)' % (finish - start)
    return 0

def main():
    opts = optparse.OptionParser()
    opts.add_option('-e', '--echo', dest='echo', action='store_true',
            help='Echo the `query`')
    opts.add_option('-s', '--split', dest='split', action='store_true',
            help='Split the `query`')
    opts.add_option('-q', '--query', dest='query',
            help='Query to send to Avro echo server')
    options, args = opts.parse_args()

    if not options.query:
        print '>>> Need a `--query`'
        return -1

    if not options.echo and not options.split:
        print '>>> Must either `--echo` or `--split` the `query`'
        return -1

    query = options.query
    client = avro.ipc.HTTPTransceiver(HOST, PORT)

    if options.echo:
        return send_echo(client, query)
    if options.split:
        return send_split(client, query)

    return 0

if __name__ == '__main__':
    exit(main())
