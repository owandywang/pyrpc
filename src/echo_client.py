# -*- encoding: utf-8 -*-

import echo_service_pb2
import t_channel
import t_controller
import asyncore
import time

# 要返回response的话，需要增加context_map，在response返回时能够找到callback
# 如果出错，直接调用callback

def Callback(response = None):
  print '[Callback]', response
  return

if __name__ == "__main__":
  rpc_channel = t_channel.TRpcChannel()
  service_stub = echo_service_pb2.EchoService_Stub(rpc_channel)
  asyncore.loop(1, count=1)

  print 'start call...'
  request = echo_service_pb2.EchoRequest()
  request.ping = 123
  rpc_controller = t_controller.TRpcController
  callback = Callback
  service_stub.Echo(rpc_controller, request, callback)

  asyncore.loop(1)