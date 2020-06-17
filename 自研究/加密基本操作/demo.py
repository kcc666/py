import hashlib

#1 ######## md5 ########
# 目的：实现对b"HelloIt's me" 这句话进行md5加密
m = hashlib.md5()            # 1）生成一个md5加密对象
m.update("你好".encode("UTF8"))          # 2）使用m对 b"Hello" 加密
# m.update(b"It's me")        # 3) 使用m对 b"It's me"加密
print(m.hexdigest())         # 4) 最终加密结果就是对b"HelloIt's me"加密的md5值：5ddeb47b2f925ad0bf249c52e342728a

#2 ######## sha1 ########
hash = hashlib.sha1()
hash.update(b'admin')
print(hash.hexdigest())

#3 ######## sha256 ########
hash = hashlib.sha256()
hash.update(b'admin')
print(hash.hexdigest())

#4 ######## sha384 ########
hash = hashlib.sha384()
hash.update(b'admin')
print(hash.hexdigest())

#5 ######## sha512 ########
hash = hashlib.sha512()
hash.update(b'admin')
print(hash.hexdigest())
