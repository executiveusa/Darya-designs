import React from "react";
import { useTranslation } from "react-i18next";
import {
  useModelPresets,
  useSetActivePreset,
} from "#/hooks/query/use-model-presets";
import { useWorkflows, useRunWorkflow } from "#/hooks/query/use-workflows";
import { useConfig } from "#/hooks/query/use-config";
import { displaySuccessToast } from "#/utils/custom-toast-handlers";
import { cn } from "#/utils/utils";

type SpeechRecognitionResultEventLike = {
  results: ArrayLike<ArrayLike<{ transcript: string }>>;
};

type SpeechRecognitionLike = {
  lang: string;
  onresult: ((event: SpeechRecognitionResultEventLike) => void) | null;
  start: () => void;
};

type SpeechRecognitionCtor = new () => SpeechRecognitionLike;

const PRESET_LABELS: Record<string, string> = {
  fast: "Fast",
  quality: "Quality",
  long: "Long",
  main: "Main",
};

export function ModelPresetSelector() {
  const { data } = useModelPresets();
  const setActive = useSetActivePreset();
  const { data: workflows } = useWorkflows();
  const runWorkflow = useRunWorkflow();
  const config = useConfig();
  const { t } = useTranslation();

  const voiceEnabled = Boolean(
    config.data?.FEATURE_FLAGS.VOICE_ENABLED ?? true,
  );

  const handlePreset = (preset: string) => {
    setActive.mutate({ preset });
    displaySuccessToast(`Switched to ${preset} mode`);
  };

  const handleRunWorkflow = React.useCallback(
    (name: string) => {
      const match = workflows?.find((workflow) =>
        workflow.name.toLowerCase().includes(name.toLowerCase()),
      );
      if (match) {
        runWorkflow.mutate({ workflow_id: match.id, input: {} });
        displaySuccessToast(`Running ${match.name}`);
      }
    },
    [workflows, runWorkflow],
  );

  const handleVoice = React.useCallback(() => {
    const SpeechRecognition =
      (
        window as Window & {
          SpeechRecognition?: SpeechRecognitionCtor;
          webkitSpeechRecognition?: SpeechRecognitionCtor;
        }
      ).SpeechRecognition ||
      (
        window as Window & {
          SpeechRecognition?: SpeechRecognitionCtor;
          webkitSpeechRecognition?: SpeechRecognitionCtor;
        }
      ).webkitSpeechRecognition;
    if (!SpeechRecognition) return;
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.onresult = (event: SpeechRecognitionResultEventLike) => {
      // Add bounds checking for speech recognition results
      const firstResult =
        event.results && event.results.length > 0
          ? event.results[0]
          : undefined;
      if (!firstResult || firstResult.length === 0) return;
      const firstAlternative = firstResult[0];
      if (!firstAlternative || typeof firstAlternative.transcript !== "string")
        return;

      const transcript = firstAlternative.transcript.toLowerCase();
      if (transcript.includes("fast")) handlePreset("fast");
      if (transcript.includes("quality")) handlePreset("quality");
      if (transcript.includes("long")) handlePreset("long");
      if (transcript.includes("run")) {
        const name = transcript.replace("run", "").trim();
        if (name) handleRunWorkflow(name);
      }
    };
    recognition.start();
  }, [handleRunWorkflow]);

  const visiblePresets =
    data?.presets.filter((preset) =>
      ["fast", "quality", "long", "main"].includes(preset.name),
    ) ?? [];

  return (
    <div
      className={cn(
        "flex items-center gap-2 rounded-full border border-white/10",
        "bg-white/5 px-3 py-1 text-xs text-white/70",
        "backdrop-blur",
      )}
    >
      {visiblePresets.map((preset) => (
        <button
          key={preset.name}
          type="button"
          onClick={() => handlePreset(preset.name)}
          className={cn(
            "rounded-full px-2 py-1 text-[11px]",
            data.state.active === preset.name
              ? "bg-white/20 text-white"
              : "hover:bg-white/10",
          )}
        >
          {PRESET_LABELS[preset.name] ?? preset.name}
        </button>
      ))}
      {voiceEnabled && (
        <button
          type="button"
          onClick={handleVoice}
          className="rounded-full border border-white/20 px-2 py-1 text-[11px] hover:bg-white/10"
        >
          {t("Voice")}
        </button>
      )}
    </div>
  );
}
