import webapp2
import os
import jinja2
import time
from google.appengine.api import users
from nethack import progress

jinja_environment = jinja2.Environment(autoescape=True,
                                       loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__))))


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())


class ProgressHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user is None:
            return self.redirect(users.create_login_url(self.request.uri))

        characterKey = self.request.get('charKey')
        template_values = {
            'user': user,
            'characters': progress.get_characters(user, characterKey)
        }
        if characterKey:
            template_values['characterSelected'] = 'true'

        template = jinja_environment.get_template('progress.html')
        self.response.out.write(template.render(template_values))


class SaveProgressHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        key = self.request.get('key')

        if user is None:
            return self.redirect(users.create_login_url(self.request.uri))

        if key and not progress.is_character_owner(user, key):
            return self.abort(403)

        # verify input

        # save to db
        progress.create_or_update_character(user, self.request.get('key'), self.request.get('charName'),
                                            self.request.get('serverName'), self.request.get('role'),
                                            self.request.get('alignment'),
                                            self.request.get('donations'), self.request.get('magicResistance'),
                                            self.request.get('magicCancellation'), self.request.get('reflection'),
                                            self.request.get('boh'), self.request.get('luckstone'),
                                            self.request.get('stashLocations'),
                                            self.request.get('storeLocations'), self.request.get('vaultLocations'),
                                            self.request.get('mineLocation'), self.request.get('sokobanLocation'),
                                            self.request.get('fortLudiosLocation'),
                                            self.request.get('castleLocation'), self.request.get('questLocation'),
                                            self.request.get('medusaLocation'), self.request.get('vladTowerLocation'),
                                            self.request.get('fakeTowerLocation'),
                                            self.request.get('poisonResistance'),
                                            self.request.get('sleepResistance'), self.request.get('coldResistance'),
                                            self.request.get('fireResistance'),
                                            self.request.get('shockResistance'),
                                            self.request.get('disintegrationResistance'),
                                            self.request.get('telepathy'),
                                            self.request.get('speed'),
                                            self.request.get('invisible'),
                                            self.request.get('seeInvisible'),
                                            self.request.get('stealth'),
                                            self.request.get('freeAction'),
                                            self.request.get('levitation'),
                                            self.request.get('conflict'),
                                            self.request.get('slowDigestion'),
                                            self.request.get('notes'))


class DeleteProgressHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        key = self.request.get('key')

        if user is None:
            return self.redirect(users.create_login_url(self.request.uri))

        if not key:
            return self.abort(400)

        if not progress.is_character_owner(user, key):
            return self.abort(403)

        progress.delete_character(user, key)
        time.sleep(0.2)


class CreateUserProgressHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        charName = self.request.get('charName')

        if user is None:
            return self.redirect(users.create_login_url(self.request.uri))

        if not charName:
            return self.redirect(400)

        progress.create_character(user, self.request.get('charName'))
        time.sleep(0.2)
        return self.redirect('/nethack/progress')


class NotFoundHandler(webapp2.RequestHandler):
    def get(self):
        return self.redirect('../notfound')


app = webapp2.WSGIApplication([('/', ProgressHandler),
                               ('/nethack[/]?', IndexHandler),
                               ('/nethack/progress', ProgressHandler),
                               ('/nethack/progress/save', SaveProgressHandler),
                               ('/nethack/progress/delete', DeleteProgressHandler),
                               ('/nethack/progress/createUser', CreateUserProgressHandler),
                               ('/nethack.*', NotFoundHandler), ],
                              debug=True)

