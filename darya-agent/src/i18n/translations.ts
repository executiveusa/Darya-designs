/**
 * i18n Translations Manager
 * Bilingual support for English and Spanish
 */

import enTranslations from './en.json' assert { type: 'json' };
import esTranslations from './es.json' assert { type: 'json' };

type Language = 'en' | 'es';
type TranslationKeys = typeof enTranslations;

/**
 * Translations Manager
 * Provides bilingual support for the Darya Design Wizard application
 */
export class TranslationManager {
  private currentLanguage: Language = 'en';
  private translations: Record<Language, typeof enTranslations> = {
    en: enTranslations,
    es: esTranslations,
  };

  /**
   * Set the current language
   */
  setLanguage(language: Language): void {
    if (this.translations[language]) {
      this.currentLanguage = language;
    } else {
      console.warn(`Language ${language} not supported, defaulting to English`);
      this.currentLanguage = 'en';
    }
  }

  /**
   * Get the current language
   */
  getLanguage(): Language {
    return this.currentLanguage;
  }

  /**
   * Get a translation by key path (e.g., 'app.name' or 'navigation.home')
   */
  t(key: string, defaultValue?: string): string {
    const keys = key.split('.');
    let value: any = this.translations[this.currentLanguage];

    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k];
      } else {
        return defaultValue || key;
      }
    }

    return typeof value === 'string' ? value : defaultValue || key;
  }

  /**
   * Get multiple translations
   */
  tMultiple(keys: string[]): Record<string, string> {
    return keys.reduce(
      (acc, key) => {
        acc[key] = this.t(key);
        return acc;
      },
      {} as Record<string, string>,
    );
  }

  /**
   * Get all translations for current language
   */
  getAll(): typeof enTranslations {
    return this.translations[this.currentLanguage];
  }

  /**
   * Get available languages
   */
  getAvailableLanguages(): Language[] {
    return Object.keys(this.translations) as Language[];
  }

  /**
   * Add or override a translation
   */
  addTranslation(language: Language, key: string, value: string): void {
    const keys = key.split('.');
    let obj: any = this.translations[language];

    for (let i = 0; i < keys.length - 1; i++) {
      if (!(keys[i] in obj)) {
        obj[keys[i]] = {};
      }
      obj = obj[keys[i]];
    }

    obj[keys[keys.length - 1]] = value;
  }

  /**
   * Export translations for a language
   */
  export(language: Language): string {
    return JSON.stringify(this.translations[language], null, 2);
  }
}

// Create singleton instance
export const i18n = new TranslationManager();

// Type definitions for better IDE support
export interface Translations {
  app: {
    name: string;
    tagline: string;
  };
  navigation: {
    home: string;
    dashboard: string;
    projects: string;
    trends: string;
    animations: string;
    settings: string;
    logout: string;
  };
  dashboard: {
    title: string;
    welcome: string;
    subtitle: string;
    metrics: string;
    recentProjects: string;
    trendingNow: string;
    quickActions: string;
    createProject: string;
    browseTrends: string;
    viewAnalytics: string;
  };
  projects: {
    title: string;
    newProject: string;
    projectName: string;
    description: string;
    targetAudience: string;
    status: string;
    created: string;
    estimatedHours: string;
    statusDraft: string;
    statusInProgress: string;
    statusReview: string;
    statusCompleted: string;
    statusArchived: string;
    noProjects: string;
    deleteProject: string;
    viewDetails: string;
    editProject: string;
  };
  design: {
    title: string;
    analyzeBrief: string;
    brief: string;
    designPrinciples: string;
    colorPalette: string;
    typography: string;
    primary: string;
    secondary: string;
    layoutRecommendations: string;
    componentSuggestions: string;
    accessibility: string;
    performanceNotes: string;
    estimatedHours: string;
    analyzing: string;
    analyzed: string;
  };
  trends: {
    title: string;
    trendingTopics: string;
    viralPotential: string;
    colorTrends: string;
    typographyTrends: string;
    patternTrends: string;
    marketInsight: string;
    growthRate: string;
    trendScore: string;
    low: string;
    medium: string;
    high: string;
    trendingColorsTitle: string;
    trendingColorDescription: string;
    trendingTypographyTitle: string;
    trendingTypographyDescription: string;
  };
  animations: {
    title: string;
    generateAnimation: string;
    elementType: string;
    duration: string;
    intensity: string;
    useVR: string;
    gsap: string;
    framerMotion: string;
    hybrid: string;
    subtle: string;
    moderate: string;
    dramatic: string;
    optimizeForPerformance: string;
    generatingAnimation: string;
    animationGenerated: string;
  };
  components: {
    title: string;
    generateComponents: string;
    selectTypes: string;
    button: string;
    card: string;
    input: string;
    navigation: string;
    hero: string;
    footer: string;
    form: string;
    modal: string;
  };
  common: {
    save: string;
    cancel: string;
    delete: string;
    edit: string;
    export: string;
    import: string;
    download: string;
    upload: string;
    close: string;
    loading: string;
    error: string;
    success: string;
    warning: string;
    info: string;
    confirmDelete: string;
    confirmAction: string;
    yes: string;
    no: string;
  };
  errors: {
    invalidInput: string;
    serverError: string;
    notFound: string;
    unauthorized: string;
    networkError: string;
    pleaseRetry: string;
  };
  messages: {
    projectCreated: string;
    projectUpdated: string;
    projectDeleted: string;
    analysisComplete: string;
    exportSuccess: string;
    importSuccess: string;
  };
}
