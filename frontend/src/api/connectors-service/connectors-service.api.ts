import { openHands } from "#/api/open-hands-axios";
import { ConnectorConnectRequest, ConnectorInfo } from "#/api/open-hands.types";

class ConnectorsService {
  static async listConnectors(): Promise<ConnectorInfo[]> {
    const { data } = await openHands.get<ConnectorInfo[]>("/api/connectors");
    return data;
  }

  static async connectConnector(
    payload: ConnectorConnectRequest,
  ): Promise<ConnectorInfo> {
    const { data } = await openHands.post<ConnectorInfo>(
      "/api/connectors/connect",
      payload,
    );
    return data;
  }

  static async status(): Promise<ConnectorInfo[]> {
    const { data } = await openHands.get<ConnectorInfo[]>(
      "/api/connectors/status",
    );
    return data;
  }
}

export default ConnectorsService;
