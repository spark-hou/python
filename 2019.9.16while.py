import random
serect=random.randint(1,10)
print("answer is :", serect)


print("------------spark-text--------------")
temp=input("enter the number:")
val=int(temp)
while val!=serect:
  
    if val==serect:
        print("right")

    else:
        print("no")
        temp=input("try again:")
        val=int(temp)

print("game,over")
