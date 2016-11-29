# -*- encoding: utf-8 -*-

import google.protobuf.service

class TRpcController(google.protobuf.service.RpcController):
  def __init__(self):
    super(TRpcController, self).__init__()

  def Reset(self):
    pass

  def Failed(self):
    pass

  def ErrorText(self):
    pass

  def StartCancel(self):
    pass

  def SetFailed(self):
    pass

  def IsCancled(self):
    pass

  def NotifyOnCancel(self, callback):
    pass
