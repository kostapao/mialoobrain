
from typing import List,Dict
import asyncio
import aiohttp
#Necessary because "Cannot run the event loop whole another loop is running"
import nest_asyncio
nest_asyncio.apply()


def get_wikipedia_search_results(searchterms: List, number_of_searchresults) -> List[Dict[str,List]]:

    results= []
    def get_tasks(session):
        tasks = []
        for i in searchterms:
                URL = "https://en.wikipedia.org/w/api.php"
                SEARCHPAGE = i
                PARAMS = {
                    "action": "query",
                    "format": "json",
                    "list": "search",
                    #TODO: How to handle Section Title?
                    "srprop":"sectiontitle",
                    #TODO: Examine possibilities
                    "srsort":"relevance",
                    "srlimit": number_of_searchresults,
                    "srsearch": SEARCHPAGE
                }
                tasks.append(asyncio.create_task(session.get(url=URL, params=PARAMS, ssl=False)))
        return tasks

    #Get Page Title

    async def get_titles():
        async with aiohttp.ClientSession() as session:
                tasks = get_tasks(session)
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    DATA = await response.json()
                    try:
                        results.append(DATA["query"]["search"]) #["search"][0]["title"]
                    except IndexError:
                        results.append("not found")


    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_titles())
    loop.close()

    zipped_keywords_results = zip(searchterms,results)
    #keywords_search_results = []
    kw_wiki_search_dict = {}
    for keyword, search_result_kw in zipped_keywords_results:
        search_results_titles = []
        for wiki_result in search_result_kw:
            search_results_titles.append(wiki_result["title"])
        kw_wiki_search_dict[keyword] = search_results_titles
        #keywords_search_results.append(kw_wiki_search_dict)

    return kw_wiki_search_dict