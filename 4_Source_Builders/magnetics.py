"""v4.5: Magnetics - vehicle and indoor magnets: magnetic sheeting with a printed (mounted or direct) or cut vinyl graphic.

Fields follow management's MAGNETICS table (October 15, 2026 catalog) plus industry practice:
  30 mil sheeting is the vehicle grade (20 / 15 mil are indoor grades), 1" rounded corners resist wind lift,
  magnets hold on steel only and need a flat area clear of body lines.
Production: every magnet spec goes to the Vinyl department (plotter / hand cut, print, laminate).
SignOS: no magnetic sheeting item yet (SignOS_Ref left blank until the SKU is set up).
"""
C1, C2, C3 = "COLUMN 1", "COLUMN 2", "COLUMN 3"
PRINT = "GRAPHIC TYPE~=Print"
CUT = "GRAPHIC TYPE~=Cut Vinyl"

# (zone, variable, label, type, default, options, show_if, required, signos_ref, notes, hide_values)
FIELDS = [
    (C1, "QUANTITY", "QTY", "select", "1 Pair (2 Pieces)", "1 Pair (2 Pieces)|1 Piece|Custom Set", "", "Yes", "",
     "Vehicle door magnets are usually sold as a pair (driver + passenger side)", ""),
    (C1, "SIZE", "DIMENSIONS", "dims", "24|18", "W|H", "", "Yes", "",
     'Common sizes: 12x18 (car door), 12x24 (long doors, vans), 18x24 (vans, box trucks), 24x36 (truck sides, tailgates)', ""),
    (C1, "APPLICATION", "APPLICATION", "select", "Vehicle Door", "Vehicle Door|Vehicle Tailgate / Rear|Indoor (Fridge, Steel Door, Display)", "", "Yes", "",
     "Where the magnet goes: vehicles need 30 mil sheeting and a flat steel area", ""),
    (C2, "SUBSTRATE", "SUBSTRATE", "select", "30 mil Magnetic Sheeting (Vehicle)",
     "30 mil Magnetic Sheeting (Vehicle)|20 mil Magnetic Sheeting (Indoor)|15 mil Magnetic Sheeting (Indoor, Light)", "", "Yes", "",
     "30 mil is the vehicle grade; 20 mil lacks the pull for highway speeds", ""),
    (C2, "MAGNET FACE", "MAGNET FACE", "select", "White", "White|Black", "", "Yes", "",
     "Face color of the sheeting (shows behind cut vinyl)", ""),
    (C2, "GRAPHIC TYPE", "GRAPHIC", "select", "Digital Print Vinyl Mounted (Arlon 4500GLX)",
     "Digital Print Vinyl Mounted (Arlon 4500GLX)|Direct Print|Cut Vinyl (Oracal 751)", "", "Yes", "", "", ""),
    (C3, "OVERLAMINATE", "OVERLAMINATE", "select", "Arlon 3210 Premium Laminate",
     "Arlon 3210 Premium Laminate|3M 8518 Wrap Gloss Laminate|3M 8520 Wrap Matte Laminate|None", PRINT, "Yes", "", "", ""),
    (C3, "PRINT COLOR", "COLOR", "fullcolor", "Full Color Digital", "", PRINT, "", "", "", ""),
    (C3, "VINYL COLOR", "COLOR", "vinyl", "751RA", "751RA|951|651", CUT, "Yes", "", "", ""),
    (C3, "CORNERS", "CORNERS", "select", 'Rounded 1"', 'Rounded 1"|Rounded 1/2"|Square|Custom Contour Cut', "", "Yes", "",
     'Rounded corners keep wind from lifting the magnet at speed', ""),
]

REGISTRY = ("MAGNETIC", "Magnetics", "No", "Yes", "Vehicle and indoor magnets: magnetic sheeting with a printed or cut vinyl graphic.")
ASSEMBLY = ("Magnetics", 1, "MAGNETIC", "Magnetics", "Required", "Yes", "")

# (Rule_ID, Section, Components, Match_Rule, Standard, Why, CorelDRAW_How_To, Basis, Order, Active)
GUIDE = [
    ("M01", "MAGNETICS", "MAGNETIC", "APPLICATION~=Vehicle",
     "Magnets hold on steel only: confirm the panel is steel (aluminum or fiberglass doors and trucks need a decal instead). "
     "Measure only the flat area of the panel - clear of body lines, handles, trim, badges and rivets - and keep 1\" clear of every edge.",
     "A magnet over a curve or edge lifts at speed and can fly off.", "", "Industry", 900, "Yes"),
    ("M02", "MAGNETICS", "MAGNETIC", "APPLICATION~=Vehicle",
     "Vehicle magnets: 30 mil sheeting and rounded corners (1\" standard). Keep art inside a 1/8\" safe zone; 1/8\" bleed for printed magnets.",
     "20 mil and thinner lack the pull for highway speeds; square corners catch the wind.", "", "Industry", 910, "Yes"),
    ("M03", "MAGNETICS", "MAGNETIC", "",
     "Tell the customer: remove the magnet weekly and before car washes, clean and dry both sides, store flat or rolled printed side out, "
     "avoid hoods and roofs in direct sun, and wait about 90 days after new paint (60 after clear coat) before applying.",
     "Moisture and heat trapped under the magnet can mark the paint.", "", "Industry", 920, "Yes"),
]
