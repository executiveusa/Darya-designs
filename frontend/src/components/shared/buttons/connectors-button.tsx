import { TooltipButton } from "./tooltip-button";
import { Plug } from "lucide-react";

interface ConnectorsButtonProps {
  disabled?: boolean;
}

export function ConnectorsButton({ disabled = false }: ConnectorsButtonProps) {
  return (
    <TooltipButton
      tooltip="Connectors"
      ariaLabel="Connectors"
      navLinkTo="/connectors"
      testId="connectors-button"
      disabled={disabled}
    >
      <Plug size={24} />
    </TooltipButton>
  );
}
