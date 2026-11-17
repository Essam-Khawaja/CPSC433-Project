"""Timetable slot representation."""

class Slot:
    def __init__(self, day: str, start_time: str, max_capacity: int, min_capacity: int, al_max_capacity: int):
        self.day = day
        self.start_time = start_time
        self.max_capacity = max_capacity
        self.min_capacity = min_capacity
        self.al_max_capacity = al_max_capacity
