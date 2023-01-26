class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart


def main():
    x = Complex(3.0, -4.5)
    print(x.i)
    print(x.r)

if __name__ == '__main__':
    main()
