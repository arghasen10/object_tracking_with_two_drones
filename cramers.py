def det(matrix, mul = 1):
    width = len(matrix)
    if width == 1:
        return mul * matrix[0][0]
    else:
        sign = -1
        total = 0
        for i in range(width):
            m = []
            for j in range(1, width):
                buff = []
                for k in range(width):
                    if k != i:
                        buff.append(matrix[j][k])
                m.append(buff)
            sign *= -1
            total += mul * det(m, sign * matrix[0][i])
        return total


def Cramer(matrix):
    n = len(matrix)
    mainMat = []
    for i in range(n):
        mainMat.append([])
        for j in range(n):
            mainMat[i].append(matrix[i][j])
    mainDet = det(mainMat)

    if mainDet != 0:
        for r in range(n):
            nowMat = []
            for i in range(n):
                nowMat.append([])
                for j in range(n):
                    if j == r:
                        nowMat[i].append(matrix[i][n])
                    else:
                        nowMat[i].append(matrix[i][j])
            print('x', r+1, '=', det(nowMat) / mainDet)

'''

print('Enter number of unknowns = n')
n = int(input())
print('sequentially enter the elements of matrix n*(n+1)')
matrix = []
for i in range(n):
    matrix.append([])
    for j in range(n + 1):
        matrix[i].append(float(input()))
'''
matrix = [[4,-6,-3,-10],[1,1,-2,3],[4,-20,-4,6]]
Cramer(matrix)
