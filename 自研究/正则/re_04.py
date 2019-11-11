import re


str_1 = "key = value".replace(" ","")
str_2 = "key=value"

str_1_kw = []
str_2_kw = []

str_1_kw = str_1.split("=")
str_2_kw = str_2.split("=")

# str_1_kw[0] = str_1_kw[0].replace(" ","")
# str_1_kw[1] = str_1_kw[1].replace(" ","")

print('*'*40)
print(str_1_kw)
print('*'*40)
print(str_2_kw)
print('*'*40)