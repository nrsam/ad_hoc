SOL = [83, 60, 57, 88, 40, 33, 36, 48, 29, 47, 14, 7, 55, 30, 0, 8, 72, 52, 96, 21, 42, 39, 82, 69, 94, 2, 46, 93, 81, 77, 38, 95, 84, 32, 97, 22, 86, 16, 44, 50, 5, 78, 73, 23, 3, 85, 24, 61, 75, 1, 51, 98, 34, 43, 80, 62, 41, 20, 70, 19, 79, 66, 18, 10, 89, 99, 90, 4, 6, 26, 15, 74, 87, 71, 25, 91, 76, 17, 9, 92, 53, 31, 65, 67, 45, 13, 27, 59, 54, 35, 12, 49, 56, 28, 11, 63, 58, 64, 37, 68]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == '__main__':
    n = len(SOL)
    print(n)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            assert SOL[i] != SOL[j]
            assert abs(SOL[i] - SOL[j]) != abs(i-j)
    for i in range(n):
        print(bcolors.OKBLUE + '#' * SOL[i], end='') 
        print(bcolors.OKGREEN + 'Q', end='') 
        print(bcolors.OKBLUE + '#' * (n - 1 - SOL[i])) 

