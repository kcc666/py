import random
first_name = ["张","黄","刘","李","陈","蔡"]
last_name = ["帅","桥","天","美","花","奇","琳","坤","徐","娇","芝"]


for i in range(20):
    if random.randint(1,2) == 1:
        print(random.choice(first_name)+random.choice(last_name))
    else:
        print(random.choice(first_name)+random.choice(last_name)+random.choice(last_name))
