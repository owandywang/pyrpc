# -*- encoding: utf-8 -*-

class GuidMgr(object):
  guid = 0

  @classmethod
  def NewGuid(cls):
    cls.guid += 1
    return cls.guid


if __name__ == "__main__":
  for i in range(10):
    print GuidMgr.NewGuid()
