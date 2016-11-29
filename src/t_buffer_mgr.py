# -*- encoding: utf-8 -*-

import struct

class TBufferMgr(object):
  def __init__(self):
    self.buffer_list = []
    self.start_cursor = 0
    self.total_size = 0

  def Dump(self):
    print '----------------'
    print self.buffer_list
    print self.start_cursor
    print self.total_size
    print '-----------------'

  def Append(self, buffer):
    self.buffer_list.append(buffer)
    self.total_size += len(buffer)

  def GetPacketSize(self):
    if self.total_size < 4:
      return
    packet_size_data = self.PeekN(4)
    packet_size = struct.unpack('<I', packet_size_data)[0]
    return packet_size

  def HasPacket(self):
    if not self.buffer_list:
      return False
    if self.total_size < 4:
      return False
    packet_size = self.GetPacketSize()
    if not packet_size:
      return False
    if self.total_size < 4 + packet_size:
      return False
    else:
      return True

  def GetPacket(self):
    if not self.HasPacket():
      return
    data1 = self.ReadN(4)
    msg_size = struct.unpack('<I', data1)[0]
    data2 = self.ReadN(msg_size)
    return data1 + data2

  def PeekN(self, n):
    return self.ReadN(n, is_peek=True)

  def ReadN(self, n, is_peek = False):
    if self.total_size < n:
      print 'read error'
      return

    data = ''
    old_start_cursor = self.start_cursor
    next_cursor = self.start_cursor
    total_size = self.total_size
    next_total_size = self.total_size
    left_size = n
    finish_line_num = 0

    for line in self.buffer_list:
      # self.Dump()
      line_left_size = len(line) - next_cursor
      if line_left_size > left_size:
        next_next_cursor = next_cursor + left_size
        data += line[next_cursor : next_next_cursor]
        next_cursor = next_next_cursor
        next_total_size -= left_size
        left_size = 0
        break
      elif line_left_size == left_size:
        data += line[next_cursor:]
        next_cursor = 0
        next_total_size -= left_size
        finish_line_num += 1
        left_size = 0
        break
      else:
        line_data = line[next_cursor:]
        line_data_size = len(line_data)
        data += line_data
        next_cursor = 0
        next_total_size -= line_data_size
        finish_line_num += 1
        left_size = n - len(data)

    if not is_peek:
      self.buffer_list = self.buffer_list[finish_line_num : ]

    if is_peek:
      self.start_cursor = old_start_cursor
    else:
      self.start_cursor = next_cursor
      self.total_size = next_total_size
    return data

def PackData(data):
  data_len = len(data)
  msg_size = data_len
  msg = struct.pack('<I%ds' % data_len, msg_size, data)
  return msg

def UnpackData(msg):
  msg_size = struct.unpack('<I', msg[0:4])[0]
  data_len = msg_size
  print data_len
  data = struct.unpack('<%ds' % data_len, msg[4:])[0]
  return data



def Test1():
  buff_mgr = TBufferMgr()
  buff_mgr.Append('abc')
  buff_mgr.Append('defgh')
  print '-----------------'
  print buff_mgr.PeekN(3)
  print '-----------------'
  print buff_mgr.PeekN(8)


  print '-----------------'
  print buff_mgr.ReadN(3)
  print buff_mgr.ReadN(1)
  print buff_mgr.ReadN(3)
  print buff_mgr.ReadN(1)

def Test2():
  buff_mgr = TBufferMgr()

  msg3 = PackData('abc')
  msg5 = PackData('defgh')
  msg6 = PackData('ijklmn')

  buff_mgr.Append(msg3[:2])
  buff_mgr.Append(msg3[2:])
  print buff_mgr.total_size

  buff_mgr.Append(msg5)
  print buff_mgr.total_size

  buff_mgr.Append(msg6[:3])
  buff_mgr.Append(msg6[3:5])
  buff_mgr.Append(msg6[5:])
  print buff_mgr.total_size


  for i in range(3):
    msg = buff_mgr.GetPacket()
    print 'msg---', msg, len(msg)
    print 'total_size:', buff_mgr.total_size
    print UnpackData(msg)

if __name__ == "__main__":
  Test1()
  Test2()


