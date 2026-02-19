import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router";
import ConversationService from "#/api/conversation-service/conversation-service.api";

export const useCurrentUsage = () => {
  const { conversationId } = useParams<{ conversationId: string }>();

  return useQuery({
    queryKey: ["usage", conversationId],
    queryFn: () => ConversationService.getCurrentUsage(conversationId!),
    enabled: Boolean(conversationId),
    // Reduced from 1.5s to 5s to reduce backend load
    refetchInterval: 5000,
  });
};
