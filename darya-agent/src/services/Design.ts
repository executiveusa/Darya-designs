import { Anthropic } from '@anthropic-ai/sdk';
import { Logger } from 'winston';
import { z } from 'zod';

/**
 * Design Strategy schema for validation
 */
const DesignStrategySchema = z.object({
  projectName: z.string(),
  briefAnalysis: z.string(),
  designPrinciples: z.array(z.string()),
  colorPalette: z.array(z.string()),
  typography: z.object({
    primary: z.string(),
    secondary: z.string(),
  }),
  layoutRecommendations: z.string(),
  componentSuggestions: z.array(z.string()),
  accessibility: z.string(),
  performanceNotes: z.string(),
  estimatedHours: z.number(),
});

export type DesignStrategy = z.infer<typeof DesignStrategySchema>;

interface DesignAnalysisInput {
  projectName: string;
  brief: string;
  targetAudience: string;
  brandGuide?: string;
  constraints?: string[];
}

/**
 * Design Analysis Engine
 * Analyzes design briefs and generates recommendations using Claude API
 */
export class DesignAnalyzer {
  private client: Anthropic;
  private logger: Logger;

  constructor(logger: Logger) {
    this.client = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });
    this.logger = logger;
  }

  /**
   * Analyze a design brief and return comprehensive strategy
   */
  async analyzeBrief(input: DesignAnalysisInput): Promise<DesignStrategy> {
    try {
      this.logger.info('Analyzing design brief', { projectName: input.projectName });

      const prompt = this.buildAnalysisPrompt(input);

      const message = await this.client.messages.create({
        model: 'claude-3-5-haiku-20241022',
        max_tokens: 2048,
        messages: [
          {
            role: 'user',
            content: prompt,
          },
        ],
      });

      const responseText = this.extractTextContent(message);
      const strategy = this.parseDesignStrategy(responseText, input.projectName);

      this.logger.info('Design brief analyzed successfully', {
        projectName: input.projectName,
      });

      return strategy;
    } catch (error) {
      this.logger.error('Failed to analyze design brief', { error, projectName: input.projectName });
      throw error;
    }
  }

  /**
   * Generate design recommendations based on analysis
   */
  async generateRecommendations(strategy: DesignStrategy): Promise<{
    recommendations: string[];
    nextSteps: string[];
  }> {
    try {
      this.logger.info('Generating design recommendations', {
        projectName: strategy.projectName,
      });

      const prompt = `Based on this design strategy:
${JSON.stringify(strategy, null, 2)}

Generate 5 specific, actionable design recommendations and 3 next steps for implementation.`;

      const message = await this.client.messages.create({
        model: 'claude-3-5-haiku-20241022',
        max_tokens: 1024,
        messages: [
          {
            role: 'user',
            content: prompt,
          },
        ],
      });

      const responseText = this.extractTextContent(message);
      const { recommendations, nextSteps } = this.parseRecommendations(responseText);

      return { recommendations, nextSteps };
    } catch (error) {
      this.logger.error('Failed to generate recommendations', { error });
      throw error;
    }
  }

  /**
   * Private helper: Build analysis prompt
   */
  private buildAnalysisPrompt(input: DesignAnalysisInput): string {
    return `You are an expert design strategist. Analyze the following design brief and provide a comprehensive design strategy in JSON format.

Project Name: ${input.projectName}
Design Brief: ${input.brief}
Target Audience: ${input.targetAudience}
${input.brandGuide ? `Brand Guide: ${input.brandGuide}` : ''}
${input.constraints?.length ? `Constraints: ${input.constraints.join(', ')}` : ''}

Provide a JSON response with these exact fields:
{
  "projectName": "string",
  "briefAnalysis": "string - detailed analysis of the brief",
  "designPrinciples": ["string - array of 3-5 design principles"],
  "colorPalette": ["string - array of 4-6 hex colors"],
  "typography": {
    "primary": "string - primary font recommendation",
    "secondary": "string - secondary font recommendation"
  },
  "layoutRecommendations": "string - specific layout suggestions",
  "componentSuggestions": ["string - array of 5-8 suggested components"],
  "accessibility": "string - accessibility considerations",
  "performanceNotes": "string - performance optimization notes",
  "estimatedHours": "number - estimated hours for implementation"
}

Return ONLY the JSON object, no additional text.`;
  }

  /**
   * Private helper: Extract text content from API message
   */
  private extractTextContent(message: any): string {
    if (Array.isArray(message.content) && message.content.length > 0) {
      const textBlock = message.content.find((block: any) => block.type === 'text');
      return textBlock?.text || '';
    }
    return '';
  }

  /**
   * Private helper: Parse design strategy from response
   */
  private parseDesignStrategy(responseText: string, projectName: string): DesignStrategy {
    try {
      const jsonMatch = responseText.match(/\{[\s\S]*\}/);
      if (!jsonMatch) {
        throw new Error('No JSON found in response');
      }

      const parsed = JSON.parse(jsonMatch[0]);
      return DesignStrategySchema.parse(parsed);
    } catch (error) {
      this.logger.warn('Failed to parse design strategy, returning defaults', { error });
      return this.getDefaultStrategy(projectName);
    }
  }

  /**
   * Private helper: Parse recommendations from response
   */
  private parseRecommendations(
    responseText: string,
  ): { recommendations: string[]; nextSteps: string[] } {
    const recommendationsMatch = responseText.match(/Recommendations?:?([\s\S]*?)(?:Next Steps|Implementation|$)/i);
    const nextStepsMatch = responseText.match(/Next Steps?:?([\s\S]*?)$/i);

    const recommendations = recommendationsMatch
      ? recommendationsMatch[1]
          .split('\n')
          .filter((line) => line.trim().match(/^[-•*]/))
          .map((line) => line.replace(/^[-•*]\s*/, '').trim())
          .filter((line) => line.length > 0)
      : [];

    const nextSteps = nextStepsMatch
      ? nextStepsMatch[1]
          .split('\n')
          .filter((line) => line.trim().match(/^[-•*]/))
          .map((line) => line.replace(/^[-•*]\s*/, '').trim())
          .filter((line) => line.length > 0)
      : [];

    return { recommendations, nextSteps };
  }

  /**
   * Private helper: Get default strategy
   */
  private getDefaultStrategy(projectName: string): DesignStrategy {
    return {
      projectName,
      briefAnalysis: 'Design brief analysis pending',
      designPrinciples: ['Clarity', 'Consistency', 'User-Centered'],
      colorPalette: ['#1F2937', '#3B82F6', '#10B981', '#F59E0B', '#EF4444'],
      typography: {
        primary: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
        secondary: 'Georgia, serif',
      },
      layoutRecommendations: 'Grid-based layout with responsive breakpoints',
      componentSuggestions: ['Hero Section', 'Feature Cards', 'Navigation', 'Footer', 'CTA Buttons'],
      accessibility: 'WCAG 2.1 AA compliant with proper contrast ratios',
      performanceNotes: 'Optimize images and implement lazy loading',
      estimatedHours: 40,
    };
  }
}
