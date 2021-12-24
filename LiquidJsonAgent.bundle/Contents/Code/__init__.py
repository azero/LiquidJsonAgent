import os, json
from base64 import b64encode

def wl(msg):
    Log(msg)

class LiquidJsonAgent(Agent.Movies):
    name = "Liquid JSON Agent"
    
    languages = [Locale.Language.NoLanguage]

    primary_provider = True
    persist_stored_files = False

    contributes_to = ['com.plexapp.agents.none']
    accepts_from = ['com.plexapp.agents.localmedia']

    def search(self, results, media, lang):
        part = media.items[0].parts[0]
        path = os.path.join(os.path.dirname(part.file), 'Info.json')
        
        movieTitle = getattr(media, "name", getattr(media, "title", "Unknown"))
        
        if os.path.exists(path):
            wl("Found JSON File.")
            mid = b64encode(movieTitle).replace("/", "_")
            results.Append(MetadataSearchResult(id=mid, name=movieTitle, year=2021, lang=lang, score=100))
        else:
            wl("Couldnt find json at [" + str(path) + "]")


    def update(self, metadata, media, lang, force):
        part = media.items[0].parts[0]
        path = os.path.join(os.path.dirname(part.file), 'Info.json')
        
        if os.path.exists(path):
            info = json.loads(Core.storage.load(path))
            wl(info)

            try:
                metadata.title = info['title']
                wl("Set Tile")
            except:
                wl("Couldnt Set Title")
                pass

            try:
                metadata.content_rating = info['content_rating']
            except:
                pass

            try:
                metadata.studio = info['studio']
            except:
                pass

            metadata.directors.clear()
            try:
                for d in info['directors']:
                    metadata.directors.add(d)
            except:
                pass

            metadata.genres.clear()
            try:
                for g in info['genres']:
                    metadata.genres.add(g)
            except:
                pass

            metadata.roles.clear()

            metadata.collections.clear()
            try:
                for c in info['collections']:
                    metadata.collections.add(c)
            except:
                pass
        else:
            wl("No info file found.")
