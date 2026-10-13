"""v1.9.2: stand-alone cloud letter components, assembled from their channel letter counterparts
so they always mirror them.

  CLOUD_LETTERS_FL   = every Channel Letters - Front Lit field (columns 1-4) + the cloud fields (column 5)
  CLOUD_LETTERS_HALO = every Halo Letters field (1-4) + the Illumination fields (5) + the cloud fields (6)

Detail drawings and Design Help rules written for the letter components apply to these too
(mirror_targets adds the new IDs wherever the originals are named).
"""
C5, C6 = "COLUMN 5", "COLUMN 6"
# drawings / help rules naming a component on the left also apply to the cloud components on the right
MIRROR = {"CHANNEL_LETTERS_FL": ["CLOUD_LETTERS_FL"], "HALO_LETTERS": ["CLOUD_LETTERS_HALO"], "ILLUMINATION": ["CLOUD_LETTERS_HALO"]}

def _row11(r):
    r = tuple(r)
    return r + ("",) * (11 - len(r))

def build(F, registry, illumination_defaults=None):
    """Return (registry rows, {component_id: fields}) for the two cloud letter components."""
    cloud = lambda col: [(col,) + _row11(r)[1:] for r in F["CLOUD"]]                  # cloud fields in their own column
    illum = []
    for r in F["ILLUMINATION"]:                                                       # halo: lighting in its own column
        r = list(_row11(r)); r[0] = C5
        if illumination_defaults and r[1] in illumination_defaults: r[4] = illumination_defaults[r[1]]
        illum.append(tuple(r))
    fields = {
        "CLOUD_LETTERS_FL": [_row11(r) for r in F["CHANNEL_LETTERS_FL"]] + cloud(C5),
        "CLOUD_LETTERS_HALO": [_row11(r) for r in F["HALO_LETTERS"]] + illum + cloud(C6),
    }
    reg = [
        ("CLOUD_LETTERS_FL", "Cloud Letters - Front Lit", "Yes", "Yes",
         "Front lit channel letters on a cloud: every front lit letter option plus the cloud (size, depth, material, color, lighting)."),
        ("CLOUD_LETTERS_HALO", "Cloud Letters - Halo Lit", "Yes", "Yes",
         "Halo lit channel letters on a cloud: every halo letter and illumination option plus the cloud."),
    ]
    return reg, fields

def _mirror_ids(text, sep):
    parts = str(text or "").split(sep)
    have = [p.strip() for p in parts]
    add = []
    for p in have:
        for m in MIRROR.get(p, []):
            if m not in have and m not in add: add.append(m)
    return sep.join(parts + add) if add else text

def mirror_comps(comps):
    """'CHANNEL_LETTERS_FL,HALO_LETTERS' -> '...,CLOUD_LETTERS_FL,CLOUD_LETTERS_HALO'"""
    return _mirror_ids(comps, ",") if str(comps or "").strip() else comps

def mirror_rule(rule):
    """COMPONENT=CHANNEL_LETTERS_FL|ILLUMINATION -> COMPONENT=CHANNEL_LETTERS_FL|ILLUMINATION|CLOUD_LETTERS_FL"""
    import re
    return re.sub(r"COMPONENT=([A-Z0-9_|]+)", lambda m: "COMPONENT=" + _mirror_ids(m.group(1), "|"), str(rule or "")) if rule else rule
