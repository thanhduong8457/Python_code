class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart


def main():
    temp_list = {
        'temp1' : [1, 2], 
        'temp2' : [1, 2], 
        'temp3' : [1, 2]
    }
    
    for key, value in temp_list.items():
        print(temp_list[key][1])

if __name__ == '__main__':
    main()
