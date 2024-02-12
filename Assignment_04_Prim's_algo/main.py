import copy
from queue import PriorityQueue
import sys
import random


def inf():
    return 10000000000

class exceptionGraph(Exception):
    pass

class Graph(object):
    def __init__(self, vertices):
        self.__vertices = vertices
        self.__dictionaryCosts = {}
        self.__neighbours = {}
        self.__edges = {}
        for i in range(vertices):
            self.__neighbours[i] = []


    def parse_vertices(self):
        return self.__neighbours.keys()

    # returns the number of vertices in the graph
    def get_nr_of_vertices(self):
        return self.__vertices

    def add_vertex(self,vertex):
        if vertex in self.__neighbours.keys():
            raise exceptionGraph("Vertex already exists")
        self.__neighbours[vertex] = []
        self.__vertices += 1

    # returns the number of edges in the graph
    def get_nr_of_edges(self):
        return len(self.__dictionaryCosts.keys())



    # returns an interable containing
    # all the edges in the graph
    def parse_edges(self):
        return self.__dictionaryCosts.keys()

    def get_cost(graph):
        print("Input it as <vertex1,vertex2>")
        edge = input("\nInsert the edge you want to see the cost of")
        edge = edge.strip().split(",")
        vertex1 = int(edge[0])
        vertex2 = int(edge[1])
        print("The cost of this edge is: ", graph.get_cost(vertex1, vertex2))

    def get_edge_cost(self,vertex1,vertex2):
        if (vertex1, vertex2) in self.__dictionaryCosts.keys():
            return self.__dictionaryCosts[(vertex1,vertex2)]
        if (vertex2,vertex1) in self.__dictionaryCosts.keys():
            return self.__dictionaryCosts[(vertex2,vertex1)]
        return 100000000000

    def get_min_key(self,keyValue,isInMST):
        minim=inf()
        minIndex=-1
        for i in range(self.get_nr_of_vertices()):
            if keyValue[i]<minim and isInMST[i]==0:
                minim = keyValue[i]
                minIndex=i
        return minIndex

    # checks if there is an edge from 'vertex1'
    # to 'vertex2'
    # the vertices must be valid
    # otherwise it raises an exception
    # returns true if the edge exists, false otherwise
    def is_edge(self,vertex1,vertex2):
        if vertex1 not in self.__neighbours.keys() or vertex2 not in self.__neighbours.keys():
            raise exceptionGraph("Vertices are not valid")
        return vertex2 in self.__neighbours[vertex1]

    # adds an edge(vertex1,vertex2,cost) to the graph
    # raises an exception if the vertices do not exist
    # or if the edge already exists
    def add_edge(self,vertex1,vertex2,cost):
        if vertex1 not in self.__neighbours.keys() or vertex2 not in self.__neighbours.keys():
            raise exceptionGraph("Vertices do not exist")
        if self.is_edge(vertex1,vertex2):
            raise exceptionGraph("The edge already exists")
        if vertex1 == vertex2:
            raise exceptionGraph("There can't be an edge from a vertex to itself")
        self.__neighbours[vertex2].append(vertex1)
        self.__neighbours[vertex1].append(vertex2)
        self.__dictionaryCosts[(vertex1,vertex2)] = cost

    def MSTprim(self,startVertex):
        totalCost = 0
        edges = []
        inMST = []
        parent = []
        valueOfVertex = []

        #initialization
        for it in range(self.get_nr_of_vertices()):
            valueOfVertex.append(inf())

            inMST.append(0)

            parent.append(0)

        parent[startVertex]=-1
        inMST[startVertex]=1
        valueOfVertex[startVertex]=0

        nr_of_vertices = self.get_nr_of_vertices()
        currentVertex = startVertex

        #sorting edges
        for neighbour in self.__neighbours[currentVertex]:
            edgeCost=self.get_edge_cost(neighbour,currentVertex)
            if valueOfVertex[neighbour]>edgeCost and inMST[neighbour]==0:
                valueOfVertex[neighbour]=edgeCost
                parent[neighbour]=currentVertex


        #finding neighbors with lowest cost and then assigning them in inMST =1 and putting its parent
        while len(edges) < nr_of_vertices-1:
            currentVertex=self.get_min_key(valueOfVertex,inMST)
            inMST[currentVertex]=1
            edges.append([currentVertex,parent[currentVertex],self.get_edge_cost(currentVertex,parent[currentVertex])])
            for neighbour in self.__neighbours[currentVertex]:
                edgeCost = self.get_edge_cost(neighbour,currentVertex)
                if valueOfVertex[neighbour] > edgeCost and inMST[neighbour]==0:
                    valueOfVertex[neighbour]=edgeCost
                    parent[neighbour]=currentVertex

        #printing the MST
        edge = 0
        while edge < len(edges):
            print("edge: " + str(edges[edge][0]) + " - " + str(edges[edge][1]) +  " | cost: " + str(edges[edge][2]))
            totalCost += edges[edge][2]
            edge+=1
        print ("Total cost: ", totalCost)
        print ("That's the minimum spanning tree." )





