from brain.data_preprocessing.classes.main_class import Lecture, Keyword, WikiSearch, WikiArticle,Resource, Node, Edge

#example_data = [['3_Clustering', 'Cluster analysis'], ['Cluster', 'Cluster analysis']]


def get_nodes_edges(lecture: Lecture):
    #Create map from wiki_title to keyword
    edges_list_wiki_titles = lecture.edges_list_wiki_titles
    all_wiki_titles = []
    for edge in edges_list_wiki_titles:
        for wiki_title in edge:
            all_wiki_titles.append(wiki_title)
    all_wiki_titles_unique = list(set(all_wiki_titles))
    #Create Nodes
    nodes = []
    counter = 0
    for wiki_title in all_wiki_titles_unique:
        if wiki_title is not None:
            counter += 1
            id = str(counter)
            label = wiki_title
            resource_label = "Wikipedia"
            wiki_title_spaces_replaced = wiki_title.replace(" ","_")
            resource_url = "https://en.wikipedia.org/wiki/" + wiki_title_spaces_replaced
            resource = Resource(resource_label,resource_url)
            node = Node(id,label,resource)
            nodes.append(node)

    #Create wiki title to node map for edges
    wiki_title_node_dict = {}
    for node in nodes:
        wiki_title_node_dict[node.label] = node

    edges = []
    for connection in edges_list_wiki_titles:
        edge = Edge(wiki_title_node_dict[connection[0]],wiki_title_node_dict[connection[1]])
        edges.append(edge)

    nodes_json_list = []
    for node in nodes:
        node_element = {"id": node.id, "label": node.label, "resources": [{"label": node.resource.label, "url": node.resource.url}]}
        nodes_json_list.append(node_element)
    # node_json = {"nodes":nodes_json_list}
    edges_json_list = []
    for edge in edges:
        edge_element = {"id": edge.id, "nodeSource": edge.nodeSource.id, "nodeTarget": edge.nodeTarget.id}
        edges_json_list.append(edge_element)

    complete_response = {"nodes": nodes_json_list, "edges": edges_json_list}

    return complete_response

