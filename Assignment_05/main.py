from UndirectedGraph import UndirectedGraph

class myException(Exception):
    pass

class Console:

    def __init__(self):
        self.__fileName = "graph.txt"
        self.__options = {"1": self.__loadGraph, "2": self.__vertexCover, "3": self.__greedyVertexCover,
                          "4": self.__addEdge, "5": self.__addVertex}

    def __printMenu(self):
        print("Options: ")
        print("1-load graph")
        print("2-print the approximate vertex cover (maximum 2*optimal number of vertices)")
        print("4-add edge")
        print("5-add vertex")
        print("exit-to quit the program")

    def __loadGraph(self):
        try:
            with open(self.__fileName, "r") as file:
                firstLine = file.readline()
                firstLine = firstLine.strip().split()
                vertices, edges = int(firstLine[0]), int(firstLine[1])
                self.__graph = UndirectedGraph(vertices)
                for times in range(edges):
                    line = file.readline()
                    line = line.strip().split()
                    start, end, cost = int(line[0]), int(line[1]), int(line[2])
                    try:
                        self.__graph.addEdge(start, end)
                    except myException as me:
                        continue
            print("Graph loaded.")
        except IOError:
            raise myException("File Reading Error")

    def __vertexCover(self):
        print("(using non-optimal approach) The vertices forming the approximate minimum vertex cover are: ")
        print(self.__graph.approximateVertexCover())

    def __greedyVertexCover(self):
        print("(using greedy approach) The vertices forming the approximate minimum vertex cover are:")
        print(self.__graph.greedyVertexCover())

    def __addEdge(self):
        print("x:")
        x = int(input())
        print("y:")
        y = int(input())
        try:
            self.__graph.addEdge(x, y)
        except myException as me:
            print(me)

    def __addVertex(self):
        print("x:")
        x = int(input())
        try:
            self.__graph.addVertex(x)
        except myException as me:
            print(me)

    def main(self):
        print(">>")
        while True:
            self.__printMenu()

            cmd = input()

            if cmd == "exit":
                return
            elif cmd in self.__options:
                self.__options[cmd]()


c = Console()
c.main()