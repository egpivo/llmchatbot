from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class ChatterOutput:
    chatbot: List[Tuple[str, str]]
    history: List[Tuple[str, str]]
    audio_data: Optional[Tuple[int, bytes]] = None
    audio_message: Optional[bytes] = None
    text_message: Optional[str] = None
