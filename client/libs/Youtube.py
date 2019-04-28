def requestJSON(url):
    import urllib.request
    import json

    response = urllib.request.urlopen(url)
    responseJSON = json.loads(response.read())

    return responseJSON

    

class YoutubeChannel():
    def __init__(self, name, apiKey):
        self.name = name
        self.apiKey = apiKey

        self.id = requestJSON('https://www.googleapis.com/youtube/v3/channels?key={apiKey}&forUsername={channelName}&part=id'.format(channelName=self.name, apiKey=self.apiKey))['items'][0]['id']

    def getStatistics(self):
        return requestJSON('https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channelId}&key={apiKey}'.format(channelId=self.id, apiKey=self.apiKey))

    def getSubscribersCount(self):
        return int(self.getStatistics()['items'][0]['statistics']['subscriberCount'])
