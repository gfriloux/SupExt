import sys
import requests
import logging

class cachet:
    def __init__(self, config):
        self.url = config['url']
        self.token = config['token']
        self.logger = logging.getLogger('supext')
        self.certificate = None
        self.key = None
        if config.get('certificate') and config.get('key'):
            self.certificate = config['certificate']
            self.key = config['key']

    def getHeader(self):
        return {'X-Cachet-Token': self.token}

    def getCert(self):
        if self.key and self.certificate:
            return (self.certificate, self.key)
        return None

    def getId(self, name):
        try:
            req = requests.request("GET", '{0}/components?name={1}'.format(self.url, name), headers=self.getHeader(), cert=self.getCert())
        except:
            self.logger.error("Cachet component {0} doesn't exist".format(name))
        else:
            if 'data' in req.json():
                return req.json()['data'][0]['id']

        return None

    def run(self, result, check):
        # Get name of component
        name = (check['meta']['cachet'].get('component') if check['meta'].get('cachet') else None)
        if not name:
            self.logger.warn('Check {0} doesn\'t have a cachet component, skipping'.format(check['name']))
            return None

        # Get status from result
        if result['ok'] == True:
            status = '1'
        if result['ok'] == False:
            status = '3'
        if result['ok'] == None:
            status = '4'

        payload =  {'status':"{0}".format(status),'description':"{0}".format(result['message'])}
        try:
           return requests.request("PUT", '{0}/components/{1}'.format(self.url, self.getId(name)), data=payload, headers=self.getHeader(), cert=self.getCert())
        except:
            self.logger.error("Cannot update cachet")
            return None