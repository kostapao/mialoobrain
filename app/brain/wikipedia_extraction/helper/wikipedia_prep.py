from brain.data_preprocessing.classes.main_class import Lecture, Keyword
from typing import List, Dict
import nltk
from nltk.cluster import KMeansClusterer
import numpy as np
import pandas as pd




def create_search_batches(lec:Lecture) -> List[List[str]]:
    number_of_similarity_clusters = lec.number_of_similarity_clusters
    final_search_list = []
    kw_pos_to_kw_map = kw_pos_to_kw_mapper(lec)
    for i in range(1,number_of_similarity_clusters+1):
        search_group = []
        for pos_kw in kw_pos_to_kw_map:
            #Uses the lecture similarity cluster created in the function create_ranked_clusters
            if kw_pos_to_kw_map[pos_kw][0].lecture_similarity_cluster == i:
                search_group.append(pos_kw)
        final_search_list.append(search_group)
    return final_search_list
        


def create_ranked_clusters(lec: Lecture) -> Lecture:
    """Create clusters, rank by lecture similarity 1 -> most similar, 5 -> Least similar"""
    kw_pos_to_kw_map = kw_pos_to_kw_mapper(lec)
    #create dataframe with columns, kw_pos and vector
    rows = []
    for kw_pos in kw_pos_to_kw_map:
        keyword = kw_pos_to_kw_map[kw_pos][0]
        bert_vector = keyword.bert_vector
        row = [kw_pos, bert_vector]
        rows.append(row)
    embeddings_df = pd.DataFrame(rows, columns=["kw_pos", "embedding"])
    number_of_similarity_clusters = 5
    lec.number_of_similarity_clusters = number_of_similarity_clusters
    output= clustering(embeddings_df,NUM_CLUSTERS = number_of_similarity_clusters)
    #For every kw.pos get cos_sim_lecture

    lecture_similarities = []
    for kw_pos in embeddings_df["kw_pos"].values:
        cos_sim_lecture = kw_pos_to_kw_map[kw_pos][0].cos_sim_lecture
        lecture_similarities.append(cos_sim_lecture)

    #Rank Clusters by average cos_sim_lecture within one cluster

    embeddings_df["cos_sim_lecture"] = lecture_similarities
    clusters_average_dict = dict(embeddings_df.groupby(['cluster'])["cos_sim_lecture"].mean())
    clusters_average_sorted = sorted(list(clusters_average_dict.values()), reverse = True)
    clusters_average_inverse_dict = {v: k for k, v in clusters_average_dict.items()}
    cluster_rank_dict = {}
    rank = 1
    for average in clusters_average_sorted:
        cluster_number_unranked = clusters_average_inverse_dict[average]
        cluster_number_ranked = rank
        rank += 1
        cluster_rank_dict[cluster_number_unranked] = cluster_number_ranked
    ranked_cluster = []
    for cluster in embeddings_df["cluster"].values:
        ranked_cluster_value = cluster_rank_dict[cluster]
        ranked_cluster.append(ranked_cluster_value)
    kw_pos_list = embeddings_df["kw_pos"].values
    map_ranked_cluster_to_pos = dict(zip(kw_pos_list,ranked_cluster))
    for kw_pos in map_ranked_cluster_to_pos:
        keyword_objects = kw_pos_to_kw_map[kw_pos]
        for kewyword_object in keyword_objects:
            kewyword_object.lecture_similarity_cluster = map_ranked_cluster_to_pos[kw_pos]
    return lec



def clustering(data,NUM_CLUSTERS = 5):
    X = np.array(data['embedding'].tolist())
    kclusterer = KMeansClusterer(
        NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance,
        repeats=25,avoid_empty_clusters=True)
    assigned_clusters = kclusterer.cluster(X, assign_clusters=True)
    data['cluster'] = pd.Series(assigned_clusters, index=data.index)
    data['centroid'] = data['cluster'].apply(lambda x: kclusterer.means()[x])
    return data


def kw_pos_to_kw_mapper(lecture: Lecture) -> Dict[str,List[Keyword]]:
    """Creat dictionary that maps every kw.pos to Kewyword object"""
    kw_pos_kw_dict = {}
    for slide in lecture.slides:
        for kw in slide.keywords:
            if kw.pos in kw_pos_kw_dict:
                current = kw_pos_kw_dict[kw.pos]
                current.append(kw)
                kw_pos_kw_dict[kw.pos] = current
            else:
                kw_pos_kw_dict[kw.pos] =[kw]
    return kw_pos_kw_dict
















# def top_n(lecture: Lecture, n: int) -> List[Keyword]:
#     all_keywords = []
#     for slide in lecture.slides:
#         for keyword in slide.keywords:
#             sum_similarity = keyword.cos_sim_slide + keyword.cos_sim_lecture + keyword.cos_sim_neighbour
#             all_keywords.append((sum_similarity, keyword.pos))
#     #Sort by sum_similarity decreasing
#     all_keywords_sorted = sorted(all_keywords, key=lambda tup: tup[0], reverse = True)
#     top_n_list = []
#     index = 0
#     while len(top_n_list) < n:
#         if all_keywords_sorted[index][1] not in top_n_list:
#             top_n_list.append(all_keywords_sorted[index][1])
#         index += 1
#     return top_n_list