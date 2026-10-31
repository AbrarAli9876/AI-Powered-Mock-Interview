import {
  getInterviews,
  getTopics,
  getCodingInterviews,
  type Interview,
  type Topic,
  type CodingInterview,
} from "./api";

interface CacheEntry<T> {
  data: T;
  timestamp: number;
}

interface MemoryCache {
  userId?: string;
  interviews?: CacheEntry<Interview[]>;
  topics?: CacheEntry<Topic[]>;
  codingInterviews?: CacheEntry<CodingInterview[]>;
}

const memoryCache: MemoryCache = {};

let pendingInterviewsPromise: Promise<Interview[]> | null = null;
let pendingTopicsPromise: Promise<Topic[]> | null = null;
let pendingCodingInterviewsPromise: Promise<CodingInterview[]> | null = null;

// Cache lifetime: 2 minutes for interviews (or until explicitly invalidated)
const CACHE_TTL_MS = 2 * 60 * 1000;
// Topics rarely change, keep for 10 minutes
const TOPICS_TTL_MS = 10 * 60 * 1000;

function getCurrentUserId(): string {
  try {
    const rawUser = localStorage.getItem("user");
    if (!rawUser) return "anonymous";
    const user = JSON.parse(rawUser);
    return user?.id ? String(user.id) : "anonymous";
  } catch {
    return "anonymous";
  }
}

function getSessionStorageKey(type: string): string {
  const userId = getCurrentUserId();
  return `app_cache_${userId}_${type}`;
}

function readSessionStorage<T>(key: string, ttlMs: number): T | null {
  try {
    const raw = sessionStorage.getItem(key);
    if (!raw) return null;
    const entry: CacheEntry<T> = JSON.parse(raw);
    if (Date.now() - entry.timestamp > ttlMs) {
      sessionStorage.removeItem(key);
      return null;
    }
    return entry.data;
  } catch {
    return null;
  }
}

function writeSessionStorage<T>(key: string, data: T): void {
  try {
    const entry: CacheEntry<T> = {
      data,
      timestamp: Date.now(),
    };
    sessionStorage.setItem(key, JSON.stringify(entry));
  } catch {
    // Continue if storage is quota-limited
  }
}

/* =========================================================
   SYNCHRONOUS CACHE READERS (Zero loading delay)
   ========================================================= */

export function getCachedInterviews(): Interview[] | null {
  const currentUserId = getCurrentUserId();
  if (
    memoryCache.userId === currentUserId &&
    memoryCache.interviews &&
    Date.now() - memoryCache.interviews.timestamp <= CACHE_TTL_MS
  ) {
    return memoryCache.interviews.data;
  }
  const sessionData = readSessionStorage<Interview[]>(
    getSessionStorageKey("interviews"),
    CACHE_TTL_MS,
  );
  if (sessionData) {
    memoryCache.userId = currentUserId;
    memoryCache.interviews = { data: sessionData, timestamp: Date.now() };
    return sessionData;
  }
  return null;
}

export function getCachedTopics(): Topic[] | null {
  if (
    memoryCache.topics &&
    Date.now() - memoryCache.topics.timestamp <= TOPICS_TTL_MS
  ) {
    return memoryCache.topics.data;
  }
  const sessionData = readSessionStorage<Topic[]>(
    "app_cache_topics",
    TOPICS_TTL_MS,
  );
  if (sessionData) {
    memoryCache.topics = { data: sessionData, timestamp: Date.now() };
    return sessionData;
  }
  return null;
}

export function getCachedCodingInterviews(): CodingInterview[] | null {
  const currentUserId = getCurrentUserId();
  if (
    memoryCache.userId === currentUserId &&
    memoryCache.codingInterviews &&
    Date.now() - memoryCache.codingInterviews.timestamp <= CACHE_TTL_MS
  ) {
    return memoryCache.codingInterviews.data;
  }
  const sessionData = readSessionStorage<CodingInterview[]>(
    getSessionStorageKey("coding_interviews"),
    CACHE_TTL_MS,
  );
  if (sessionData) {
    memoryCache.userId = currentUserId;
    memoryCache.codingInterviews = {
      data: sessionData,
      timestamp: Date.now(),
    };
    return sessionData;
  }
  return null;
}

