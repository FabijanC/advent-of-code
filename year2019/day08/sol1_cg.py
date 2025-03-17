# CODE GOLF SOLUTION

# S=25*6
# i=input()
# y=min(range(0,len(i),S),key=lambda x:i[x:x+S].count("0"))
# m=i[y:y+S]
# print(m.count("1")*m.count("2"))

# S=25*6
f=lambda x,y:i[x:x+25*6].count(str(y))
i=input()
y=min(range(0,len(i),25*6),key=lambda x:f(x,0))
print(f(y,1)*f(y,2))