import React from "react";
import { useConnectors, useConnectorStatus, useConnectConnector } from "#/hooks/query/use-connectors";
import { cn } from "#/utils/utils";

export default function ConnectorsRoute() {
  const { data: connectors } = useConnectors();
  const { data: status } = useConnectorStatus();
  const connect = useConnectConnector();

  const handleConnect = (name: string) => {
    connect.mutate({ name, payload: {} });
  };

  return (
    <div className="p-6 text-white">
      <div className="mb-6 rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
        <h1 className="text-xl font-semibold">Connectors</h1>
        <p className="text-sm text-white/60">
          Connect MCP tools with read-only defaults and approval gates.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-4">
          {connectors?.map((connector) => (
            <div
              key={connector.id}
              className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-semibold">{connector.name}</p>
                  <p className="text-xs text-white/50">{connector.status}</p>
                </div>
                <button
                  type="button"
                  onClick={() => handleConnect(connector.name)}
                  className="rounded-full border border-white/20 px-3 py-1 text-xs text-white/80 hover:bg-white/10"
                >
                  Connect
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
          <p className="text-sm font-semibold">Connected</p>
          <div className="mt-3 space-y-2 text-xs text-white/70">
            {status?.map((connector) => (
              <div
                key={connector.id}
                className={cn(
                  "rounded-lg border border-white/10 bg-black/20 p-2",
                )}
              >
                <p>{connector.name}</p>
                <p>Status: {connector.status}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
