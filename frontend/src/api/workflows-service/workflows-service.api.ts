import { openHands } from "#/api/open-hands-axios";
import {
  Workflow,
  WorkflowArtifact,
  WorkflowApprovalRequest,
  WorkflowRunRequest,
  WorkflowRunResponse,
  WorkflowRunStatus,
} from "#/api/open-hands.types";

class WorkflowsService {
  static async listWorkflows(): Promise<Workflow[]> {
    const { data } = await openHands.get<Workflow[]>("/api/workflows");
    return data;
  }

  static async runWorkflow(
    payload: WorkflowRunRequest,
  ): Promise<WorkflowRunResponse> {
    const { data } = await openHands.post<WorkflowRunResponse>(
      "/api/workflows/run",
      payload,
    );
    return data;
  }

  static async getRun(runId: string): Promise<WorkflowRunStatus> {
    const { data } = await openHands.get<WorkflowRunStatus>(
      `/api/workflows/run/${runId}`,
    );
    return data;
  }

  static async listArtifacts(runId: string): Promise<WorkflowArtifact[]> {
    const { data } = await openHands.get<WorkflowArtifact[]>(
      `/api/workflows/run/${runId}/artifacts`,
    );
    return data;
  }

  static async approveRun(
    runId: string,
    payload: WorkflowApprovalRequest,
  ): Promise<WorkflowRunStatus> {
    const { data } = await openHands.post<WorkflowRunStatus>(
      `/api/workflows/run/${runId}/approve`,
      payload,
    );
    return data;
  }
}

export default WorkflowsService;
