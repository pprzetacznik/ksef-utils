from __future__ import annotations
from abc import ABC, abstractmethod
from argparse import Namespace, ArgumentParser
from ksef_utils.utils import KSEFUtils


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class GenerateCertsCommand(Command):
    def __init__(
        self,
        identifier: str,
        identifier_type: KSEFUtils.SerialNumberType,
        working_directory: str,
    ) -> None:
        self.identifier = identifier
        self.identifier_type = identifier_type
        self.working_directory = working_directory

    def execute(self) -> None:
        KSEFUtils.generate_certs(
            self.identifier, self.identifier_type, self.working_directory
        )
