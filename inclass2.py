import igraph

def enumerate_matrix(matrix, i):
    return [x+1 for x in range(len(matrix[i])) if matrix[i][x] != 0]

def enumerate_adj_list(lst, i):
    return lst[i]

def dosim(n):
    graph = igraph.Graph.Barabasi(n, n)

if __name__ == "__main__":
    #dosim(10)
    matrix = [[0, 1, 0, 0, 1, 0],
              [1, 0, 1, 1, 0, 0],
              [0, 1, 0, 1, 1, 1],
              [0, 1, 1, 0, 0, 0],
              [1, 0, 1, 0, 0, 0],
              [0, 0, 1, 0, 0, 0]]
    
    lst = [[]]
    
    print enumerate_matrix(matrix, 2)