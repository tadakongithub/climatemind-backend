import json
import pickle
import argparse
import networkx as nx
import pandas as pd

from owlready2 import *


from knowledge_graph.ontology_processing_utils import give_alias, save_test_ontology_to_json, save_graph_to_pickle, get_valid_test_ont, get_non_test_ont
import os


# Set a lower JVM memory limit
owlready2.reasoning.JAVA_MEMORY = 500


def add_edges_to_graph(edges, G):
    """
    Adds edges to networkx object

    Parameters
    ----------
    edges: List of graph edges (object, subject, predicate triples)
    G: A networkx Graph
    """
    for src, tgt, kind in edges:
        G.add_edge(src, tgt, type=kind, properties=None)

def listify(collection, onto):
    """just capturing a repeated operation"""
    return [str(thing.label[0]) 
            for thing in collection
            if thing in onto.classes()]

def add_ontology_data_to_graph_nodes(G, onto):
    """Find the equivalent nodes in the ontology and load in relevant data
    including the classes they belong to.

    Parameters
    ----------
    G: A networkx Graph
    onto: owlready2 ontology object
    """
    # This shouldn't need to be repeated for each node. 
    # Moved out of loop.
    cm_class = onto.search_one(label="climate mind")
    superclasses = list(cm_class.subclasses())
    
    for node in list(G.nodes):
        ontology_node = onto.search_one(label=node)
        class_objects = onto.get_parents_of(ontology_node)
        annot_properties = [
            thing.label[0].replace(":", "_")
            for thing in list(onto.annotation_properties())
        ]

        attributes_dict = {}
        attributes_dict["label"] = str(ontology_node.label[0])
        attributes_dict["iri"] = str(ontology_node)
        attributes_dict["comment"] = str(ontology_node.comment)
        attributes_dict["direct classes"] = listify(class_objects, onto) 

        all_classes = []
        for parent in class_objects:
            if parent in onto.classes():
                all_classes.extend(parent.ancestors())

        list_classes = listify(all_classes, onto)
        list_classes = list(set(list_classes))
        if "climate mind" in list_classes:
            list_classes.remove("climate mind")
        attributes_dict["all classes"] = list_classes

        # for each class in the classes associated with the node, list that class in the appropriate super_class in the attributes_dict and all of the ancestor classes of that class
        for node_class in class_objects:
            for super_class in superclasses:
                if node_class in super_class.descendants():
                    to_add = listify(node_class.ancestors(), onto)
                    if "climate mind" in to_add:
                        to_add.remove("climate mind")
                    if super_class in attributes_dict.keys():
                        attributes_dict[str(super_class.label[0])] = list(
                            set(attributes_dict[super_class]) | set(to_add)
                        )
                    else:
                        attributes_dict[str(super_class.label[0])] = to_add
        # if there are multiple of the nested classes associated with the node in the ontology, code ensures it doesn't overwrite the other class.

        G.add_nodes_from([(node, attributes_dict)])

        # the if statement is needed to avoid the Restriction objects
        # still don't know why Restriction Objects are in our ontology!
        # technically each class could have multiple labels, but this way just pulling 1st label

        annot_properties_dict = {}
        for prop in annot_properties:
            annot_properties_dict[prop] = list(eval("ontology_node." + prop))
        G.add_nodes_from([node], properties=annot_properties_dict)


def set_edge_properties(G):
    """Add edge annotation properties that exist on both nodes of an edge
    and create a list of properties to remove from the nodes.
    (Properties that exist on both nodes of an edge are only for the edge)

    Parameters
    ----------
    G: A networkx Graph
    """
    to_remove = {}
    for edge in list(G.edges):
        node_a = edge[0]
        node_b = edge[1]
        for prop in G.nodes[node_a]["properties"].keys():
            intersection = set(G.nodes[node_a]["properties"][prop]) & set(
                G.nodes[node_b]["properties"][prop]
            )
            # add intersection to edge property dictionary
            if intersection:
                G.add_edge(node_a, node_b, properties={prop: list(intersection)})
                if (node_a, prop) in to_remove.keys():
                    to_remove[(node_a, prop)] = to_remove[(node_a, prop)] | intersection
                else:
                    to_remove[(node_a, prop)] = intersection
                if (node_b, prop) in to_remove.keys():
                    to_remove[(node_b, prop)] = to_remove[(node_b, prop)] | intersection
                else:
                    to_remove[(node_b, prop)] = intersection
    return list(to_remove)

