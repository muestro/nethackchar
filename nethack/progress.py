from google.appengine.ext import db
from google.appengine.api import users
import datetime


class Character(db.Model):
    """Models an NetHack character progress entry."""

    creator = db.UserProperty()
    character_name = db.StringProperty()
    created_date = db.DateTimeProperty()
    server_name = db.StringProperty()
    role = db.StringProperty()
    alignment = db.StringProperty()

    # resistances/intrinsics
    cold_resistance = db.StringProperty()
    disintegration_resistance = db.StringProperty()
    fire_resistance = db.StringProperty()
    poison_resistance = db.StringProperty()
    shock_resistance = db.StringProperty()
    sleep_resistance = db.StringProperty()

    telepathy = db.StringProperty()
    speed = db.StringProperty()
    invisible = db.StringProperty()
    seeInvisible = db.StringProperty()
    stealth = db.StringProperty()

    freeAction = db.StringProperty()
    levitation = db.StringProperty()
    conflict = db.StringProperty()
    slowDigestion = db.StringProperty()

    # location(s)
    stash_location = db.StringProperty()
    store_location = db.StringProperty()
    vault_location = db.StringProperty()
    mine_location = db.StringProperty()
    sokoban_location = db.StringProperty()
    ludios_location = db.StringProperty()
    castle_location = db.StringProperty()
    quest_location = db.StringProperty()
    medusa_location = db.StringProperty()

    vladTower_location = db.StringProperty()
    fakeTower_location = db.StringProperty()

    # general
    donations = db.StringProperty()
    magic_resistance = db.StringProperty()
    magic_cancellation = db.StringProperty()
    reflection = db.StringProperty()
    boh = db.StringProperty()
    luckstone = db.StringProperty()

    notes = db.TextProperty()


def create_or_update_character(user, key, character_name, server_name='', role='', alignment='',
                               donations='0', magic_resistance='no',
                               magic_cancellation='no', reflection='no', boh='no', luckstone='no',
                               stash_location='0', store_location='0',
                               vault_location='0', mine_location='0', sokoban_location='0', ludios_location='0',
                               castle_location='0', quest_location='0', medusa_location='0',
                               vladTower_location='0', fakeTower_location='0',
                               poison_resistance='no',
                               sleep_resistance='no', cold_resistance='no', fire_resistance='no',
                               shock_resistance='no', disintegration_resistance='no',
                               telepathy='no',
                               speed='no',
                               invisible='no',
                               seeInvisible='no',
                               stealth='no',
                               freeAction='no',
                               levitation='no',
                               conflict='no',
                               slowDigestion='no',
                               notes=''):
    if user is None:
        return

    if key:
        # get the existing character from the database
        character = db.get(db.Key(key))
    else:
        character = Character()

    character.character_name = character_name
    character.server_name = server_name
    character.role = role
    character.alignment = alignment
    character.donations = donations
    character.magic_resistance = magic_resistance
    character.magic_cancellation = magic_cancellation
    character.reflection = reflection
    character.boh = boh
    character.luckstone = luckstone
    character.stash_location = stash_location
    character.store_location = store_location
    character.vault_location = vault_location
    character.mine_location = mine_location
    character.sokoban_location = sokoban_location
    character.ludios_location = ludios_location
    character.castle_location = castle_location
    character.quest_location = quest_location
    character.medusa_location = medusa_location
    character.vladTower_location = vladTower_location
    character.fakeTower_location = fakeTower_location
    character.poison_resistance = poison_resistance
    character.sleep_resistance = sleep_resistance
    character.cold_resistance = cold_resistance
    character.fire_resistance = fire_resistance
    character.shock_resistance = shock_resistance
    character.disintegration_resistance = disintegration_resistance
    character.telepathy = telepathy
    character.speed = speed
    character.invisible = invisible
    character.seeInvisible = seeInvisible
    character.stealth = stealth
    character.freeAction = freeAction
    character.levitation = levitation
    character.conflict = conflict
    character.slowDigestion = slowDigestion
    character.notes = notes[:5000]

    # todo: check to see if the threshold for characters has been reached

    character.creator = user
    character.created_date = datetime.datetime.today()
    character.put()
    return 1


def delete_character(user, key):
    if user is None or key is None:
        return

    character = db.get(db.Key(key))
    character.delete()


def get_characters(user, characterKey):
    if user is None:
        return
    if not characterKey:
        characters = db.GqlQuery('SELECT * FROM Character WHERE creator = :1 ORDER BY created_date DESC', user).fetch(
            100)
        return characters
    else:
        character = db.get(db.Key(characterKey))
        if character and character.creator == user:
            characters = [character]
            return characters
