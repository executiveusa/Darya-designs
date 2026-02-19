import { openHands } from "#/api/open-hands-axios";
import {
  ModelPresetActivateRequest,
  ModelPresetResponse,
  ModelPresetState,
} from "#/api/open-hands.types";

class ModelsService {
  static async listPresets(): Promise<ModelPresetResponse> {
    const { data } = await openHands.get<ModelPresetResponse>(
      "/api/models/presets",
    );
    return data;
  }

  static async setActivePreset(
    payload: ModelPresetActivateRequest,
  ): Promise<ModelPresetState> {
    const { data } = await openHands.post<ModelPresetState>(
      "/api/models/presets/active",
      payload,
    );
    return data;
  }
}

export default ModelsService;
