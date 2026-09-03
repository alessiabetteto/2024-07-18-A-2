from dataclasses import dataclass


@dataclass
class Gene:
    GeneID: str
    Function: str
    Essential: str
    Chromosome: int

    def __str__(self):
        return f"{self.GeneID} - {self.Function} | Ess.: {self.Essential}, Chrom.: {self.Chromosome}"

    def __hash__(self):
        return hash((self.GeneID, self.Function))

    def __eq__(self, other):
        return (self.GeneID, self.Function) == (other.GeneID, other.Function)
