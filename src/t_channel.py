# -*- encoding: utf-8 -*-

import google.protobuf.service
import asyncore
import socket
import t_setting
import t_parser
import t_guid_mgr
import binascii
import t_buffer_mgr

class TRpcChannel(asyncore.dispatcher, google.protobuf.service.RpcChannel):
  def __init__(self):
    asyncore.dispatcher.__init__(self)
    google.protobuf.service.RpcChannel.__init__(self)
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connect((t_setting.HOST, t_setting.PORT))

    self.send_msg_list = []
    self.context_dict = {}

    self.buffer_mgr = t_buffer_mgr.TBufferMgr()

  def handle_connect(self):
    print '[TRpcChannel][handle_connect]'


  def SendMsg(self, msg):
    print '[TRpcChannel][SendMsg]', binascii.hexlify(msg)
    self.send_msg_list.append(msg)
    return

  def CallMethod(self, method_descriptor, rpc_controller,
                 request, response_class, done):
    print '[TRpcChannel][SendMsg]', request, self.connected
    if not self.connected:
      done(None)
      return

    call_guid = t_guid_mgr.GuidMgr.NewGuid()
    method_idx = method_descriptor.index
    data = request.SerializeToString()
    request_msg = t_parser.PackRequest(call_guid, method_idx, data)
    self.SendMsg(request_msg)
    # TODO: 放到handle_write中
    self.context_dict[call_guid] = [request, response_class, done]
    return

  def handle_close(self):
    print 'handle_close'
    self.close()

  def handle_expt(self):
    print 'handle_error'

  def writable(self):
    print '[TRpcChannel][writable]', len(self.send_msg_list), self.connected

    # 不加这一句会导致无法handle_connect
    if not self.connected:
      return True

    return len(self.send_msg_list)

  def readable(self):
    print '[TRpcChannel][readable]', self.connected
    return True

  def handle_read(self):
    msg = self.recv(t_setting.BUFF_SIZE)
    self.buffer_mgr.Append(msg)
    while self.buffer_mgr.HasPacket():
      packet = self.buffer_mgr.GetPacket()
      self.DealResponse(packet)

  def DealResponse(self, msg):
    print '[TRpcChannel][handle_read]', msg
    call_guid, data = t_parser.UnpackResponse(msg)
    request, response_class, done = self.context_dict.pop(call_guid)
    print '[TRpcChannel][handle_read]', request, response_class, done
    response = response_class()
    response.ParseFromString(data)
    done(response)
    return

  def handle_write(self):
    for msg in self.send_msg_list:
      self.send(msg)
    self.send_msg_list = []
    return