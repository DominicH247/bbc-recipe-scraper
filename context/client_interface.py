from abc import ABC, abstractmethod
from typing import Any

class IClientInterface(ABC):
    @abstractmethod
    def get_connection(self,  database: str, collection: str, schema) -> Any:
        raise NotImplementedError