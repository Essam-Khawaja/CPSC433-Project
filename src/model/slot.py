"""Timetable slot representation."""

class Slot:
    def __init__(self, kind: str, day: str, start_time: str, max_capacity: int, min_desired: int, al_max_capacity: int):
        self.kind = kind              # "LEC" or "TUT"
        self.day = day                # "MO", "TU", "FR"
        self.start_time = start_time  # e.g. "9:30"
        self.max_capacity = max_capacity
        self.min_desired = min_desired
        self.al_max_capacity = al_max_capacity

        # Convert "9:30" into minutes since midnight (570)
        hours, minutes = start_time.split(":")
        self.start = int(hours) * 60 + int(minutes)

        # Work out which days the slot actually meets, and how long it lasts
        if kind == "LEC" and day == "MO":
            self.days = {"M", "W", "F"}
            length = 60
        elif kind == "LEC" and day == "TU":
            self.days = {"T", "R"}
            length = 90
        elif kind == "TUT" and day == "MO":
            self.days = {"M", "W"}
            length = 60
        elif kind == "TUT" and day == "TU":
            self.days = {"T", "R"}
            length = 60
        elif kind == "TUT" and day == "FR":
            self.days = {"F"}
            length = 120
        else:
            raise ValueError(f"Unknown slot: {kind} {day}")

        self.end = self.start + length

    def overlaps(self, other: Slot) -> bool:
        # No shared day means no overlap
        shared_days = self.days & other.days
        if not shared_days:
            return False

        # One ends before (or exactly when) the other starts
        if self.end <= other.start:
            return False
        if other.end <= self.start:
            return False

        return True

    def __repr__(self) -> str:
        return f"{self.day}, {self.start_time}"
