spells = {

}

class Spell:
    '''
    Spells are attacks that deal damage of a certain type and cost mana.
    They have a certain skill requirement before they can be learned.
    '''
    skill_requirement = {
        # This can be a requirement for any skill.
    }

    damage = 0 # Base damage done.

    skill_boost = {
        # Boost per level of a particular skill.
    }
    damage_types = [] # Keys corresponding to the damage types.

    def __init__(self,
        key,
        skill_requirement = None,
        damage = 10,
        skill_boost = None,
        damage_types = None,
        lore=""):
        spells[key] = self
        self.key = key
        self.skill_requirement = skill_requirement or self.skill_requirement
        self.damage = damage
        self.skill_boost = skill_boost or self.skill_boost
        self.damage_types = damage_types or ['PHYSICAL']
        self.lore = lore
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
        caster.msg("You cast %s on %s." % (self.key, target))
        boost = sum([level * self.skill_boost.get(skill, 0) for skill, level in caster.db.skills])
        try: target.damage(self.damage + boost, damage_types)
        except AttributeError:
            caster.msg("You attack %s, but it has no effect." % target)
        for skill in self.skill_boost:
            caster.db.skills[skill] += 0.1

import yaml
for spell_name, spell in yaml.safe_load(open('skills/skills.yaml')).items():
    spell_dict = {
        'key': spell_name,
    }
    for k, v in spell.items():
        spell_dict[k] = v
    Spell(**spell_dict)
