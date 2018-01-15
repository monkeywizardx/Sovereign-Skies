class Spell:
    '''
    Spells are attacks that deal damage of a certain type and cost mana.
    They have a certain skill requirement before they can be learned.
    '''
    self.skill_requirement = {
        # This can be a requirement for any skill.
    }

    self.damage = 0 # Base damage done.

    self.skill_boost = {
        # Boost per level of a particular skill.
    }
    self.damage_types = [] # Keys corresponding to the damage types.

    def __init__(self, key, skill_requirement, damage, skill_boost, damage_types, lore=""):
        self.key = key
        self.skill_requirement = skill_requirement
        self.damage = damage
        self.skill_boost = skill_boost
        self.damage_types = damage_types

    def description(self):
        return '''
        Skill: {}
        Base Damage: {}
        Relevant Skills: {}
        Types: {}
        Lore: {}
        '''.format(self.key,
                   self.damage,
                   str(tuple(x[0] for x in sorted(self.skill_boost.items(), lambda t: t[1]))).lstrip('(').rstrip(')'),
                   str(self.damage_types).lstrip('[').rstrip(']'),
                   self.lore)
    def cast(self, caster, target):
        '''
        Calculates dealt damage and then calls the targets damage.
        '''
        caster.msg("You cast %s on %s." % self.key, target)
        boost = sum([level * self.skill_boost.get(skill, 0) for skill, level in caster.db.skills])
        target.db.damage(self.damage + boost, damage_types)
