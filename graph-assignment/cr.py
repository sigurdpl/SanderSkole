from typing import final
from graph import *
from graph_io import load_graph, write_dot, save_graph
import copy
from collections import Counter, defaultdict
import cProfile
# nothing
graphlist = ['crSamples/test_3reg.grl', 'crSamples/colorref_smallexample_4_7.grl', 'crSamples/colorref_smallexample_6_15.grl', 'crSamples/test_iter.grl', 'crSamples/colorref_largeexample_6_960.grl']

enkleGrafer = ['crSamples/enkelGraf.grl']

benchmarklist = ['Benchmark_instances/CrefBenchmark1.grl', 'Benchmark_instances/CrefBenchmark6.grl', 'Benchmark_instances/CrefBenchmark5.grl', 'Benchmark_instances/CrefBenchmark2.grl']

benchmarklist2 = [
    'Benchmark_instances/CrefBenchmark1.grl',
    'Benchmark_instances/CrefBenchmark2.grl',
    'Benchmark_instances/CrefBenchmark3.grl',
    'Benchmark_instances/CrefBenchmark4.grl',
    'Benchmark_instances/CrefBenchmark5.grl',
    'Benchmark_instances/CrefBenchmark6.grl'
]
graphlist2 = [
    'crSamples/colorref_largeexample_4_1026.grl',
    'crSamples/colorref_largeexample_6_960.grl',
    'crSamples/colorref_smallexample_2_49.grl',
    'crSamples/colorref_smallexample_4_16.grl',
    'crSamples/colorref_smallexample_4_7.grl',
    'crSamples/colorref_smallexample_6_15.grl',
    'crSamples/cref9vert3comp_10_27.grl',
    'crSamples/cref9vert_4_9.grl',
    'crSamples/test_3reg.grl',
    'crSamples/test_cref9.grl',
    'crSamples/test_cycles.grl',
    'crSamples/test_empty.grl',
    'crSamples/test_iter.grl',
    'crSamples/test_trees.grl'
]

class graphInfo():
    def __init__(self):
        self.colour_mapping = {} 
        self.current_colour = 0 


def basic_colorref(graphlist):
    with open(benchmarklist2[4]) as f:
        L = load_graph(f, read_list=True)

    results = []
    graph_colour_freq = []
    graph_colour_freq_list = []
    colour_freq_list = []
    itr_list = []
    discrete_list = []
    graphInf = graphInfo()
    # this is where i call the function once for each graph
    for i in range(len(L[0])):
        # res = cr(L[0][i], graphInf)
        # results.append(res)
        cf, itr, discrete, freq_thing = cr(L[0][i], graphInf)
        temporary_colour_freq = ()
        temporary_freq_thing = ()
        for num in sorted(cf):
            temporary_colour_freq += tuple([num] * cf[num])
        for num in sorted(freq_thing):
            temporary_freq_thing += tuple([num] * freq_thing[num])
        graph_colour_freq_list.append(temporary_freq_thing)
        colour_freq_list.append(temporary_colour_freq)
        itr_list.append(itr)
        discrete_list.append(discrete)
        results.append((cf, itr, discrete))
        graph_colour_freq.append(freq_thing)


    equiv_dict = {}
    for i in range(len(L[0])):
        equiv_key = (colour_freq_list[i], itr_list[i], discrete_list[i], graph_colour_freq_list[i])
        if equiv_key not in equiv_dict:
            equiv_dict[equiv_key] = []
        equiv_dict[equiv_key].append(i)

    # print("here is the equiv dict")
    # print(equiv_dict.values())

    final_output = []
    for i in equiv_dict.values():
        temp_final_output = tuple([i, list(colour_freq_list[i[0]]), itr_list[i[0]], discrete_list[i[0]]])
        final_output.append(temp_final_output)

    # print("here is the final output?")
    # print(final_output)

    return final_output

def cr(graph_num, graphInf:graphInfo):
    # with open(benchmarklist[1]) as f:
        # L = load_graph(f, read_list=True)

    # G = L[0][graph_num] # first graph Change function to take graph as param later
    G = graph_num
    
    # init dicts and initialise colouring of all verticies to the colour 1.
    previous_colouring = {vertex.label: 1 for vertex in G.vertices}
    colouring_multiset = {vertex.label: [] for vertex in G.vertices}
    current_colouring = {vertex.label: 1 for vertex in G.vertices}

    previous_partition = {}

    # step 2 init iteration count to 0
    itr_count = 0
    # print(f"graph: {G}")
    # step 3 enter while loop
    while True: 
        neighbours = {vertex.label: [] for vertex in G.vertices}

        for vertex in G.vertices:
            # finds the neighbours of the current vertex
            vertex_neighbours = [incident.other_end(vertex).label for incident in vertex.incidence]
            neighbours[vertex.label] = sorted(vertex_neighbours)
            # colours for neighbours from previous iteration
            nh_colouring = [previous_colouring[x] for x in vertex_neighbours]
            colouring_multiset[vertex.label] = sorted(nh_colouring) # {1: (1,1)]}


        partition_dict = {}
        # colour_mapping = {}# {(1,1): 1, (1,1,1): 2}
        # current_colour = 0

        for vert, neighbours_list in colouring_multiset.items():
            neighbours_list_tuple = tuple(neighbours_list)
            partition_dict.setdefault(neighbours_list_tuple, []).append(vert)
            if neighbours_list_tuple not in graphInf.colour_mapping:
                graphInf.current_colour += 1
                graphInf.colour_mapping[neighbours_list_tuple] = graphInf.current_colour # {(1,1): 5}

        nodes_to_skip = []
        for prev_partition, curr_partition in zip(previous_partition.values(), partition_dict.values()):
            if prev_partition == curr_partition:
                nodes_to_skip_current = [x for x in curr_partition]
                nodes_to_skip.extend(nodes_to_skip_current)

        stable = False
        if len(nodes_to_skip) == len(G.vertices):
            stable = True

        for vert, neighbours_list in colouring_multiset.items(): 
            # if vert in nodes_to_skip:
                # continue
            neighbours_list_tuple = tuple(neighbours_list)
            current_colouring[vert] = graphInf.colour_mapping[neighbours_list_tuple] # {1: (1,1)]}

        if previous_colouring == current_colouring or stable:
            # print(f"\nStable colouring reached after {itr_count} iterations")
            frequency_counter = Counter(Counter(current_colouring.values()).values())
            freq_thing = Counter(current_colouring.values())
            # print(f"what have i counted?{freq_thing}")
            isDiscrete = False
            if list(frequency_counter.values())[0] == len(G.vertices):
                isDiscrete = True
            # print(f"colouring multiset: {colouring_multiset}")
            # print(f"colour mapping: {graphInf.colour_mapping}")
            # print(f"colouring: {current_colouring}")
            # print(f"previous partition: {previous_partition}, current partition: {partition_dict}")

            # print(f"final colour num: {graphInf.current_colour}")
            return dict(frequency_counter), itr_count, isDiscrete, freq_thing

        previous_partition = partition_dict.copy()
        previous_colouring = current_colouring.copy()
        itr_count += 1
        # print(graphInf.current_colour)

# colour_refinement()


