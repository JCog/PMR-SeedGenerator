


class Mario:
    def __init__(self, **kwargs):
        self.boots = kwargs.get("boots", 0)
        self.hammer = kwargs.get("hammer", -1)
        self.items = kwargs.get("items", [])
        self.partners = kwargs.get("partners", [])
        self.favors = kwargs.get("favors", []) # https://www.mariowiki.com/Koopa_Koot%27s_favors
        self.flags = kwargs.get("flags", [])
        self.starspirits = kwargs.get("starspirits", 0)

def add_to_inventory(item_object):
    global mario
    # Overload: Single item -> Add item
    if type(item_object) is str:
        is_new_pseudoitem = False
    
        if (item_object.startswith("GF") or item_object.startswith("MF") or item_object.startswith("RF")) and item_object not in mario.flags:
            mario.flags.append(item_object)
            is_new_pseudoitem = True
        elif item_object.startswith("PARTNERS") and item_object not in mario.partners:
            mario.partners.append(item_object)
            is_new_pseudoitem = True
        elif item_object.startswith("FAVOR") and item_object not in mario.favors:
            mario.favors.append(item_object)
            is_new_pseudoitem = True
        elif item_object.startswith("EQUIPMENT"):
            if item_object == "EQUIPMENT_Boots_Progressive":
                mario.boots = mario.boots + 1 if mario.boots < 2 else mario.boots
            if item_object == "EQUIPMENT_Hammer_Progressive":
                mario.hammer = mario.hammer + 1 if mario.hammer < 2 else mario.hammer
        elif item_object == "STARSPIRIT":
            mario.starspirits = mario.starspirits + 1 if mario.starspirits < 7 else mario.starspirits
            is_new_pseudoitem = True
        else:
            mario.items.append(item_object)

        return is_new_pseudoitem
    # Overload: List of items -> Call function per item
    if type(item_object) is list:
        has_new_pseudoitem = False
        for item in item_object:
            is_new_pseudoitem = add_to_inventory(item)
            if is_new_pseudoitem:
                has_new_pseudoitem = True
        return has_new_pseudoitem
    else:
        raise TypeError('item_object argument is not of type str or list', type(item_object), item_object)

def flip_panels():
    global mario
    return mario.hammer == 2 or mario.boots >= 1

def shake_trees():
    global mario
    return mario.hammer >= 0 or "PARTNER_Bombette" in mario.partners

def item(item_str):
    global mario
    return item_str in mario.items

def partner(partner_str):
    global mario
    return partner_str in mario.partners

def parakarry_3_letters():
    global mario
    count = 0
    for item_str in mario.items:
        if item_str.startswith("Letter"):
            count += 1
            if count >= 3:
                return True
    return False

def require(**kwargs):
    def func(kwargs=kwargs):
        global mario
        # Sanity-checking kwargs
        for key in kwargs.keys():
            if key not in ["partner","item","hammer","boots","favor","flag","starspirits"]:
                raise KeyError('Requirement kwargs is not valid', key)

        # Partners
        partners = kwargs.get("partner")
        if type(partners) is not list:
            partners = [partners]
        for partner in partners:
            if partner in mario.partners:
                return True
        # Items
        if item := kwargs.get("item"):
            if item in mario.items:
                return True
        # Hammer
        hammer = kwargs.get("hammer")
        if hammer is not None and mario.hammer >= hammer:
            return True
        # Boots
        if boots := kwargs.get("boots"):
            if mario.boots >= boots:
                return True
        # Koopa Koot Favors
        if favor := kwargs.get("favor"):
            if favor in mario.favors:
                return True
        # Flags
        if flag := kwargs.get("flag"):
            if flag in mario.flags:
                return True
        # Star Spirits
        if starspirits := kwargs.get("starspirits"):
            if mario.starspirits >= starspirits:
                return True
                
        return False
    return func


# Example
mario = Mario()
"""
mario.partners.append("Kooper")
mario.boots = 0

reqs = [require(partner="Kooper", boots=2)]
if all([r() for r in reqs]):
    print("Accessible")
else:
    print("Not accessible")
"""