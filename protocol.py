#!/usr/bin/env python

import avro.protocol


_echo_protocol = '''{
        "protocol" : "AvroEcho",
        "namespace" : "rpc.sample.echo",
        "doc" : "Protocol for our AVRO echo server",
        "types" : [],
        "messages" : {
            "echo" : {
                "doc" : "Echo the string back",
                "request" : [
                        {"name" : "query", "type" : "string"}
                        ],
                "response"  : "string",
                "errors" : ["string"]
            },
            "split" : {
                "doc" : "Split the string in two and echo",
                "request" : [
                        {"name" : "query", "type" : "string"}
                        ],
                "response"  : "string",
                "errors" : ["string"]
            }
        }}'''

EchoProtocol = avro.protocol.parse(_echo_protocol)