def write_to_file(graph):
    file = input("-> The file you want to write the graph to: ")
    f = open(file, 'w')
    number_of_vertices = graph.get_nr_of_vertices()
    number_of_edges = graph.get_nr_of_edges()
    f.write(str(number_of_vertices) + ' ' + str(number_of_edges) + '\n')

    edges = graph.parse_edges()
    for vertices in edges:
        vertex1 = vertices[0]
        vertex2 = vertices[1]
        cost = graph.get_cost(vertex1, vertex2)
        f.write('Vertex1: ' + str(vertex1) + ' Vertex2: ' + str(vertex2) + ' Cost: ' + str(cost) + '\n')

        for isolatedVertex in graph.parse_vertices():
            if graph.get_vertex_degree(isolatedVertex) == 0:
                f.write(str(isolatedVertex) + ' -1 \n')

        f.close()

def read_file(file):
    try:
        f = open(file, 'r')
    except exceptionGraph:
        raise exceptionGraph("The file is not available")
    firstLine = f.readline().strip().split()
    graph = Graph(0)
    number_of_vertices = int(firstLine[0])

    line = f.readline()
    while line != "":
        edge = line.strip().split()
        vertex1 = int(edge[0])
        vertex2 = int(edge[1])
        if vertex1 not in graph.parse_vertices():
            graph.add_vertex(vertex1)
        if vertex2 not in graph.parse_vertices() and vertex2 != -1:
            graph.add_vertex(vertex2)
        if len(edge) == 3 and vertex1 != vertex2 and not graph.is_edge(vertex1, vertex2):
            graph.add_edge(vertex1, vertex2, int(edge[2]))
        line = f.readline()

    if number_of_vertices != graph.get_nr_of_vertices():
        for vertex in range(number_of_vertices):
            if vertex not in graph.parse_vertices():
                graph.add_vertex(vertex)

    f.close()
    return graph

def add_edge(graph):
    edge = input("\nInsert the edge you want to add as <vertex1,vertex2>")
    edge = edge.strip().split(",")
    vertex1 = int(edge[0])
    vertex2 = int(edge[1])
    cost = int(input("The cost is: "))
    graph.add_edge(vertex1, vertex2, cost)

def MST(graph):
    startVertex = int(input("The vertex you want to start from is: "))
    print("\n")
    graph.MSTprim(startVertex)

def random_graph(number_of_vertices, number_of_edges):
    minimum = int(input("Minimum cost: "))
    maximum = int(input("Maximum cost: "))

    if number_of_edges > number_of_vertices * number_of_vertices:
        raise exceptionGraph("The nr of edges must be < than nrVertices^2")

    graph = Graph(number_of_vertices)
    for vertex in range(number_of_edges):
        cost = random.randint(minimum, maximum)
        vertex1 = random.randrange(0, number_of_vertices)
        vertex2 = random.randrange(0, number_of_vertices)
        while graph.is_edge(vertex1, vertex2) or vertex1 == vertex2:
            vertex1 = random.randrange(0, number_of_vertices)
            vertex2 = random.randrange(0, number_of_vertices)
        graph.add_edge(vertex1, vertex2, cost)
    return graph

def run():
        while True:
            print("\n ----Problem 6 solved using Prim's Algorithm-----\n")
            command = input(">")
            try:
                if command == "file":
                    file = input("The file name is: ")
                    graph = read_file(file)
                    MST(graph)
                elif command == "random":
                    number_vertices = int(input("Number of vertices: "))
                    number_edges = int(input("Number of edges: "))
                    graph = random_graph(number_vertices, number_edges)
                elif command == "exit":
                    return
                else:
                    print("Inexistent command")
            except Exception as e:
                print("Error: " + str(e))


run()

