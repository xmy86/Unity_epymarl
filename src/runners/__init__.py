REGISTRY = {}

from .episode_runner import EpisodeRunner
REGISTRY["episode"] = EpisodeRunner

from .episode_runner_continue import EpisodeRunnerContinue
REGISTRY["episode_continue"] = EpisodeRunnerContinue

from .parallel_runner import ParallelRunner
REGISTRY["parallel"] = ParallelRunner
