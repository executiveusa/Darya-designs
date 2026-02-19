const HOTPAD_KEY = "dara_hotpad";

export function getHotpadPins(): string[] {
  if (typeof window === "undefined") {
    return [];
  }
  const stored = localStorage.getItem(HOTPAD_KEY);
  if (!stored) return [];
  try {
    return JSON.parse(stored);
  } catch {
    return [];
  }
}

export function setHotpadPins(pins: string[]) {
  if (typeof window === "undefined") {
    return;
  }
  localStorage.setItem(HOTPAD_KEY, JSON.stringify(pins));
}

export function toggleHotpadPin(id: string) {
  const current = getHotpadPins();
  if (current.includes(id)) {
    setHotpadPins(current.filter((pin) => pin !== id));
  } else {
    setHotpadPins([...current, id].slice(0, 6));
  }
}
