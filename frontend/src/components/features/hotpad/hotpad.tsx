import React from "react";
import { useWorkflows, useRunWorkflow } from "#/hooks/query/use-workflows";
import { getHotpadPins } from "#/utils/hotpad";
import { cn } from "#/utils/utils";

export function Hotpad() {
  const { data: workflows } = useWorkflows();
  const runWorkflow = useRunWorkflow();
  const [pins, setPins] = React.useState<string[]>([]);
  const [expanded, setExpanded] = React.useState(false);

  React.useEffect(() => {
    setPins(getHotpadPins());
  }, []);

  const pinnedWorkflows = workflows?.filter((workflow) =>
    pins.includes(workflow.id),
  );

  if (!pinnedWorkflows?.length) {
    return null;
  }

  return (
    <div
      className={cn(
        "rounded-2xl border border-white/10 bg-white/5 px-4 py-2",
        "backdrop-blur-xl text-xs text-white/70",
      )}
    >
      <div className="flex items-center justify-between">
        <span className="uppercase tracking-[0.2em] text-white/50">
          Hotpad
        </span>
        <button
          type="button"
          onClick={() => setExpanded((prev) => !prev)}
          className="text-[10px] uppercase text-white/60"
        >
          {expanded ? "Hide" : "Show"}
        </button>
      </div>
      {expanded && (
        <div className="mt-2 flex flex-wrap gap-2">
          {pinnedWorkflows.map((workflow) => (
            <button
              key={workflow.id}
              type="button"
              onClick={() =>
                runWorkflow.mutate({ workflow_id: workflow.id, input: {} })
              }
              className="rounded-full border border-white/20 px-3 py-1 text-[11px] text-white/80 hover:bg-white/10"
            >
              {workflow.name}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
