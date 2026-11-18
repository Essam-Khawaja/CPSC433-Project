"""Shared limit on search work rather than elapsed time."""


class StepBudget:
    def __init__(self, max_steps: int):
        if max_steps < 0:
            raise ValueError("Step budget cannot be negative")

        self.remaining = max_steps

    def expired(self) -> bool:
        return self.remaining <= 0

    def consume(self) -> None:
        if self.expired():
            raise RuntimeError("Step budget is exhausted")

        self.remaining -= 1
