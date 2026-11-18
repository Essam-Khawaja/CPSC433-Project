"""Timetable assignments and slot counters."""

class Assignment:
    def __init__(self) -> None:
        self.placements: dict = {} #component -> slot
        self.counts: dict = {} #slot -> number of assigned components
        self.al_counts: dict = {} # slot -> number of assigned AL components

    def add(self,component, slot) -> None:
        if component in self.placements:
            raise ValueError(f"{component} is already assigned")

        self.placements[component] = slot
        self.counts[slot] = self.counts.get(slot,0) + 1

        if component.al_required:
            self.al_counts[slot] = self.al_counts.get(slot,0) + 1

    def copy(self):
        new = Assignment()
        new.placements = self.placements.copy()
        new.counts = self.counts.copy()
        new.al_counts = self.al_counts.copy()
        return new
