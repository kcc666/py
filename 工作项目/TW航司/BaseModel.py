#! /usr/bin/env python
# coding=utf-8
import json


class BaseModel():
    def __init__(self):
        pass

    def toMap(self):
        d = {}
        for k, v in self.__dict__.items():
            d[k] = v
        return d

    def fromMap(self, d):
        for k, v in d.items():
            if k in self.__dict__:
                self.__dict__[k] = v
        return self

    def toJson(self):
        return json.dumps(self.toMap())

    def fromJson(self, string):
        loadDict = json.loads(string)
        self.fromMap(loadDict)
        return self

    def fromObject(self, obj):
        assert isinstance(obj, BaseModel)
        self.fromMap(obj.toMap())
        return self
    #读一行文件,变成对象
    def readFromTextLine(self, line, splitChar, cNames=[]):
        try:
            for index, item in enumerate(line.split(splitChar)):
                if cNames[index] in self.__dict__:
                    self.__dict__[cNames[index]] = item
        except Exception as e:
            pass
            # print e
        return self
    #生成一行文件
    def toTextLine(self, splitChar=',', cNames=[], head=False):
        body = []
        if cNames:
            for name in cNames:
                if name in self.__dict__:
                    if head:
                        body.append(name)
                    else:
                        body.append(str(self.__dict__[name]))
        else:
            for k, v in sorted(self.__dict__.items()):
                if head:
                    body.append(str(k))
                else:
                    body.append(str(v))
        return splitChar.join(body)


#通过属性查找
    # obj 是其他对象
    # lookupdict 是自身列与 obj 列对应关系
    #valuedict 是自身列与 obj 列值获取关系
    #all 是否完全匹配,true 表示全匹配,false 表示有一个匹配就算匹配
    def vlookup(self,obj,lookupDict={},valueDict={},all=True):
        ok=0
        for myAttr,objAttr in lookupDict.items():
            if str(self.__dict__.get(myAttr,"myAttr"))==str(obj.__dict__.get(objAttr,"objAttr")):
                ok+=1

        if (ok==len(lookupDict) and all) or (not all and ok>0):
            for k,v in self.__dict__.items():
                if k in valueDict:
                    self.__dict__[k]=obj.__dict__.get(v,None)
        return self



