'''
The main idea of this code is simulate the behavior of MLV proposal

1. Create a graph (e.g. a tree);
2. Create elements in the graph;
3. Put information in each node;
4. Walking through the graph.

The main example for be analyzed 

                        AS 1
                      /     \
                     /      \
                    /       \
                AS 2       AS 3
              /     \    /      \
             /      \   /       \
            /       \  /        \
       AS 4 ----> AS 5 <------>AS 6
      />   <\    />    <\    />   <\
     /      \   /      \   /      \
    /       \  /  /     \  /       \
AS 7 ------> AS 8        AS 9 ----> AS 10


'''

import networkx as nx
import copy

PREFIX_SIZE = 4
LINK_SIZE = 32


class Prefix_MLV():

    def __init__(self, ASN, path):
        self.ASN = ASN
        self.path = [path]

    def add_path(self, path):
        if path in self.path:
            pass
        else:
            self.path.append(path)


class MLV_Updates():

    def __init__(self, ASN,list_of_prefixes):
        self.ASN = ASN
        self.list_of_prefixes = list_of_prefixes
        self.list_of_neighbors = []
        self.RIB = {}
        self.number_of_update_messages = 0
        for prefix in list_of_prefixes:
            self.RIB[prefix] = [self.ASN]

    def update_neighbor(self, neighbor):
        if neighbor in self.list_of_neighbors:
            pass
        else:
            self.list_of_neighbors.append(neighbor)

    def update_RIB(self,prefixes, AS_PATH):
        self.number_of_update_messages += 1
        for prefix in prefixes:
            if prefix in self.RIB:
                as_path = self.RIB[prefix]
                if len(as_path) > len(AS_PATH):
                    #print self.ASN, " new prefix ", prefix,as_path, AS_PATH
                    self.RIB[prefix] = AS_PATH
            else:
                #print self.ASN," new prefix ", prefix, AS_PATH
                self.RIB[prefix] = AS_PATH

    def get_number_updates(self):
        return self.number_of_update_messages

    def get_neighbors(self):
        return self.list_of_neighbors

    def get_prefixes(self):
        return self.list_of_prefixes

    def get_RIB(self):
        return  self.RIB

    def __str__(self):
        return str(self.ASN)

    def __unicode__(self):
        return self.ASN

    def __repr__(self):
        return str(self.ASN)


def add_neighbors(Internet, neighbor1, neighbor2):
    Internet.add_edge(neighbor1,neighbor2)
    neighbor1.update_neighbor(neighbor2)
    neighbor2.update_neighbor(neighbor1)


def create_topo_fig_6():
    Internet = nx.DiGraph()
    Internet.add_edge(7,8)
    Internet.add_edge(7,4)

    Internet.add_edge(8,4)
    Internet.add_edge(8,5)
    Internet.add_edge(8,6)

    Internet.add_edge(9,5)
    Internet.add_edge(9,6)
    Internet.add_edge(9,10)

    Internet.add_edge(10,6)

    Internet.add_edge(4,5)
    Internet.add_edge(4,2)

    Internet.add_edge(5,2)
    Internet.add_edge(5,3)
    Internet.add_edge(5,6)

    Internet.add_edge(6,5)
    Internet.add_edge(6,3)

    Internet.add_edge(2,3)
    Internet.add_edge(2,1)
    Internet.add_edge(3,2)
    Internet.add_edge(3,1)
    return Internet

def create_topo_fig_4():
    as1 = 1
    as2 = 2
    as3 = 3
    as4 = 4
    Internet = nx.DiGraph()
    Internet.add_edge( as1, as2)
    Internet.add_edge( as1, as3)
    Internet.add_edge( as2, as3)
    Internet.add_edge( as2, as4)
    Internet.add_edge( as3, as4)
    return Internet


'''
The simultaneous advertisement each prefix is advertised individually (worst case scenario).
'''

def count_mlv_simultaneous_advertisement(Internet, asn_src, asn_dst,number_of_prefixes):
    # if asn_src != 1:
    #     return 0
    count = 0
    prefix_size = PREFIX_SIZE
    link_size = LINK_SIZE
    paths = nx.all_simple_paths(Internet, asn_src, asn_dst)

    list_of_paths = []
    for path in paths:
        count += prefix_size*number_of_prefixes + link_size * len(path)
        list_of_paths.append(''.join(str(e) for e in path[1:]))
        #print path[1:]
    #print list_of_paths
    for path1 in list_of_paths:
        for path2 in list_of_paths:
            if path1 == path2 or len(path1)==1 or len(path2)==1:
                continue
            if path1 in path2:
                reduction = len(path1)
                print asn_src, "Found", path1, path2, count,reduction
                count -= prefix_size*number_of_prefixes+link_size*reduction
        #count += prefix_size + link_size * len(path)
        # (1,4) -> [1, 2, 3, 4]
        # ()
        # [1, 2, 4]
        # [1, 3, 4]
    return count

'''
The interative advertisement each prefix is advertised individually (worst case scenario).
'''

def count_mlv_interative_advertisement(Internet, asn_src, asn_dst,number_of_prefixes):
    # if asn_src != 1:
    #     return 0
    count = 0
    prefix_size = PREFIX_SIZE
    link_size = LINK_SIZE
    paths = nx.all_simple_paths(Internet, asn_src, asn_dst)

    list_of_paths = []
    for path in paths:
        count += prefix_size*number_of_prefixes + link_size * len(path)
        list_of_paths.append(''.join(str(e) for e in path[1:]))
        #print path[1:]
    #print list_of_paths
    for path1 in list_of_paths:
        for path2 in list_of_paths:
            if path1 == path2 or len(path1)==1 or len(path2)==1:
                continue
            if path1 in path2:
                reduction = len(path1)
 #               print asn_src, "Found", path1, path2, count,reduction
                count -= prefix_size+link_size*reduction
        #count += prefix_size + link_size * len(path)
        # (1,4) -> [1, 2, 3, 4]
        # ()
        # [1, 2, 4]
        # [1, 3, 4]
    return count