def remove_edge_properties_from_nodes(G, to_remove):
    """Remove properties from Networkx nodes that occur on both nodes of an edge
    (because it marks that property is only for the edge).

    Parameters
    ----------
    G: A networkx graph
    to_remove: A dictionary of nodes and properties
    """
    for item in to_remove:
        node = item[0]
        prop = item[1]
        to_delete = item
        G.nodes[node]["properties"][prop] = [
            node
            for node in list(G.nodes[node]["properties"][prop])
            if node not in list(to_delete)
        ]
        # DM: uh... won't `node not in list(to_delete)` always evaluate to false?

def remove_non_test_nodes(G, node, valid_test_ont, not_test_ont):
    if node in G.nodes:
        is_test_ont = False
        for c in G.nodes[node]["direct classes"]:
            if c in valid_test_ont:
                is_test_ont = True
            if c in not_test_ont:
                is_test_ont = False
                break
        if not is_test_ont:
            G.remove_node(node)
        else:
            is_test_ont = False

def get_test_ontology(G, valid_test_ont, not_test_ont):
    for edge in list(G.edges):
        node_a = edge[0]
        node_b = edge[1]
        remove_non_test_nodes(G, node_a, valid_test_ont, not_test_ont)
        remove_non_test_nodes(G, node_b, valid_test_ont, not_test_ont)

def makeGraph(onto_path, edge_path, output_folder_path):
    """
    Main function to make networkx graph object from reference ontology and edge list.

    input: args = args from the argument parser for the function
                    (refOntologyPath, refEdgeListPath)
    output: saves a python pickle file of the networkx object, and yaml and json of the networkx object
    """

    # Load ontology and format object properties and annotation properties into Python readable names
    onto = get_ontology(onto_path).load()
    obj_properties = list(onto.object_properties())
    annot_properties = list(onto.annotation_properties())
    [give_alias(x) for x in obj_properties]
    [give_alias(x) for x in annot_properties]

    # run automated reasoning.
    with onto:
        sync_reasoner()

    # print(list(default_world.inconsistent_classes()))

    # Read in the triples data
    ## DMARX - csv via make_network.outputEdges()
    #          via node_network.result
    # ... If we've already processed the ontology through the Network object,
    # why do we need to reload it here? 
    # Can we move add_ontology_data_to_graph_nodes to network_class?
    df_edges = pd.read_csv(edge_path)

    G = nx.DiGraph()  # There should not be duplicate edges that go the same direction.
    # If so, need to throw an error.
    add_edges_to_graph(df_edges.values, G)
    
    
    add_ontology_data_to_graph_nodes(G, onto)
    to_remove = set_edge_properties(G)
    remove_edge_properties_from_nodes(G, to_remove)

    save_graph_to_pickle(G, output_folder_path)

    valid_test_ont = get_valid_test_ont()
    not_test_ont = get_non_test_ont()
    get_test_ontology(G, valid_test_ont, not_test_ont)

    save_test_ontology_to_json(G, output_folder_path)


def main(args):
    """
    Main function to make networkx graph object from reference ontology and edge list.

    input: args = args from the argument parser for the function
    (refOntologyPath, refEdgeListPath)
    output: saves a python pickle file of the networkx object, and yaml and json of the networkx object

    example: python3 make_graph.py "./climate_mind_ontology20200721.owl" "output.csv"
    """

    # set arguments
    onto_path = args.refOntologyPath
    edge_path = args.refEdgeListPath

    # run makeGraph function
    makeGraph(onto_path, edge_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="get networkx graph object from ontology after running make_network.py"
    )
    parser.add_argument(
        "refOntologyPath", type=str, help="path to reference OWL2 ontology"
    )
    parser.add_argument(
        "refEdgeListPath",
        type=str,
        help="path for csv file of result edges (list of object,subject,predicate triples)",
    )

    args = parser.parse_args()
    main(args)
