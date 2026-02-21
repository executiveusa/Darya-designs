import { Layers } from "lucide-react";
import { TooltipButton } from "./tooltip-button";

interface WorkflowsButtonProps {
  disabled?: boolean;
}

export function WorkflowsButton({ disabled = false }: WorkflowsButtonProps) {
  return (
    <TooltipButton
      tooltip="Workflows"
      ariaLabel="Workflows"
      navLinkTo="/workflows"
      testId="workflows-button"
      disabled={disabled}
    >
      <Layers size={24} />
    </TooltipButton>
  );
}
