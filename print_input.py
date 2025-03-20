f = open('input.txt', 'r')
for line in f:
    for word in line.split():
        print(word, end=" , ")
    print()