/* =========================================================
   ASYNCHRONOUS CACHE FETCHERS (Deduplicated & Cached)
   ========================================================= */

export async function fetchInterviewsCached(options?: {
  force?: boolean;
}): Promise<Interview[]> {
  const currentUserId = getCurrentUserId();

  if (!options?.force) {
    const cached = getCachedInterviews();
    if (cached) return cached;
  }

  if (pendingInterviewsPromise) {
    return pendingInterviewsPromise;
  }

  pendingInterviewsPromise = (async () => {
    try {
      const data = await getInterviews();
      memoryCache.userId = currentUserId;
      memoryCache.interviews = { data, timestamp: Date.now() };
      writeSessionStorage(getSessionStorageKey("interviews"), data);
      return data;
    } finally {
      pendingInterviewsPromise = null;
    }
  })();

  return pendingInterviewsPromise;
}

export async function fetchTopicsCached(options?: {
  force?: boolean;
}): Promise<Topic[]> {
  if (!options?.force) {
    const cached = getCachedTopics();
    if (cached) return cached;
  }

  if (pendingTopicsPromise) {
    return pendingTopicsPromise;
  }

  pendingTopicsPromise = (async () => {
    try {
      const data = await getTopics();
      memoryCache.topics = { data, timestamp: Date.now() };
      writeSessionStorage("app_cache_topics", data);
      return data;
    } finally {
      pendingTopicsPromise = null;
    }
  })();

  return pendingTopicsPromise;
}

export async function fetchCodingInterviewsCached(options?: {
  force?: boolean;
}): Promise<CodingInterview[]> {
  const currentUserId = getCurrentUserId();

  if (!options?.force) {
    const cached = getCachedCodingInterviews();
    if (cached) return cached;
  }

  if (pendingCodingInterviewsPromise) {
    return pendingCodingInterviewsPromise;
  }

  pendingCodingInterviewsPromise = (async () => {
    try {
      const data = await getCodingInterviews();
      memoryCache.userId = currentUserId;
      memoryCache.codingInterviews = { data, timestamp: Date.now() };
      writeSessionStorage(getSessionStorageKey("coding_interviews"), data);
      return data;
    } finally {
      pendingCodingInterviewsPromise = null;
    }
  })();

  return pendingCodingInterviewsPromise;
}

/* =========================================================
   CACHE INVALIDATION (When interviews complete or user logs out)
   ========================================================= */

export function invalidateTechnicalInterviewCache(): void {
  delete memoryCache.interviews;
  pendingInterviewsPromise = null;
  const key = getSessionStorageKey("interviews");
  try {
    sessionStorage.removeItem(key);
    // Also remove legacy dashboard cache key if present
    sessionStorage.removeItem("technicalInterviewDashboardCache");
  } catch {
    // Continue
  }
}

export function invalidateCodingInterviewCache(): void {
  delete memoryCache.codingInterviews;
  pendingCodingInterviewsPromise = null;
  const key = getSessionStorageKey("coding_interviews");
  try {
    sessionStorage.removeItem(key);
  } catch {
    // Continue
  }
}

export function clearAppCache(): void {
  delete memoryCache.userId;
  delete memoryCache.interviews;
  delete memoryCache.topics;
  delete memoryCache.codingInterviews;
  pendingInterviewsPromise = null;
  pendingTopicsPromise = null;
  pendingCodingInterviewsPromise = null;

  try {
    const keysToRemove: string[] = [];
    for (let i = 0; i < sessionStorage.length; i += 1) {
      const k = sessionStorage.key(i);
      if (k && (k.startsWith("app_cache_") || k.includes("technicalInterview"))) {
        keysToRemove.push(k);
      }
    }
    keysToRemove.forEach((k) => sessionStorage.removeItem(k));
  } catch {
    // Continue
  }
}

