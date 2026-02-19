import { Provider } from "#/types/settings";

export interface GetConfigResponse {
  APP_MODE: "saas" | "oss";
  APP_SLUG?: string;
  GITHUB_CLIENT_ID: string;
  POSTHOG_CLIENT_KEY: string;
  PUBLIC_APP_NAME?: string;
  PUBLIC_DEFAULT_MODEL?: string;
  PROVIDERS_CONFIGURED?: Provider[];
  AUTH_URL?: string;
  FEATURE_FLAGS: {
    ENABLE_BILLING: boolean;
    HIDE_LLM_SETTINGS: boolean;
    ENABLE_JIRA: boolean;
    ENABLE_JIRA_DC: boolean;
    ENABLE_LINEAR: boolean;
    VOICE_ENABLED?: boolean;
    COST_VISIBILITY?: boolean;
  };
  MAINTENANCE?: {
    startTime: string;
  };
}

export interface WebClientFeatureFlags {
  enable_billing: boolean;
  hide_llm_settings: boolean;
  enable_jira: boolean;
  enable_jira_dc: boolean;
  enable_linear: boolean;
}

export interface WebClientConfig {
  app_mode: "saas" | "oss";
  posthog_client_key: string | null;
  feature_flags: WebClientFeatureFlags;
  providers_configured: Provider[];
  maintenance_start_time: string | null;
  auth_url: string | null;
  recaptcha_site_key: string | null;
  faulty_models: string[];
  error_message: string | null;
  updated_at: string;
  github_app_slug: string | null;
}
