import json

import pytumblr
from alchemyapi import AlchemyAPI


class AlchemyPost:

    def __init__(self, post_tumblr, post_id, consumer_key, consumer_secret, oauth_token, oauth_secret):
        self.post_tumblr = post_tumblr
        self.post_id = post_id
        self._init_tumblr(consumer_key, consumer_secret, oauth_token, oauth_secret)
        self._init_alchemy()

    def _init_tumblr(self, consumer_key, consumer_secret, oauth_token, oauth_secret):
        self._client = pytumblr.TumblrRestClient(consumer_key, consumer_secret, oauth_token, oauth_secret)    

    def _init_alchemy(self):
        self.alchemyapi = AlchemyAPI()
        self.content = {}

    def analyze_post(self):
        self.post = self._get_content_post()
        self._alchemy_entities()
        self._alchemy_keywords()
        self._alchemy_concepts()
        self._alchemy_sentiment()
        self._alchemy_relations()
        self._alchemy_category()
        self._alchemy_feeds()
        self._alchemy_taxonomy()

    def print_content(self):
        print(json.dumps(self.content, indent=4))

    def _get_content_post(self):
        print "*",
        infos = self._get_infos_post() 
        self.title = ''
        self.tags = []
        if 'tags' in infos:
            self.tags = infos['tags']
        
        if infos['type'] == 'text':
            return self._get_content_text(infos)
        if infos['type'] == 'quote':
            return self._get_content_quote(infos)
        return ''

    def _get_infos_post(self):
         infos = self._client.posts(self.post_tumblr, id=self.post_id)
         if 'posts' in infos and len(infos['posts'])>0:
            return infos['posts'][0]
         return {}

    def _get_content_text(self, infos):
        content = "<h1>" + str(infos['title']) + "</h1>"
        content += " <br>" + str(infos['body'])
        content += " <br>" + " ".join(infos['tags'])
        return content

    def _get_content_quote(self, infos):
        content = str(infos['text'])
        content += " <br>" + str(infos['source'])
        content += " <br>" + " ".join(infos['tags'])
        return content

    def _alchemy_entities(self):
        print ".",
        response = self.alchemyapi.entities('html', self.post)
        if response['status'] != 'OK':
            return False
        self.content['entities'] = response['entities']
        return True

    def _alchemy_keywords(self):
        print ".",
        response = self.alchemyapi.keywords('html', self.post)
        if response['status'] != 'OK':
            return False
        self.content['keywords'] = response['keywords']
        return True

    def _alchemy_concepts(self):
        print ".",
        response = self.alchemyapi.concepts('html', self.post)
        if response['status'] != 'OK':
            return False
        self.content['concepts'] = response['concepts']
        return True

    def _alchemy_sentiment(self):
        print ".",
        response = self.alchemyapi.sentiment('html', self.post)
        if response['status'] != 'OK':
            return False
        self.content['sentiment'] = response['docSentiment']
        return True

    def _alchemy_relations(self):
        print ".",
        response = self.alchemyapi.relations('html', self.post)
        if response['status'] != 'OK':
            return False
        self.content['relations'] = response['relations'] 
        return True

    def _alchemy_category(self):
        print ".",
        response = self.alchemyapi.category('html', self.post)
        if response['status'] != 'OK':
            return False
        self.content['category'] = response['category'] 
        self.content['score'] = response['score'] 
        return True

    def _alchemy_feeds(self):
        print ".",
        response = self.alchemyapi.feeds('html', self.post)
        if response['status'] != 'OK':
            return False
        self.content['feeds'] = response['feeds'] 
        return True

    def _alchemy_taxonomy(self):
        print ".",
        response = self.alchemyapi.taxonomy('html', self.post)
        if response['status'] != 'OK':
            return False
        self.content['taxonomy'] = response['taxonomy'] 
        return True
