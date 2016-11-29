# -*- encoding: utf-8 -*-

import struct

def PackRequest(call_guid, method_idx, data):
  data_len = len(data)
  msg_size = 8 + data_len
  msg = struct.pack('<III%ds' % data_len, msg_size, call_guid, method_idx, data)
  return msg

def UnpackRequest(msg):
  msg_size = struct.unpack('<I', msg[0:4])[0]
  data_len = msg_size - 8
  call_guid = struct.unpack('<I', msg[4:8])[0]
  method_idx = struct.unpack('<I', msg[8:12])[0]
  data = struct.unpack('<%ds' % data_len, msg[12:])[0]
  return [call_guid, method_idx, data]


def PackResponse(call_guid, data):
  data_len = len(data)
  msg_size = 4 + data_len
  msg = struct.pack('<II%ds' % data_len, msg_size, call_guid, data)
  return msg

def UnpackResponse(msg):
  msg_size = struct.unpack('<I', msg[0:4])[0]
  data_len = msg_size - 4
  call_guid = struct.unpack('<I', msg[4:8])[0]
  data = struct.unpack('<%ds' % data_len, msg[8:])[0]
  return [call_guid, data]

Ip2Int = lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])])

def Address2Key(address):
  ip = address[0]
  port = address[1]
  ip_int = Ip2Int(ip)
  key_str = '%s%s' % (ip_int, port)
  return int(key_str)