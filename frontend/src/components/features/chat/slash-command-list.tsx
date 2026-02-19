import React from "react";
import { useTranslation } from "react-i18next";
import { I18nKey } from "#/i18n/declaration";
import { useConversationStore } from "#/state/conversation-store";
import { cn } from "#/utils/utils";
import {
  getSlashCommandUpdateEventName,
  getSlashCommands,
  SlashCommand,
} from "#/utils/slash-commands";

export function SlashCommandList() {
  const { t } = useTranslation();
  const { setMessageToSend } = useConversationStore();
  const [commands, setCommands] = React.useState<SlashCommand[]>([]);

  React.useEffect(() => {
    setCommands(getSlashCommands());

    const updateCommands = () => setCommands(getSlashCommands());
    const updateEvent = getSlashCommandUpdateEventName();

    window.addEventListener("storage", updateCommands);
    window.addEventListener(updateEvent, updateCommands as EventListener);

    return () => {
      window.removeEventListener("storage", updateCommands);
      window.removeEventListener(updateEvent, updateCommands as EventListener);
    };
  }, []);

  if (commands.length === 0) {
    return null;
  }

  return (
    <div className="flex flex-col gap-2 rounded-md border border-base-700 bg-base px-3 py-2">
      <span className="text-xs uppercase tracking-wide text-muted-foreground">
        {t(I18nKey.SLASH_COMMANDS$TITLE)}
      </span>
      <div className="flex flex-wrap gap-2">
        {commands.map((command) => (
          <button
            key={command.name}
            type="button"
            className={cn(
              "text-xs text-white border border-base-600 rounded px-2 py-1",
              "hover:bg-base-700 transition",
            )}
            onClick={() => setMessageToSend(`/${command.name}`)}
          >
            /{command.name}
          </button>
        ))}
      </div>
    </div>
  );
}
