import { ConversationStatus } from "#/types/conversation-status";
import { RuntimeStatus } from "#/types/runtime-status";
import { Provider } from "#/types/settings";

export interface ErrorResponse {
  error: string;
}

export interface SaveFileSuccessResponse {
  message: string;
}

export interface FileUploadSuccessResponse {
  uploaded_files: string[];
  skipped_files: { name: string; reason: string }[];
}

export interface FeedbackBodyResponse {
  message: string;
  feedback_id: string;
  password: string;
}

export interface FeedbackResponse {
  statusCode: number;
  body: FeedbackBodyResponse;
}

export interface AuthenticationResponse {
  message: string;
  login?: string; // Only present when allow list is enabled
}

export interface Feedback {
  version: string;
  email: string;
  token: string;
  polarity: "positive" | "negative";
  permissions: "public" | "private";
  trajectory: unknown[];
}

export interface GetVSCodeUrlResponse {
  vscode_url: string | null;
  error?: string;
}

export interface GetTrajectoryResponse {
  trajectory: unknown[] | null;
  error?: string;
}

export interface RepositorySelection {
  selected_repository: string | null;
  selected_branch: string | null;
  git_provider: Provider | null;
}

export type ConversationTrigger =
  | "resolver"
  | "gui"
  | "suggested_task"
  | "microagent_management";

export interface Conversation {
  conversation_id: string;
  title: string;
  selected_repository: string | null;
  selected_branch: string | null;
  git_provider: Provider | null;
  last_updated_at: string;
  created_at: string;
  status: ConversationStatus;
  runtime_status: RuntimeStatus | null;
  trigger?: ConversationTrigger;
  url: string | null;
  session_api_key: string | null;
  pr_number?: number[] | null;
  conversation_version?: "V0" | "V1";
}

export interface ResultSet<T> {
  results: T[];
  next_page_id: string | null;
}

export type GitChangeStatus = "M" | "A" | "D" | "R" | "U";

export interface GitChange {
  status: GitChangeStatus;
  path: string;
}

export interface GitChangeDiff {
  modified: string;
  original: string;
}

export interface InputMetadata {
  name: string;
  description: string;
}

export interface Microagent {
  name: string;
  type: "repo" | "knowledge";
  content: string;
  triggers: string[];
}

export interface GetMicroagentsResponse {
  microagents: Microagent[];
}

export interface GetMicroagentPromptResponse {
  status: string;
  prompt: string;
}

export interface UsageCurrentResponse {
  model: string;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  accumulated_cost: number;
  updated_at: string;
}

export interface ModelPreset {
  name: string;
  model: string;
}

export interface ModelPresetState {
  active: string;
  updated_at: string;
}

export interface ModelPresetResponse {
  presets: ModelPreset[];
  state: ModelPresetState;
}

export interface ModelPresetActivateRequest {
  preset: string;
}

export interface Workflow {
  id: string;
  name: string;
  schema: {
    name: string;
    steps: Record<string, unknown>[];
  };
  created_at: string;
}

export interface WorkflowRunResponse {
  run_id: string;
}

export interface WorkflowApproval {
  id: string;
  action_type: string;
  payload_hash: string;
  status: string;
  decided_by?: string | null;
  decided_at?: string | null;
}

export interface WorkflowRunStatus {
  id: string;
  workflow_id: string;
  status: string;
  current_step: number;
  created_at: string;
  updated_at: string;
  approvals: WorkflowApproval[];
}

export interface WorkflowArtifact {
  id: string;
  path: string;
  type: string;
  created_at: string;
}

export interface WorkflowRunRequest {
  workflow_id: string;
  input: Record<string, unknown>;
}

export interface WorkflowApprovalRequest {
  approval_id: string;
  decision: string;
  decided_by?: string;
}

export interface ConnectorInfo {
  id: string;
  name: string;
  status: string;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface ConnectorConnectRequest {
  name: string;
  payload: Record<string, unknown>;
}

export interface IOption<T> {
  label: string;
  value: T;
}

export interface CreateMicroagent {
  repo: string;
  git_provider?: Provider;
  title?: string;
}

export interface MicroagentContentResponse {
  content: string;
  path: string;
  git_provider: Provider;
  triggers: string[];
}

export type GetFilesResponse = string[];

export interface GetFileResponse {
  code: string;
}
