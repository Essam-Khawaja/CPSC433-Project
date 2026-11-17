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

def readInput(file_path: str) -> dict:

    data = {
        "name": "",
        "lecture slots": [],   # Slot obj list
        "tutorial slots": [],   # Tut obj list
        "lectures": [],   # Lec obj lists
        "tutorials": [],  # tut obj lists
        "not compatible": [],    # list of (comp, comp)
        "unwanted": [],   # list of (comp, slot)
        "preferences": [],    # list of (comp, slot, penaltyInt)
        "pair": [],  # list of (comp, comp)
        "partial assignments": [], # list of (comp, slot)
    }

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

            if currentSection == "name":
                data["name"] = line
            else:
                fields = [field.strip() for field in line.split(",")]   # Temporary, we will mold these into diff objs later
                data[currentSection].append(fields)

    return data
