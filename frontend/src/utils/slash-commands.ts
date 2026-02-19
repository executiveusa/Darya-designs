export interface SlashCommand {
  name: string;
  prompt: string;
  usageCount: number;
  createdAt: string;
}

interface PatternRecord {
  count: number;
  suggested: boolean;
}

const STORAGE_KEY = "slash_commands";
const PATTERN_KEY = "slash_command_patterns";
const UPDATE_EVENT = "slash-commands-updated";
const SUGGESTION_THRESHOLD = 3;
const MIN_PATTERN_LENGTH = 12;

const normalizeName = (name: string) => name.trim().toLowerCase();

const safeParse = <T>(value: string | null, fallback: T): T => {
  if (!value) return fallback;
  try {
    return JSON.parse(value) as T;
  } catch {
    return fallback;
  }
};

const emitUpdate = () => {
  if (typeof window === "undefined") return;
  window.dispatchEvent(new CustomEvent(UPDATE_EVENT));
};

export const getSlashCommands = (): SlashCommand[] => {
  if (typeof window === "undefined") return [];
  return safeParse<SlashCommand[]>(localStorage.getItem(STORAGE_KEY), []);
};

export const saveSlashCommands = (commands: SlashCommand[]) => {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(commands));
  emitUpdate();
};

export const addSlashCommand = (name: string, prompt: string) => {
  const normalizedName = normalizeName(name);
  const commands = getSlashCommands();
  const existing = commands.find((command) => command.name === normalizedName);

  if (existing) {
    existing.prompt = prompt;
    saveSlashCommands(commands);
    return { command: existing, wasUpdated: true };
  }

  const newCommand: SlashCommand = {
    name: normalizedName,
    prompt,
    usageCount: 0,
    createdAt: new Date().toISOString(),
  };

  saveSlashCommands([...commands, newCommand]);
  return { command: newCommand, wasUpdated: false };
};

export const resolveSlashCommandInput = (message: string) => {
  const trimmed = message.trim();
  const match = /^\/([a-z0-9_-]+)(?:\s+(.*))?$/i.exec(trimmed);
  if (!match) {
    return { resolvedMessage: message, matchedCommand: null };
  }

  const commandName = normalizeName(match[1]);
  const args = match[2];
  const commands = getSlashCommands();
  const command = commands.find((item) => item.name === commandName);

  if (!command) {
    return { resolvedMessage: message, matchedCommand: null };
  }

  command.usageCount += 1;
  saveSlashCommands(commands);

  const resolvedMessage = args
    ? `${command.prompt}\n\n${args}`
    : command.prompt;
  return { resolvedMessage, matchedCommand: command };
};

export const parseSlashCommandCreation = (message: string) => {
  const trimmed = message.trim();
  const match = /^\/slash\s+(add|create)\s+([a-z0-9_-]+)\s*(.*)$/i.exec(
    trimmed,
  );
  if (!match) return null;

  const rawPrompt = match[3] || "";
  const prompt = rawPrompt.includes("::")
    ? rawPrompt.split("::").slice(1).join("::").trim()
    : rawPrompt.trim();

  if (!prompt) return null;

  return { name: match[2], prompt };
};

const normalizePattern = (message: string) =>
  message.trim().replace(/\s+/g, " ").toLowerCase();

const deriveCommandName = (message: string) => {
  const words = normalizePattern(message)
    .replace(/[^a-z0-9\s-]/g, "")
    .split(" ")
    .filter(Boolean)
    .slice(0, 3);
  return words.length > 0 ? words.join("-") : "quick-task";
};

export const recordMessagePattern = (message: string) => {
  const trimmed = message.trim();
  if (!trimmed || trimmed.startsWith("/")) return null;
  if (trimmed.length < MIN_PATTERN_LENGTH) return null;

  if (typeof window === "undefined") return null;
  const patterns = safeParse<Record<string, PatternRecord>>(
    localStorage.getItem(PATTERN_KEY),
    {},
  );

  const normalized = normalizePattern(trimmed);
  const current = patterns[normalized] || { count: 0, suggested: false };
  current.count += 1;
  patterns[normalized] = current;
  localStorage.setItem(PATTERN_KEY, JSON.stringify(patterns));

  if (current.count >= SUGGESTION_THRESHOLD && !current.suggested) {
    current.suggested = true;
    localStorage.setItem(PATTERN_KEY, JSON.stringify(patterns));
    return {
      suggestedName: deriveCommandName(trimmed),
      message: trimmed,
    };
  }

  return null;
};

export const getSlashCommandUpdateEventName = () => UPDATE_EVENT;
