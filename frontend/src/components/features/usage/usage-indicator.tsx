import React from "react";
import { useParams } from "react-router";
import { useTranslation } from "react-i18next";
import { useCurrentUsage } from "#/hooks/query/use-current-usage";
import { useConfig } from "#/hooks/query/use-config";
import { I18nKey } from "#/i18n/declaration";
import { cn } from "#/utils/utils";

interface UsageIndicatorProps {
  defaultModel?: string;
}

export function UsageIndicator({ defaultModel }: UsageIndicatorProps) {
  const { conversationId } = useParams<{ conversationId: string }>();
  const { data } = useCurrentUsage();
  const config = useConfig();
  const { t } = useTranslation();

  React.useEffect(() => {
    if (conversationId) {
      sessionStorage.setItem("session_id", conversationId);
    }
  }, [conversationId]);

  if (!conversationId || config.data?.FEATURE_FLAGS.COST_VISIBILITY === false) {
    return null;
  }

  const model = data?.model || defaultModel || "unknown";
  const tokens = data?.total_tokens ?? 0;
  const cost = (data?.accumulated_cost ?? 0).toFixed(4);

  return (
    <div
      className={cn(
        "w-full px-4 py-2 text-xs text-muted-foreground",
        "border-b border-base-700 bg-base",
      )}
    >
      {t(I18nKey.USAGE$INDICATOR, { model, tokens, cost })}
    </div>
  );
}
