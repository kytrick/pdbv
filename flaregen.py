import json
# from model import connect_to_db,
from model import PeerParticipants, MgmtPublics, PeerParticipantsPublics
import networkx as nx
from networkx.readwrite import json_graph


def flare_tree_as_json_for_asn(asn):
    """ Returned a json representation of an AS tree """
    # continent_count = Counter()
    # country_count = Counter()
    # city_count = Counter()
    # exchanges = defaultdict(lambda: defaultdict(lambda: defaultdict()))
    # results = MgmtPublics.query.filter(PeerParticipants.asn == asn).all()
    results = MgmtPublics.query.join(
        PeerParticipantsPublics).filter(
        PeerParticipantsPublics.local_asn == asn).all()

    H = nx.DiGraph()   # initialize the tree
    H.add_node("asn")  # this is the root

    for result in results:  # each result here is an IX
        H.add_nodes_from([
            result.region_continent, result.country, result.city, result.name])

        H.add_edge("asn", result.region_continent)
        H.add_edge(result.region_continent, result.country)
        H.add_edge(result.country, result.city)
        H.add_edge(result.city, result.name)

    # return json.dumps(json_graph.tree_data(H, root=asn))
    return H

def tree_data_json(asn):
    H = flare_tree_as_json_for_asn(asn)
    return json.dumps(json_graph.tree_data(H, root=asn))

def adjacency_data_json(asn):
    H = flare_tree_as_json_for_asn(asn)
    return json.dumps(json_graph.adjacency_data(H))

def otherthing():
    pass