"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter

class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(player) -  when Player disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Player has disconnected"
                    to the room.
    at_pre_puppet - Just before Player re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "PlayerName has entered the game" to the room.

    """
    def at_object_creation(self):
        self.db.skills = {
            'necromancy': 0,
            'wild magic': 0,
            'wizardry': 0,
            'concentration': 0,
            'resist': 0,
            'destruction': 0,
            'healing': 0,
            'blade': 0,
            'bow': 0,
            'block': 0,
            'dodge': 0
        }
        self.db.home = 2 # The starting room, by default.
        self.db.spells = {

        }
        self.db.health = 100
        self.db.mana = 0
        self.db.resists = {
            'HEAL': -1,
            'UNHOLY': 2
        }

    def recharge_tick(self):
        '''
        To be called by a script, this
        '''
        if self.db.health < 100 + self.db.skills['resist']:
            self.db.health += 1
        if self.db.mana < self.db.skills['wizardry'] + self.db.skills['concentration']:
            self.db.mana += 1

    def damage(self, dam, spell, attacker):
        types = spell.damage_types
        resists = [self.db.resists.get(dam_type, 1) for dam_type in types]
        damage = (reduce(lambda x, y: x * y, [dam, *resists]))
        if [x for x in resists if x < 0] == resists:
            self.location.msg_contents("%s uses %s on %s, healing them for %d", attacker, spell.key, self, damage)
            self.db.health -= damage # Check if it's all healing.
        else:
            self.location.msg_contents("%s uses %s on %s, dealing %d damage", attacker, spell.key, self, damage)
            self.db.health -= damage - self.db.skills['dodge'] - self.db.skills['block']
        self.health_check()

    def health_check(self):
        if self.db.health == 0: self.location = self.db.home
