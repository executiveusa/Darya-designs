import { describe, expect, it, beforeEach } from "vitest";
import {
  addSlashCommand,
  getSlashCommands,
  parseSlashCommandCreation,
  recordMessagePattern,
  resolveSlashCommandInput,
} from "../slash-commands";

describe("slash-commands utils", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("adds and resolves a slash command", () => {
    addSlashCommand("build", "Run build pipeline");

    const commands = getSlashCommands();
    expect(commands).toHaveLength(1);
    expect(commands[0].name).toBe("build");

    const resolved = resolveSlashCommandInput("/build now");
    expect(resolved.matchedCommand?.name).toBe("build");
    expect(resolved.resolvedMessage).toContain("Run build pipeline");
    expect(resolved.resolvedMessage).toContain("now");
  });

  it("parses slash command creation", () => {
    const parsed = parseSlashCommandCreation(
      "/slash add deploy :: deploy the service",
    );
    expect(parsed).toEqual({ name: "deploy", prompt: "deploy the service" });
  });

  it("suggests command after repeated prompts", () => {
    const message = "Generate a release checklist for this repo";
    expect(recordMessagePattern(message)).toBeNull();
    expect(recordMessagePattern(message)).toBeNull();
    const suggestion = recordMessagePattern(message);
    expect(suggestion?.suggestedName).toBeDefined();
  });
});
