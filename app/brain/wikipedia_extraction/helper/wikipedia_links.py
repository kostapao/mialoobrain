from typing import Dict


from typing import List,Dict
import asyncio
import aiohttp
#Necessary because "Cannot run the event loop whole another loop is running"
import nest_asyncio
nest_asyncio.apply()


def get_wikipedia_links(wiki_titles: List) -> Dict[str,List[str]]:

    results= []
    def get_tasks(session):
        tasks = []
        for title in wiki_titles:
                URL = "https://en.wikipedia.org/w/api.php"
                PARAMS = {
                    "action": "query",
                    "format": "json",
                    "prop":"links",
                    "plnamespace": 0,
                    "pllimit": "max",
                    "titles":title

                }
        
                tasks.append(asyncio.create_task(session.get(url=URL, params=PARAMS, ssl=False)))
        return tasks

    async def get_links():
        async with aiohttp.ClientSession() as session:
                tasks = get_tasks(session)
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    DATA = await response.json()
                    results.append(DATA["query"]["pages"]) #["search"][0]["title"]


    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_links())
    loop.close()

    all_links = []
    for page_id in results:
        links = list(page_id.values())[0]["links"]
        page_id_links = []
        for link in links:
            page_id_links.append(link["title"])
        all_links.append(page_id_links)
    
    wiki_titles_links_zipped = zip(wiki_titles,all_links)
    final_link_dict = {}
    for wiki_title, links in wiki_titles_links_zipped:
        final_link_dict[wiki_title] = links
    return final_link_dict


# example_titles = ["Hamming distance"]


# print(get_wikipedia_links(example_titles))

