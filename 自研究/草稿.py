
def middle(lst):
    len_lst = len(lst)
    if len_lst % 2 == 0:
        return (lst[int(len_lst/2)-1]+lst[int(len_lst/2)])/2
    else:
        return lst[int(len_lst/2)]

ret = middle([3,7,-12,-4,5,5])
print("*"*30)
print(ret)
print("*"*30)







print(3//2)