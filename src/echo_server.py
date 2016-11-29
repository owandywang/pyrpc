# -*- encoding: utf-8 -*-

import asyncore
import echo_service_pb2
import t_acceptor

class EchoServiceImpl(echo_service_pb2.EchoService):
  def __init__(self):
    super(EchoServiceImpl, self).__init__()
    self.service_stub = None

  def Echo(self, rpc_controller, request, callback):
    print "[MyEchoService][Echo]"
    response = echo_service_pb2.EchoResponse()
    response.pong = request.ping
    print 'response:', response
    callback(response)
    return

if __name__ == "__main__":
  rpc_service = EchoServiceImpl()
  acceptor = t_acceptor.TAcceptor(rpc_service)
  asyncore.loop()
