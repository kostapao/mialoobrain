from brain.data_preprocessing.classes.main_class import Lecture
import pandas as pd


def connect(lecture: Lecture) -> pd.DataFrame:
    all_connections = []
    for slide in lecture.slides:
        title_keywords = []
        for kw in slide.keywords:
            if kw.is_in_title:
                title_keywords.append(kw.wiki_title)
                all_connections.append(sorted([lecture.name_pure,kw.wiki_title]))
        if len(title_keywords) > 1:
            all_combs =  [sorted([el1, el2]) for el1 in title_keywords for el2 in title_keywords if el1!=el2]
            for comb in all_combs:
                all_connections.append(comb)
        for kw in slide.keywords:
            if kw.is_in_title is False:
                for title_keyword in title_keywords:
                    all_connections.append(sorted([title_keyword,kw.wiki_title]))
        for connection in all_connections:
            if connection[0] == connection[1]:
                all_connections.remove(connection)
        all_connections_deduped = []
        for conn in all_connections:
            if conn not in all_connections_deduped:
                all_connections_deduped.append(conn)
        
    return all_connections_deduped


        
        


        #Connect title to filename

        #Connect title to title

        #Connect title to below title