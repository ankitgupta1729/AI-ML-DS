print("hello world")

a = float(99)+100
print(a)

print(9/2)

print(int('123')+1)

name = input("Enter your name: ")
print("Hello",name)  # the comma makes space between name and Hello

print(max("Hello world")) 
print(min("Hello world"))

n=5
while n>0:
    print(n)
    n=n-1
print("Blastoff!")
print(n) # n is 0

while True:
    line = input('> ')
    if line == 'done':
        break
    print(line)
print('Done!')

while True:
    line = input('> ')
    if line[0] == '#':
        continue
    if line == 'done':
        break
    print(line)
print('Done!')


# Finding the smallest number in a list

smallest = None
print('Before:', smallest)
for value in [9, 41, 12, 3, 74, 15]:
    if smallest is None :
        smallest = value 
    elif value < smallest:
        smallest = value
    print('Loop:',smallest, value)
print('Smallest:', smallest)


""" Outpue 
╭─🍎 ankit@MacBook-Air 💻  …/AI-ML-DS on  main [ ✱1 ?2  ] 🐍  v3.14.2 
╰─ /Users/ankit/.local/share/uv/python/cpython-3.13.14-macos-aarch64-none/bin/python /Users/ankit/Workspace/Pro
jects/ankit-github/AI-ML-DS/45.Python-for-Everybody-University-of-Michigan-Charles-Severance-PhD/py4e/hello.py
hello world
199.0
4.5
124
Enter your name: ankit
Hello ankit
w
 
5
4
3
2
1
Blastoff!
0
> hi
hi
> done
Done!
> done
Done!
Before: None
Loop: 9 9
Loop: 9 41
Loop: 9 12
Loop: 3 3
Loop: 3 74
Loop: 3 15
Smallest: 3

"""