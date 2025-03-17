import filereader
import graph as graphs

for graph_number in range(1,15):
    file = filereader.readfile('tests/table ' + str(graph_number) + '.txt')
    graph = graphs.Graph(file.file_lines)
    graph.save_results(graph_number)