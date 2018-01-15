import operator as op

def skill_function(operator):
    def lookup(accessor, accessing, *args, **kwargs):
        if len(args) == 2:
            if accessor.db.skills:
                return operator(accessor.db.skills[args[0]], args[1])
        return False
    return lookup

def bool_comp_function(comp_func):
    def composed(*in_funcs):
        def composed(x, y):
            return reduce(lambda *args: comp_func(*args), [f(x, y) for f in in_funcs])
        return composed
    return composed

or_functions = bool_comp_function(op.or_)
skill_gt = skill_function(op.gt)
skill_gte = skill_function(or_functions(op.gt, op.eq))
skill_eq = skill_function(op.eq)
skill_lte = skill_function(or_functions(op.lt, op.eq))
skill_lt = skill_function(op.lt)
