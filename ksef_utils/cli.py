from abc import ABC, abstractmethod
from ksef_utils.utils import KSEFUtils


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        """Command pattern interface"""
        pass


class GenerateCertsCommand(Command):
    """
    Command line interface for certs generation.

    """

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
        """
        Generate certs.
        """
        KSEFUtils.generate_certs(
            self.identifier, self.identifier_type, self.working_directory
        )
