import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import ConnectorsService from "#/api/connectors-service/connectors-service.api";
import { ConnectorConnectRequest } from "#/api/open-hands.types";

export function useConnectors() {
  return useQuery({
    queryKey: ["connectors"],
    queryFn: () => ConnectorsService.listConnectors(),
  });
}

export function useConnectorStatus() {
  return useQuery({
    queryKey: ["connector-status"],
    queryFn: () => ConnectorsService.status(),
  });
}

export function useConnectConnector() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: ConnectorConnectRequest) =>
      ConnectorsService.connectConnector(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["connectors"] });
      queryClient.invalidateQueries({ queryKey: ["connector-status"] });
    },
  });
}
