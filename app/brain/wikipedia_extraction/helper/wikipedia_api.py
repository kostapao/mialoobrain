import asyncio
import aiohttp
#Necessary because "Cannot run the event loop whole another loop is running"
import nest_asyncio
nest_asyncio.apply()


def get_wikipedia_titles(searchterms):

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
                        results.append(DATA["query"]["search"][0]["title"])
                    except IndexError:
                        results.append("not found")


    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_titles())
    loop.close()

    return results



def get_wikipedia_links(wiki_titles):
    pass

def get_wikipedia_categories(wiki_page):
    pass


def is_disambiguation_page(wiki_page):
    pass
