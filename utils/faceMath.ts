import { Employee, MatchResult } from '../types';

function normalize(vector: number[]): number[] {
  const magnitude = Math.sqrt(vector.reduce((sum, value) => sum + value * value, 0)) || 1;
  return vector.map((value) => value / magnitude);
}

export function generateDeterministicEmbedding(seed: string): number[] {
  let state = 2166136261;
  for (let index = 0; index < seed.length; index += 1) {
    state ^= seed.charCodeAt(index);
    state = Math.imul(state, 16777619);
  }

  const vector: number[] = [];
  for (let index = 0; index < 128; index += 1) {
    state ^= state << 13;
    state ^= state >>> 17;
    state ^= state << 5;
    vector.push((state >>> 0) / 0xffffffff * 2 - 1);
  }
  return normalize(vector);
}

export function simulateFaceScanVariation(embedding: number[], variation: number): number[] {
  return normalize(
    embedding.map((value, index) => value + Math.sin((index + 1) * 12.9898) * variation),
  );
}

function cosineDistance(left: number[], right: number[]): number {
  if (left.length === 0 || left.length !== right.length) {
    return 1;
  }
  const dot = left.reduce((sum, value, index) => sum + value * right[index], 0);
  const leftMagnitude = Math.sqrt(left.reduce((sum, value) => sum + value * value, 0));
  const rightMagnitude = Math.sqrt(right.reduce((sum, value) => sum + value * value, 0));
  if (!leftMagnitude || !rightMagnitude) {
    return 1;
  }
  return 1 - dot / (leftMagnitude * rightMagnitude);
}

export function findBestFaceMatch(
  probe: number[],
  employees: Employee[],
  threshold: number,
): MatchResult {
  const candidates = employees
    .filter((employee) => employee.isActive && employee.faceEmbedding?.length)
    .map((employee) => ({ employee, distance: cosineDistance(probe, employee.faceEmbedding ?? []) }))
    .sort((left, right) => left.distance - right.distance);
  const best = candidates[0];
  const matched = Boolean(best && best.distance <= threshold);

  return {
    matched,
    employee: matched ? best.employee : null,
    distance: best?.distance ?? 1,
    confidence: Math.max(0, Math.min(100, (1 - (best?.distance ?? 1)) * 100)),
    threshold,
    message: matched
      ? `Match found for ${best.employee.fullName}.`
      : 'No registered active employee matched this scan.',
  };
}
