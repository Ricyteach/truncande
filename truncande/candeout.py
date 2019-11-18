from dataclasses import dataclass, field
from itertools import count
from typing import Tuple, List, Iterator, MutableSequence


class CandeOutError(Exception):
    pass


@dataclass
class CandeOut:
    lines: MutableSequence[str] = field(repr=False)
    step_line_nos: List[int] = field(repr=False, init=False)
    n_lines: int = field(init=False)
    n_steps: int = field(init=False)

    def __post_init__(self):
        self.n_lines = len(self.lines)
        self.n_steps = get_n_steps(self.lines)
        self.step_line_nos = steppify(self.lines, self.n_steps)


def get_n_steps(lines) -> int:
    for line in lines:
        if "THE NUMBER OF LOAD STEPS IS------------" in line:
            try:
                return int(line.split()[-1])
            except ValueError:
                continue
    else:
        raise CandeOutError("load steps declaration not found")


def steppify(lines, n_steps) -> List[int]:

    ilinecount: Iterator[Tuple[int, str]] = zip(count(), iter(lines))
    seek_solution_output_results(ilinecount)

    step_line_nos =list()
    try:
        for x in range(1, n_steps+1):
            n = seek_finite_element_output_for_load_step(ilinecount, x) - 3
            step_line_nos.append(n)
        return step_line_nos
    except Exception as e:
        raise CandeOutError("error reading load step output") from e


def remove_steps(candeout: CandeOut, steps: Tuple[int]=(-1,)) -> None:

    n_steps = candeout.n_steps

    keep_steps = list(steps)
    for i, step in enumerate(keep_steps):
        if step<0:
            keep_steps[i] = n_steps-step
    keep_steps = set(steps)

    step_line_nos = candeout.step_line_nos
    step_line_nos.append(-1)

    for start, stop in zip(step_line_nos[1::-1], step_line_nos[:-1:-1]):
        if start in keep_steps:
            continue
        del candeout.lines[start:stop]


def seek_solution_output_results(ilinecount: Iterator[Tuple[int, str]]) -> int:
    return seek_text("  SOLUTION OUTPUT RESULTS", ilinecount)


def seek_finite_element_output_for_load_step(ilinecount: Iterator[Tuple[int, str]], x: int) -> int:
    return seek_text(f"  FINITE ELEMENT OUTPUT FOR LOAD STEP {x: >2d}", ilinecount)


def seek_text(text: str, ilinecount: Iterator[Tuple[int, str]]) -> int:
    for ct, line in ilinecount:
        if text in line:
            return ct
    else:
        raise CandeOutError(f"{text!r} not found")
