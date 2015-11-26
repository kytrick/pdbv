import json
# from model import connect_to_db,
from model import PeerParticipants, MgmtPublics, PeerParticipantsPublics
# should I also import BaseTable?
import networkx as nx
from networkx.readwrite import json_graph


def flare_tree_as_json_for_asn(asn):
    """ Returned a json representation of an AS tree """

    results = MgmtPublics.query.join(
        PeerParticipantsPublics).filter(
        PeerParticipantsPublics.local_asn == asn).all()

    H = nx.DiGraph()   # initialize the tree
    H.add_node(asn)  # this is the root

    for result in results:  # each result here is an IX
        H.add_nodes_from([
            result.region_continent, result.country, result.city, result.name])

        H.add_edge(asn, result.region_continent)
        H.add_edge(result.region_continent, result.country)
        H.add_edge(result.country, result.city)
        H.add_edge(result.city, result.name)

    # return json.dumps(json_graph.tree_data(H, root=asn))
    return H


def generate_complete_graph():
    results = PeerParticipantsPublics.query.all()

    H = nx.Graph()
    for result in results:
        H.add_nodes_from(["participant_id:" + str(result.participant_id), 
                          "public_id:" + str(result.public_id)])

        H.add_edge("participant_id:" + str(result.participant_id),
                   "public_id:" + str(result.public_id))

    return H


def tree_data_json(asn):
    H = flare_tree_as_json_for_asn(asn)
    return json.dumps(json_graph.tree_data(H, root=asn))


def adjacency_data_json():
    H = generate_complete_graph()
    return json.dumps(json_graph.adjacency_data(H))


def sunburst_ready_json(asn):
    H = flare_tree_as_json_for_asn(asn)
    return json.dumps(json_graph.tree_data(H, root=asn))


def tree_ready_json(asn):
    H = flare_tree_as_json_for_asn(asn)
    return json.dumps(json_graph.adjacency_data(H))


def live_search(query):
    rows = PeerParticipants.query.filter(
        PeerParticipants.name.like('%%%s%%' % query)).filter(
            PeerParticipants.asn > 0).order_by(
                PeerParticipants.info_traffic.desc()).all()
    output = [row.serialize(['asn', 'name']) for row in rows]
    return json.dumps(output)