def count_hop_by_hop(Internet, asn_src, asn_dst,number_of_prefixes):
    count = 0
    prefix_size = PREFIX_SIZE
    link_size = LINK_SIZE
    paths = nx.all_simple_paths(Internet, asn_src, asn_dst)
    for path in paths:
        count+=prefix_size*number_of_prefixes+link_size*len(path)
    return count

def count_bgp(Internet,asn_src,number_of_prefixes):
    count = 0
    prefix_size = 4
    paths_reachable_as = list(nx.bfs_edges(Internet, asn_src))#nx.all_simple_paths(Internet, asn_src, asn_dst)
    #print paths_reachable_as
    #for path in paths_reachable_as:
    count=number_of_prefixes*prefix_size*len(paths_reachable_as)
    #print count
    return count

'''
BGP count with the proposal
'''

def count_bgp_proposal(Internet,asn_src, asn_dst,number_of_prefixes):
    count = 0
    prefix_size = PREFIX_SIZE
    link_size = LINK_SIZE
    #asns = Internet.nodes(data=False)
    paths_reachable_as = list(nx.bfs_edges(Internet, asn_src))
    try:
        if len(list(nx.node_disjoint_paths(Internet, asn_src, asn_dst)))>=2:
            print list(nx.node_disjoint_paths(Internet, asn_src, asn_dst)),"<"
            #print len(list(nx.node_disjoint_paths(Internet, asn_src, asn_dst)))-1,asn_src,asn_dst
            count += number_of_prefixes * prefix_size * (len(list(nx.node_disjoint_paths(Internet, asn_src, asn_dst)))-1)
    except:
        pass
    #print count,"<<<",prefix_size,number_of_prefixes
    count+=number_of_prefixes*prefix_size*len(paths_reachable_as)
    #print count
    return count

def compute_exchange_traffic(Internet):
    asns = Internet.nodes(data=False)
    counter_hop_by_hop = 0
    counter_mlv_interative = 0
    counter_mlv_simultaneous = 0
    counter_bgp = 0
    counter_bgp_proposal = 0
    number_of_prefixes = 1

    print "#Exchange traffic"
    print "#Number of prefixes,Hop,MVL Int.,BGP, BGP Proposal"
    for n_prefixes in range(5, 55 + 1, 5):
        for asn_src in asns:
            for asn_dst in asns:
                # if asn_src > 12 or asn_dst > 12:
                #     continue
                if asn_src == asn_dst:
                    continue
                counter_hop_by_hop += count_hop_by_hop(Internet, asn_src, asn_dst, number_of_prefixes)
                counter_mlv_interative += count_mlv_interative_advertisement(Internet, asn_src, asn_dst,
                                                                             number_of_prefixes)
                #            counter_mlv_simultaneous += count_mlv_simultaneous_advertisement(Internet, asn_src, asn_dst)
                counter_bgp += count_bgp(Internet, asn_src, number_of_prefixes)
                counter_bgp_proposal += count_bgp_proposal(Internet, asn_src, asn_dst,number_of_prefixes)
        print number_of_prefixes, counter_hop_by_hop, counter_mlv_interative, counter_bgp, counter_bgp_proposal
        number_of_prefixes = n_prefixes


        #     print "Hop:\t\t",counter_hop_by_hop
        #     print "MLV Int.:\t",counter_mlv_interative
        # #    print "MLV Simu.:\t", counter_mlv_interative
        #     print "BGP:\t\t",counter_bgp
        #     print "BGP Pro.:\t", counter_bgp_proposal

def compute_tree_number(Internet):
    asns = Internet.nodes(data=False)
    counter_hop_by_hop = 0
    counter_mlv_interative = 0
    counter_mlv_simultaneous = 0
    counter_bgp = 0
    counter_bgp_proposal = 0
    number_of_prefixes = 1

    print "#Exchange traffic"
    print "#Tree number,Hop,MVL Int.,BGP, BGP Proposal"
    for tree_number in range(1,10+1):
        for asn_src in asns:
            for asn_dst in asns:
                if asn_src > tree_number or asn_dst > tree_number:
                    continue
                if asn_src == asn_dst:
                    continue
                counter_hop_by_hop += count_hop_by_hop(Internet, asn_src, asn_dst, number_of_prefixes)
                counter_mlv_interative += count_mlv_interative_advertisement(Internet, asn_src, asn_dst,
                                                                             number_of_prefixes)
                #            counter_mlv_simultaneous += count_mlv_simultaneous_advertisement(Internet, asn_src, asn_dst)
                counter_bgp += count_bgp(Internet, asn_src, number_of_prefixes)
                counter_bgp_proposal += count_bgp_proposal(Internet, asn_src, asn_dst,number_of_prefixes)
        print tree_number, counter_hop_by_hop, counter_mlv_interative, counter_bgp, counter_bgp_proposal
        #number_of_prefixes = n_prefixes

if __name__ == '__main__':
    #list_of_customers = [as2, as3, as1]#,as4]
    #Internet = create_topo_fig_4()
    Internet = create_topo_fig_6()
    #compute_exchange_traffic(Internet)
    compute_tree_number(Internet)

