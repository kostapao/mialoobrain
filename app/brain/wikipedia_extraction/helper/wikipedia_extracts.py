from typing import Dict


from typing import List,Dict
import asyncio
import aiohttp
#Necessary because "Cannot run the event loop whole another loop is running"
import nest_asyncio
nest_asyncio.apply()


def get_wikipedia_extracts(wiki_titles: List) -> Dict[str,str]:

    results= []
    def get_tasks(session):
        tasks = []
        for title in wiki_titles:
                URL = "https://en.wikipedia.org/w/api.php"
                PARAMS = {
                    "action": "query",
                    "format": "json",
                    "prop":"extracts",
                    #True must be given as string
                    "exintro": "True",
                    "explaintext": "True",
                    "plnamespace": 0,
                    "titles":title

                }
        
                tasks.append(asyncio.create_task(session.get(url=URL, params=PARAMS, ssl=False)))
        return tasks

    async def get_extracts():
        async with aiohttp.ClientSession() as session:
                tasks = get_tasks(session)
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    DATA = await response.json()
                    results.append(DATA["query"]["pages"]) #["search"][0]["title"]


    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_extracts())
    loop.close()

    all_extracts = []
    for page_id in results:
        extract = list(page_id.values())[0]["extract"]
        all_extracts.append(extract)

    wiki_titles_extracts_zipped = zip(wiki_titles, all_extracts)
    final_extract_dict = {}
    for wiki_title, extract in wiki_titles_extracts_zipped:
        final_extract_dict[wiki_title] = extract
    
    return final_extract_dict



# example_titles = ['Mila (research institute)','Mixed reality','Mlpack']


# print(get_wikipedia_extracts(example_titles))







