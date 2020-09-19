
PI = 3.1415926

def circle_area(r):
    return PI * r * r

def test():
    print([circle_area(r) for r in range(1, 11)])
    
if __name__ == '__main__':
    test()
