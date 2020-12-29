from logging import getLogger
from pathlib import Path
from typing import Any, List

from ansible_generator.directory_generator.strategy import DirectoryStrategy


class DirectoryGenerator:
    """The DirectoryGenerator defines the interface to clients."""

    def __init__(self, strategy: DirectoryStrategy, log_handlers: List[Any]) -> None:
        """Accept a strategy at construction time, this can be overridden later."""
        self.handlers = log_handlers
        self.logger = getLogger(__name__)
        for handler in log_handlers:
            self.logger.addHandler(handler)
        self._strategy = strategy

    @property
    def strategy(self) -> DirectoryStrategy:
        """The strategy property is a reference to the DirectoryStrategy object.

        We don't care what the actual strategy is (normal layout? alternate? Kevin's special?)
        We just need it to conform to the DirectoryStrategy interface.
        """
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: DirectoryStrategy) -> None:
        """Allow replacement of the strategy at runtime."""
        self._strategy = strategy

    def apply_many(self, paths: List[Path]) -> None:
        self.logger.debug("Applying strategy to paths", paths=paths)
        self.strategy.apply_directory_structure_to_paths([Path(path) for path in paths])

    def apply(self, path: Path) -> None:
        self.logger.debug("Apply strategy to path", path=path)
        self.strategy.apply_directory_structure_to_path(Path(path))
