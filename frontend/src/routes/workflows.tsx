import React from "react";
import { useWorkflows, useRunWorkflow, useWorkflowRun, useApproveWorkflow, useWorkflowArtifacts } from "#/hooks/query/use-workflows";
import { toggleHotpadPin, getHotpadPins } from "#/utils/hotpad";
import { cn } from "#/utils/utils";

export default function WorkflowsRoute() {
  const { data: workflows } = useWorkflows();
  const runWorkflow = useRunWorkflow();
  const [runId, setRunId] = React.useState<string | null>(null);
  const runStatus = useWorkflowRun(runId);
  const artifacts = useWorkflowArtifacts(runId);
  const approve = useApproveWorkflow(runId);
  const [advanced, setAdvanced] = React.useState(false);
  const [pins, setPins] = React.useState<string[]>([]);

  React.useEffect(() => {
    setPins(getHotpadPins());
  }, []);

  const handleRun = (workflowId: string) => {
    runWorkflow.mutate(
      { workflow_id: workflowId, input: {} },
      {
        onSuccess: (data) => {
          setRunId(data.run_id);
        },
      },
    );
  };

  const togglePin = (id: string) => {
    toggleHotpadPin(id);
    setPins(getHotpadPins());
  };

  return (
    <div className="p-6 text-white">
      <div className="mb-6 rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
        <h1 className="text-xl font-semibold">Workflows</h1>
        <p className="text-sm text-white/60">
          Run durable workflows with approvals and artifacts.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-4">
          {workflows?.map((workflow) => (
            <div
              key={workflow.id}
              className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-semibold">{workflow.name}</p>
                  <p className="text-xs text-white/50">{workflow.id}</p>
                </div>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => togglePin(workflow.id)}
                    className={cn(
                      "rounded-full border px-2 py-1 text-xs",
                      pins.includes(workflow.id)
                        ? "border-white/40 text-white"
                        : "border-white/10 text-white/60",
                    )}
                  >
                    {pins.includes(workflow.id) ? "Pinned" : "Pin"}
                  </button>
                  <button
                    type="button"
                    onClick={() => handleRun(workflow.id)}
                    className="rounded-full border border-white/20 px-3 py-1 text-xs text-white/80 hover:bg-white/10"
                  >
                    Run
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
          <div className="flex items-center justify-between">
            <p className="text-sm font-semibold">Run Status</p>
            <button
              type="button"
              onClick={() => setAdvanced((prev) => !prev)}
              className="text-xs text-white/60"
            >
              {advanced ? "Hide details" : "Advanced / Details"}
            </button>
          </div>

          {runStatus.data ? (
            <div className="mt-3 space-y-2 text-xs text-white/70">
              <p>Status: {runStatus.data.status}</p>
              <p>Run ID: {runStatus.data.id}</p>

              {runStatus.data.approvals.length > 0 && (
                <div className="space-y-2">
                  {runStatus.data.approvals.map((approval) => (
                    <div
                      key={approval.id}
                      className="rounded-lg border border-white/10 bg-black/20 p-2"
                    >
                      <p>Approval: {approval.action_type}</p>
                      <p>Status: {approval.status}</p>
                      {approval.status === "pending" && (
                        <button
                          type="button"
                          onClick={() =>
                            approve.mutate({
                              approval_id: approval.id,
                              decision: "approved",
                            })
                          }
                          className="mt-2 rounded-full border border-white/20 px-2 py-1 text-[11px] text-white/80"
                        >
                          Approve
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {advanced && (
                <pre className="whitespace-pre-wrap text-[10px] text-white/60">
                  {JSON.stringify(runStatus.data, null, 2)}
                </pre>
              )}

              <div>
                <p className="text-xs uppercase text-white/50">Artifacts</p>
                {artifacts.data?.map((artifact) => (
                  <p key={artifact.id} className="text-[11px] text-white/70">
                    {artifact.path}
                  </p>
                ))}
              </div>
            </div>
          ) : (
            <p className="mt-3 text-xs text-white/50">No runs yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}
