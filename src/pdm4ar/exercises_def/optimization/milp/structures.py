from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Literal, Optional
import numpy as np


@dataclass(frozen=True)
class MilpFeasibility(Enum):
    feasible = "feasible"
    unfeasible = "unfeasible"

    def __eq__(self, other) -> bool:
        return self.value == other.value

@dataclass(frozen=True)
class MilpSolution:
    status: Literal[MilpFeasibility.feasible, MilpFeasibility.unfeasible]
    voyage_plan: Optional[List[int]] = None

@dataclass(frozen=True)
class ProblemSolutions:
    min_total_compass_time: Optional[MilpSolution] = None
    max_final_crew: Optional[MilpSolution] = None
    min_total_sail_time: Optional[MilpSolution] = None
    min_total_travelled_distance: Optional[MilpSolution] = None
    min_max_sail_time: Optional[MilpSolution] = None


@dataclass(frozen=True)
class Island:
    id: int
    arch: int
    x: float
    y: float
    departure: float
    arrival: float
    time_compass: int
    crew: int

@dataclass(frozen=True)
class ProblemVoyage:
    start_crew: int
    islands: Tuple[Island]
    min_fix_time_individual_island: int
    min_crew: int
    max_crew: int
    max_duration_individual_journey: float
    max_distance_individual_journey: float   

@dataclass(frozen=True)
class ProblemVoyage1(ProblemVoyage):
    ...

@dataclass(frozen=True)
class ProblemVoyage2(ProblemVoyage):
    start_pos: Tuple[float, float]
    end_pos: Tuple[float, float]   




# Following structures are not important for the student's exercise development


@dataclass(frozen=True)
class SolutionsCosts:
    min_total_compass_time:  Optional[float]
    max_final_crew:  Optional[float]
    min_total_sail_time:  Optional[float]
    min_total_travelled_distance:  Optional[float]
    min_max_sail_time: Optional[float]

@dataclass(frozen=True)
class MilpPerformance(SolutionsCosts):
    ...

    def __post_init__(self):
        perf_scores = [getattr(self, name_cost) for name_cost in self.__annotations__.keys()]
        assert  all([perf_score >= 0 or np.isnan(perf_score) for perf_score in perf_scores]), \
            f"some performance scores {perf_scores} are less than 0"

@dataclass(frozen=True)
class PerformanceWeight(MilpPerformance):
    ...

    def __post_init__(self):
        weights = [getattr(self, name_cost) for name_cost in self.__annotations__.keys()]
        assert  sum(weights) == 1, \
            f"perf weights {weights} don't sum up to 1 ({sum(weights)})"

@dataclass(frozen=True)
class MilpFinalPerformance(MilpPerformance):
    overall_score: float

    def __post_init__(self):
        perf_scores = [getattr(self, name_cost) for name_cost in self.__annotations__.keys()]
        assert  all([perf_score >= 0 or np.isnan(perf_score) for perf_score in perf_scores]), \
            f"some performance scores {perf_scores} are less than 0"

@dataclass(frozen=True)
class aViolations:
    all_archipelagos: Optional[int]
    n_islands: Optional[int]
    single_visit: Optional[int]
    order_visit: Optional[int]
    min_fix_time: Optional[int]
    min_crew: Optional[int]
    max_crew: Optional[int]
    max_duration: Optional[float]
    max_distance: Optional[float]

@dataclass(frozen=True)
class SolutionViolations:
    min_total_compass_time: Optional[aViolations]
    max_final_crew: Optional[aViolations]
    min_total_sail_time: Optional[aViolations]
    min_total_travelled_distance: Optional[aViolations]
    min_max_sail_time: Optional[aViolations]


@dataclass(frozen=True)
class SlackViolations(SolutionViolations):
    ...

@dataclass(frozen=True)
class SlackCosts(SolutionsCosts):
    ...
