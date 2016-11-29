# -*- encoding: utf-8 -*-

import asyncore
import socket
import echo_service_pb2
import t_setting
import t_parser
import t_session

class TAcceptor(asyncore.dispatcher):
  def __init__(self, rpc_service):
    asyncore.dispatcher.__init__(self)
    self.session_dict = {}
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.set_reuse_addr()
    self.bind((t_setting.HOST, t_setting.PORT))
    self.listen(5)
    self.rpc_service = rpc_service

  def handle_accept(self):
    conn, address = self.accept()
    print '[TServer][handle_accept]', conn, address
    new_session = t_session.TSession(self.rpc_service, conn, address, self)
    self.session_dict[t_parser.Address2Key(address)] = new_session
    return

  def handle_close(self):
    print '[server][handle_accept]'
    self.close()
    return

  def handle_error(self):
    return

  def Stop(self):
    self.close()
    return



