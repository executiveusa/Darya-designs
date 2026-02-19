import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import WorkflowsService from "#/api/workflows-service/workflows-service.api";
import {
  WorkflowApprovalRequest,
  WorkflowRunRequest,
} from "#/api/open-hands.types";

export function useWorkflows() {
  return useQuery({
    queryKey: ["workflows"],
    queryFn: () => WorkflowsService.listWorkflows(),
  });
}

export function useRunWorkflow() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: WorkflowRunRequest) =>
      WorkflowsService.runWorkflow(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workflow-runs"] });
    },
  });
}

export function useWorkflowRun(runId: string | null) {
  return useQuery({
    queryKey: ["workflow-run", runId],
    queryFn: () => WorkflowsService.getRun(runId || ""),
    enabled: Boolean(runId),
    refetchInterval: 2000,
  });
}

export function useWorkflowArtifacts(runId: string | null) {
  return useQuery({
    queryKey: ["workflow-artifacts", runId],
    queryFn: () => WorkflowsService.listArtifacts(runId || ""),
    enabled: Boolean(runId),
  });
}

export function useApproveWorkflow(runId: string | null) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: WorkflowApprovalRequest) =>
      WorkflowsService.approveRun(runId || "", payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workflow-run", runId] });
      queryClient.invalidateQueries({ queryKey: ["workflow-artifacts", runId] });
    },
  });
}
