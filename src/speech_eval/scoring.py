"""Edit-distance scores with an explicit, versioned text policy.

The basic policy is intentionally modest. It does not translate, transliterate,
remove fillers or Singapore discourse particles, or standardize spelling.
"""

from dataclasses import dataclass
import unicodedata


POLICIES = ("strict", "basic")


def normalize(text: str, policy: str = "basic") -> str:
    if policy not in POLICIES:
        raise ValueError(f"unknown normalization policy: {policy}")
    if policy == "strict":
        return text
    text = unicodedata.normalize("NFKC", text).casefold()
    # Remove punctuation without deleting the token it surrounds: [ah] -> ah.
    # Apostrophes within words are removed: don't -> dont.
    text = "".join("" if unicodedata.category(c).startswith("P") else c for c in text)
    return " ".join(text.split())


def tokenize(text: str, unit: str = "word", policy: str = "basic") -> list[str]:
    text = normalize(text, policy)
    if unit == "word":
        return text.split()
    if unit == "character":
        return [c for c in text if not c.isspace()]
    raise ValueError(f"unknown unit: {unit}")


@dataclass(frozen=True)
class Counts:
    reference_units: int = 0
    substitutions: int = 0
    deletions: int = 0
    insertions: int = 0

    @property
    def errors(self) -> int:
        return self.substitutions + self.deletions + self.insertions

    @property
    def rate(self) -> float | None:
        # An empty reference has no meaningful denominator, even if the
        # hypothesis contains insertions. The insertions remain in counts.
        return self.errors / self.reference_units if self.reference_units else None

    def __add__(self, other: "Counts") -> "Counts":
        return Counts(
            self.reference_units + other.reference_units,
            self.substitutions + other.substitutions,
            self.deletions + other.deletions,
            self.insertions + other.insertions,
        )

    def as_dict(self) -> dict:
        return {
            "reference_units": self.reference_units,
            "substitutions": self.substitutions,
            "deletions": self.deletions,
            "insertions": self.insertions,
            "errors": self.errors,
            "rate": self.rate,
        }


def edit_counts(reference: list[str], hypothesis: list[str]) -> Counts:
    """Levenshtein alignment; ties prefer substitution, deletion, insertion."""
    # A cell stores (errors, substitutions, deletions, insertions).
    previous = [(j, 0, 0, j) for j in range(len(hypothesis) + 1)]
    for i, ref_unit in enumerate(reference, start=1):
        current = [(i, 0, i, 0)]
        for j, hyp_unit in enumerate(hypothesis, start=1):
            if ref_unit == hyp_unit:
                same = previous[j - 1]
                candidates = [(same, 0)]
            else:
                e, s, d, ins = previous[j - 1]
                candidates = [((e + 1, s + 1, d, ins), 0)]
            e, s, d, ins = previous[j]
            candidates.append(((e + 1, s, d + 1, ins), 1))
            e, s, d, ins = current[j - 1]
            candidates.append(((e + 1, s, d, ins + 1), 2))
            current.append(min(candidates, key=lambda item: (item[0][0], item[1]))[0])
        previous = current
    _, substitutions, deletions, insertions = previous[-1]
    return Counts(len(reference), substitutions, deletions, insertions)


def score_pair(reference: str, hypothesis: str, unit: str = "word", policy: str = "basic") -> Counts:
    return edit_counts(tokenize(reference, unit, policy), tokenize(hypothesis, unit, policy))
