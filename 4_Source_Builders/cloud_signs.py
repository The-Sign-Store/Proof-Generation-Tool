"""v1.9.4: Cloud signs - a sign type of their own, separate from channel letters.

A cloud sign is a shaped, fabricated sign cabinet (front lit or halo lit). It has a quantity and
overall dimensions instead of a letter count / letter height / text, and otherwise the same face,
return, trim cap, lighting and mounting options as the matching channel letters, so the two stay
in step. A project with letters on a cloud simply selects both products.

  CLOUD_SIGN_FL    = Cloud Sign - Front Lit: QUANTITY + CLOUD SIZE, then every front lit letter
                     option except the letter-only fields
  CLOUD_SIGN_HALO  = Cloud Sign - Halo Lit: same from the halo letters, plus the Illumination fields
"""
import re
C1, C5 = "COLUMN 1", "COLUMN 5"
LETTER_ONLY = {"QUANTITY", "LETTER HEIGHT", "TEXT"}          # replaced by QUANTITY + CLOUD SIZE
RENAME = {"LETTER TYPE": "LIGHTING TYPE"}                     # halo: Reverse Lit (Halo) / Reverse Non-Lit
MIRROR = {"CHANNEL_LETTERS_FL": ["CLOUD_SIGN_FL"], "HALO_LETTERS": ["CLOUD_SIGN_HALO"], "ILLUMINATION": ["CLOUD_SIGN_HALO"]}
NOT_FOR_CLOUDS = {"L01", "L03", "L06"}                        # letter cap height, letter cut files, halo letter stroke

def _row11(r):
    r = tuple(r)
    return r + ("",) * (11 - len(r))

def _rename(text):
    text = str(text or "")
    for a, b in RENAME.items(): text = text.replace(a, b)
    return text

def _sign_fields(letter_fields):
    head = [(C1, "QUANTITY", "QTY", "number", "1", "", "", "Yes", "", "Number of cloud signs", ""),
            (C1, "CLOUD SIZE", "CLOUD SIZE", "dims", "", "W|H", "", "Yes", "", "Overall cloud sign size, inches", "")]
    rest = []
    for r in letter_fields:
        r = list(_row11(r))
        if r[1] in LETTER_ONLY: continue
        if r[1] in RENAME: r[1] = RENAME[r[1]]
        r[6] = _rename(r[6])
        rest.append(tuple(r))
    return head + rest

def build(F, illumination_defaults=None):
    """Return (registry rows, {component_id: fields}) for the two cloud sign components."""
    illum = []
    for r in F["ILLUMINATION"]:
        r = list(_row11(r)); r[0] = C5
        if illumination_defaults and r[1] in illumination_defaults: r[4] = illumination_defaults[r[1]]
        illum.append(tuple(r))
    fields = {"CLOUD_SIGN_FL": _sign_fields(F["CHANNEL_LETTERS_FL"]),
              "CLOUD_SIGN_HALO": _sign_fields(F["HALO_LETTERS"]) + illum}
    reg = [("CLOUD_SIGN_FL", "Cloud Sign - Front Lit", "No", "Yes",
            "Front lit cloud sign: quantity and size, with the front lit channel letter face, return, trim cap, LED and mounting options."),
           ("CLOUD_SIGN_HALO", "Cloud Sign - Halo Lit", "No", "Yes",
            "Halo lit cloud sign: quantity and size, with the halo letter face, return, back, standoff and illumination options.")]
    assemblies = [("Cloud Sign - Front Lit", 1, "CLOUD_SIGN_FL", "Cloud Sign - Front Lit", "Required", "Yes", ""),
                  ("Cloud Sign - Halo Lit", 1, "CLOUD_SIGN_HALO", "Cloud Sign - Halo Lit", "Required", "Yes", "")]
    return reg, fields, assemblies

def _mirror_ids(text, sep):
    parts = str(text or "").split(sep)
    have = [p.strip() for p in parts]
    add = [m for p in have for m in MIRROR.get(p, [])]
    add = [m for i, m in enumerate(add) if m not in have and m not in add[:i]]
    return sep.join(parts + add) if add else text

def mirror_comps(comps, rule_id=""):
    if rule_id in NOT_FOR_CLOUDS or not str(comps or "").strip(): return comps
    return _mirror_ids(comps, ",")

def mirror_rule(rule, rule_id=""):
    """COMPONENT=... lists gain the cloud IDs; a LETTER TYPE condition gains its LIGHTING TYPE twin."""
    if rule_id in NOT_FOR_CLOUDS or not rule: return rule
    rule = re.sub(r"COMPONENT=([A-Z0-9_|]+)", lambda m: "COMPONENT=" + _mirror_ids(m.group(1), "|"), str(rule))
    twins = [_rename(p) for p in rule.split(" OR ") if "LETTER TYPE" in p]
    return rule + "".join(" OR " + t for t in twins if t not in rule)
