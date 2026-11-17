"""

Input parsing

The File Format is:

Name:
Example-name
Lecture slots:
Day, Start time, lecturemax, lecturemin, allecturemax
Tutorial slots:
Day, Start time, tutorialmax, tutorialmin, altutorialmax
Lectures:
Lecture Identifier, alrequired
Tutorials:
Tutorial Identifier, alrequired
Not compatible:
Lecture Identifier, Lecture Identifier
Lecture Identifier, Tutorial Identifier
Tutorial Identifier, Tutorial Identifier
Unwanted:
Lecture Identifier, Slot day, Slot time
Tutorial Identifier, Slot day, Slot time
Preferences:
Slot day, Slot time, Lecture Identifier, Preference value
Slot day, Slot time, Tutorial Identifier, Preference value
Pair:
Lecture Identifier, Lecture Identifier
Lecture Identifier, Tutorial Identifier
Tutorial Identifier, Tutorial Identifier
Partial assignments:
Lecture Identifier, Slot day, Slot time
Tutorial Identifier, Slot day, Slot time

"""
from model.components import Lecture, Tutorial
from model.slot import Slot


def cleanName(name: str) -> str:
    # "CPSC  231 LEC 01" -> "CPSC 231 LEC 01"
    return " ".join(name.split())


def toMinutes(time: str) -> int:
    # "9:30" -> 570
    hours, minutes = time.split(":")
    return int(hours) * 60 + int(minutes)


def readInput(file_path: str) -> dict:

    data = {
        "name": "",
        "lecture slots": [],   # Slot obj list
        "tutorial slots": [],   # Slot obj list
        "lectures": [],   # Lec obj lists
        "tutorials": [],  # tut obj lists
        "not compatible": [],    # list of (comp, comp)
        "unwanted": [],   # list of (comp, slot)
        "preferences": [],    # list of (comp, slot, penaltyInt)
        "pair": [],  # list of (comp, comp)
        "partial assignments": [], # list of (comp, slot)
    }

    # Lookups used to turn names in later sections into objects
    components = {}   # "CPSC 231 LEC 01" -> Lecture/Tutorial
    lecSlots = {}     # ("MO", 480) -> Slot
    tutSlots = {}     # ("MO", 480) -> Slot

    currentSection = None

    with open(file_path, "r", encoding="utf-8") as file:
        for lineNumber, line in enumerate(file, start=1):
            line = line.strip()

            # Ignore empty lines without ending the loop.
            if not line:
                continue

            # A header changes which section receives subsequent lines.
            if line.endswith(":"):
                header = line[:-1].strip().lower()

                if header not in data:
                    raise ValueError(f"Line {lineNumber}: unknown section '{line}'")

                currentSection = header
                continue

            if currentSection is None:
                raise ValueError(f"Line {lineNumber}: data appears before a section")

            fields = [field.strip() for field in line.split(",")]   # Take all the individual words out of the current line

            if currentSection == "name":
                data["name"] = line

            elif currentSection == "lecture slots" or currentSection == "tutorial slots":
                try:
                    if currentSection == "lecture slots":
                        kind = "LEC"
                    else:
                        kind = "TUT"

                    day = fields[0]
                    time = fields[1]
                    slot = Slot(kind, day, time, int(fields[2]), int(fields[3]), int(fields[4]))

                    data[currentSection].append(slot)
                    if kind == "LEC":
                        lecSlots[(day, toMinutes(time))] = slot
                    else:
                        tutSlots[(day, toMinutes(time))] = slot
                except (ValueError, IndexError):
                    raise ValueError(f"Line {lineNumber}: error in slot format")

            elif currentSection == "lectures":
                try:
                    id = cleanName(fields[0])
                    tokens = id.split()
                    program = tokens[0]
                    number = int(tokens[1])
                    al_required = fields[1].lower() == "true"
                    section = tokens[3]

                    lecture = Lecture(id, program, number, al_required, section)
                    data["lectures"].append(lecture)
                    components[id] = lecture
                except (ValueError, IndexError):
                    raise ValueError(f"Line {lineNumber}: error in lecture format")

            elif currentSection == "tutorials":
                try:
                    id = cleanName(fields[0])
                    tokens = id.split()
                    program = tokens[0]
                    number = int(tokens[1])
                    al_required = fields[1].lower() == "true"

                    if tokens[2] == "LEC":
                        # CPSC 231 LEC 01 TUT 02
                        lec_section = tokens[3]
                        tut_number = tokens[5]
                    else:
                        # SENG 300 TUT 01
                        lec_section = None
                        tut_number = tokens[3]

                    tutorial = Tutorial(id, program, number, al_required, lec_section, tut_number)
                    data["tutorials"].append(tutorial)
                    components[id] = tutorial
                except (ValueError, IndexError):
                    raise ValueError(f"Line {lineNumber}: error in tutorial format")

            else:
                # Keep the raw fields for now; turned into objects after the whole file is read
                data[currentSection].append(fields)

    # ---- Turn the raw name/slot strings into objects ----

    def findComponent(name: str):
        name = cleanName(name)
        if name not in components:
            raise ValueError(f"Unknown lecture/tutorial: '{name}'")
        return components[name]

    def findSlot(component, day: str, time: str):
        # The same "MO, 8:00" can be a lecture slot or a tutorial slot,
        # so pick based on what the component is.
        if component.is_lecture():
            slots = lecSlots
        else:
            slots = tutSlots

        key = (day, toMinutes(time))
        if key not in slots:
            raise ValueError(f"Unknown slot '{day}, {time}' for {component}")
        return slots[key]

    notCompatible = []
    for fields in data["not compatible"]:
        a = findComponent(fields[0])
        b = findComponent(fields[1])
        notCompatible.append((a, b))
    data["not compatible"] = notCompatible

    unwanted = []
    for fields in data["unwanted"]:
        comp = findComponent(fields[0])
        slot = findSlot(comp, fields[1], fields[2])
        unwanted.append((comp, slot))
    data["unwanted"] = unwanted

    preferences = []
    for fields in data["preferences"]:
        # Order here is: day, time, component, value
        comp = findComponent(fields[2])
        slot = findSlot(comp, fields[0], fields[1])
        value = int(fields[3])
        preferences.append((comp, slot, value))
    data["preferences"] = preferences

    pairs = []
    for fields in data["pair"]:
        a = findComponent(fields[0])
        b = findComponent(fields[1])
        pairs.append((a, b))
    data["pair"] = pairs

    partial = []
    for fields in data["partial assignments"]:
        comp = findComponent(fields[0])
        slot = findSlot(comp, fields[1], fields[2])
        partial.append((comp, slot))
    data["partial assignments"] = partial

    return data
