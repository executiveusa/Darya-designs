import { useCallback } from "react";
import { useTranslation } from "react-i18next";
import {
  clearTextContent,
  clearFileInput,
} from "#/components/features/chat/utils/chat-input.utils";
import { I18nKey } from "#/i18n/declaration";
import { displaySuccessToast } from "#/utils/custom-toast-handlers";
import {
  addSlashCommand,
  parseSlashCommandCreation,
  recordMessagePattern,
  resolveSlashCommandInput,
} from "#/utils/slash-commands";

/**
 * Hook for handling chat message submission
 */
export const useChatSubmission = (
  chatInputRef: React.RefObject<HTMLDivElement | null>,
  fileInputRef: React.RefObject<HTMLInputElement | null>,
  smartResize: () => void,
  onSubmit: (message: string) => void,
  resetManualResize?: () => void,
) => {
  const { t } = useTranslation();
  // Send button click handler
  const handleSubmit = useCallback(() => {
    const message = chatInputRef.current?.innerText || "";
    const trimmedMessage = message.trim();

    if (!trimmedMessage) {
      return;
    }

    const creation = parseSlashCommandCreation(trimmedMessage);
    if (creation) {
      const { command, wasUpdated } = addSlashCommand(
        creation.name,
        creation.prompt,
      );
      displaySuccessToast(
        wasUpdated
          ? t(I18nKey.SLASH_COMMANDS$UPDATED, { name: command.name })
          : t(I18nKey.SLASH_COMMANDS$CREATED, { name: command.name }),
      );
      clearTextContent(chatInputRef.current);
      clearFileInput(fileInputRef.current);
      smartResize();
      resetManualResize?.();
      return;
    }

    const suggestion = recordMessagePattern(trimmedMessage);
    if (suggestion) {
      displaySuccessToast(
        t(I18nKey.SLASH_COMMANDS$SUGGESTION, {
          name: suggestion.suggestedName,
        }),
      );
    }

    const resolved = resolveSlashCommandInput(trimmedMessage);
    onSubmit(resolved.resolvedMessage);

    // Clear the input
    clearTextContent(chatInputRef.current);
    clearFileInput(fileInputRef.current);

    // Reset height and show suggestions again
    smartResize();

    // Reset manual resize state for next message
    resetManualResize?.();
  }, [chatInputRef, fileInputRef, smartResize, onSubmit, resetManualResize, t]);

  // Resume agent button click handler
  const handleResumeAgent = useCallback(() => {
    const message = chatInputRef.current?.innerText || "continue";

    onSubmit(message.trim());

    // Clear the input
    clearTextContent(chatInputRef.current);
    clearFileInput(fileInputRef.current);

    // Reset height and show suggestions again
    smartResize();

    // Reset manual resize state for next message
    resetManualResize?.();
  }, [chatInputRef, fileInputRef, smartResize, onSubmit, resetManualResize]);

  // Handle stop button click
  const handleStop = useCallback((onStop?: () => void) => {
    if (onStop) {
      onStop();
    }
  }, []);

  return {
    handleSubmit,
    handleResumeAgent,
    handleStop,
  };
};
