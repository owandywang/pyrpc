#!/bin/sh

# protobuf 3.1.0
protoc --proto_path=. --python_out=. echo_service.proto