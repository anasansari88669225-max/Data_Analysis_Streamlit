"""Synthetic demo embeddings and cosine-distance matching."""

from __future__ import annotations

import hashlib
import math
import random
from collections.abc import Sequence


def generate_deterministic_embedding(seed: str, dimensions: int = 128) -> list[float]:
    seed_bytes = hashlib.sha256(seed.encode("utf-8")).digest()
    rng = random.Random(int.from_bytes(seed_bytes, "big"))
    vector = [rng.uniform(-1.0, 1.0) for _ in range(dimensions)]
    magnitude = math.sqrt(sum(value * value for value in vector))
    return [value / magnitude for value in vector]


def cosine_distance(left: Sequence[float], right: Sequence[float]) -> float:
    if not left or len(left) != len(right):
        raise ValueError("Face embeddings must be non-empty vectors of equal length.")
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if not left_norm or not right_norm:
        raise ValueError("Face embeddings must have non-zero magnitude.")
    similarity = sum(a * b for a, b in zip(left, right)) / (left_norm * right_norm)
    return 1.0 - max(-1.0, min(1.0, similarity))
