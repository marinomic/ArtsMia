from dataclasses import dataclass

from model.ArtObject import ArtObject


@dataclass
class Connessione:
    u: ArtObject
    v: ArtObject
    weight: int

    def __str__(self):
        return f"Arco:{self.u.object_id} - {self.v.object_id} - Peso: {self.weight}"
