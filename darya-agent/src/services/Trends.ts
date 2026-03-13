import axios, { AxiosInstance } from 'axios';
import { Logger } from 'winston';
import { z } from 'zod';

/**
 * Trend insights schema for validation
 */
const TrendInsightSchema = z.object({
  topic: z.string(),
  trendingScore: z.number().min(0).max(100),
  viralPotential: z.string().enum(['low', 'medium', 'high']),
  relatedTopics: z.array(z.string()),
  colorTrends: z.array(z.object({ color: z.string(), trend: z.string() })),
  typographyTrends: z.array(z.string()),
  patternTrends: z.array(z.string()),
  growthRate: z.number(),
  marketInsight: z.string(),
});

export type TrendInsight = z.infer<typeof TrendInsightSchema>;

/**
 * Trends Service
 * Fetches and analyzes trending topics, colors, and typography
 */
export class TrendsService {
  private httpClient: AxiosInstance;
  private logger: Logger;
  private googleTrendsApiUrl = 'https://www.google.com/trends/api/trends/home/overview/feed';
  private colorTrendsCache: Map<string, TrendInsight> = new Map();
  private cacheExpiry: number = 3600000; // 1 hour

  constructor(logger: Logger) {
    this.logger = logger;
    this.httpClient = axios.create({
      timeout: 10000,
      headers: {
        'User-Agent':
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      },
    });
  }

  /**
   * Fetch trending topics from Google Trends
   */
  async getTrendingTopics(regionCode: string = 'US', category: string = 'all'): Promise<any[]> {
    try {
      this.logger.info('Fetching trending topics', { regionCode, category });

      // Note: Direct Google Trends API requires authentication
      // This is a simulated response with realistic data structure
      const trendingTopics = await this.fetchTrendingData(regionCode, category);

      this.logger.info('Trending topics fetched successfully', {
        count: trendingTopics.length,
      });

      return trendingTopics;
    } catch (error) {
      this.logger.error('Failed to fetch trending topics', { error, regionCode });
      return this.getDefaultTrendingTopics();
    }
  }

  /**
   * Analyze viral potential of a topic
   */
  async analyzeViralPotential(topic: string): Promise<{
    score: number;
    viralPotential: 'low' | 'medium' | 'high';
    analysis: string;
  }> {
    try {
      this.logger.info('Analyzing viral potential', { topic });

      const score = await this.calculateTrendScore(topic);
      const viralPotential = this.scoreToViralLevel(score);
      const analysis = this.generateViralAnalysis(topic, score);

      return { score, viralPotential, analysis };
    } catch (error) {
      this.logger.error('Failed to analyze viral potential', { error, topic });
      throw error;
    }
  }

  /**
   * Get trending colors with their market insight
   */
  async getTrendingColors(): Promise<
    Array<{
      color: string;
      colorName: string;
      trend: string;
      industry: string;
      viralScore: number;
    }>
  > {
    try {
      this.logger.info('Fetching trending colors');

      const trendingColors = [
        {
          color: '#FF6B6B',
          colorName: 'Energetic Red',
          trend: 'Bold and assertive brand identities',
          industry: 'Tech, Health & Wellness',
          viralScore: 92,
        },
        {
          color: '#4ECDC4',
          colorName: 'Teal Dream',
          trend: 'Calm and trustworthy designs',
          industry: 'Finance, Healthcare',
          viralScore: 88,
        },
        {
          color: '#95E1D3',
          colorName: 'Mint Fresh',
          trend: 'Wellness and sustainability focus',
          industry: 'Eco-friendly, Wellness',
          viralScore: 85,
        },
        {
          color: '#000000',
          colorName: 'Elegant Black',
          trend: 'Luxury and sophisticated minimalism',
          industry: 'Fashion, Luxury',
          viralScore: 90,
        },
        {
          color: '#FFD93D',
          colorName: 'Vibrant Gold',
          trend: 'Optimism and premium positioning',
          industry: 'Retail, Entertainment',
          viralScore: 82,
        },
      ];

      this.logger.info('Trending colors fetched', { count: trendingColors.length });
      return trendingColors;
    } catch (error) {
      this.logger.error('Failed to fetch trending colors', { error });
      throw error;
    }
  }

  /**
   * Get trending typography styles
   */
  async getTrendingTypography(): Promise<
    Array<{
      fontPair: string;
      primary: string;
      secondary: string;
      style: string;
      viralScore: number;
      useCase: string;
    }>
  > {
    try {
      this.logger.info('Fetching trending typography');

      const trendingTypography = [
        {
          fontPair: 'Poppins + Inter',
          primary: 'Poppins',
          secondary: 'Inter',
          style: 'Modern, Friendly',
          viralScore: 94,
          useCase: 'Tech, SaaS, Startup',
        },
        {
          fontPair: 'Playfair Display + Lato',
          primary: 'Playfair Display',
          secondary: 'Lato',
          style: 'Elegant, Editorial',
          viralScore: 89,
          useCase: 'Fashion, Luxury, Publishing',
        },
        {
          fontPair: 'Work Sans + IBM Plex Mono',
          primary: 'Work Sans',
          secondary: 'IBM Plex Mono',
          style: 'Technical, Professional',
          viralScore: 87,
          useCase: 'Tech, Developer Tools',
        },
        {
          fontPair: 'Montserrat + Open Sans',
          primary: 'Montserrat',
          secondary: 'Open Sans',
          style: 'Bold, Accessible',
          viralScore: 85,
          useCase: 'Retail, Non-profit',
        },
        {
          fontPair: 'Space Grotesk + Crimson Text',
          primary: 'Space Grotesk',
          secondary: 'Crimson Text',
          style: 'Contemporary, Sophisticated',
          viralScore: 83,
          useCase: 'Creative, Design-focused',
        },
      ];

      this.logger.info('Trending typography fetched', {
        count: trendingTypography.length,
      });

      return trendingTypography;
    } catch (error) {
      this.logger.error('Failed to fetch trending typography', { error });
      throw error;
    }
  }

  /**
   * Get comprehensive trend insights for a topic
   */
  async getTrendInsight(topic: string): Promise<TrendInsight> {
    try {
      // Check cache
      const cached = this.colorTrendsCache.get(topic);
      if (cached) {
        this.logger.debug('Returning cached trend insight', { topic });
        return cached;
      }

      this.logger.info('Generating trend insight', { topic });

      const viralAnalysis = await this.analyzeViralPotential(topic);
      const relatedTopics = await this.getRelatedTopics(topic);
      const colors = await this.getTrendingColors();
      const typography = await this.getTrendingTypography();

      const insight: TrendInsight = {
        topic,
        trendingScore: viralAnalysis.score,
        viralPotential: viralAnalysis.viralPotential,
        relatedTopics,
        colorTrends: colors.map((c) => ({
          color: c.color,
          trend: c.trend,
        })),
        typographyTrends: typography.map((t) => t.fontPair),
        patternTrends: this.getPatternTrends(),
        growthRate: Math.random() * 50 + 10, // 10-60% growth
        marketInsight: viralAnalysis.analysis,
      };

      // Cache the result
      this.colorTrendsCache.set(topic, insight);

      return insight;
    } catch (error) {
      this.logger.error('Failed to get trend insight', { error, topic });
      throw error;
    }
  }

  /**
   * Private helper: Fetch trending data
   */
  private async fetchTrendingData(regionCode: string, category: string): Promise<any[]> {
    // Simulated trending data
    return [
      { title: 'AI Design Tools', trend: 'up', changePercent: 145 },
      { title: 'Minimalist Design', trend: 'up', changePercent: 98 },
      { title: 'Web3 Interfaces', trend: 'stable', changePercent: 23 },
      { title: 'Accessibility First', trend: 'up', changePercent: 156 },
      { title: 'Motion Design', trend: 'up', changePercent: 112 },
    ];
  }

  /**
   * Private helper: Calculate trend score
   */
  private async calculateTrendScore(topic: string): Promise<number> {
    // Simulate trend scoring based on topic characteristics
    const baseScore = 50;
    const topicBoost =
      topic.toLowerCase().includes('ai') ||
      topic.toLowerCase().includes('design') ||
      topic.toLowerCase().includes('web')
        ? 30
        : 10;
    const randomVariation = Math.random() * 20 - 10;

    return Math.min(100, Math.max(0, baseScore + topicBoost + randomVariation));
  }

  /**
   * Private helper: Convert score to viral level
   */
  private scoreToViralLevel(score: number): 'low' | 'medium' | 'high' {
    if (score >= 75) return 'high';
    if (score >= 50) return 'medium';
    return 'low';
  }

  /**
   * Private helper: Generate viral analysis text
   */
  private generateViralAnalysis(topic: string, score: number): string {
    const level = this.scoreToViralLevel(score);
    const descriptions = {
      high: `${topic} shows exceptional viral potential with strong audience engagement. Expect rapid growth and high shareability across social platforms.`,
      medium: `${topic} has moderate viral potential. With proper marketing and timing, it could gain significant traction in target communities.`,
      low: `${topic} has limited viral potential but may appeal to niche audiences. Consider targeted campaigns for specific demographics.`,
    };

    return descriptions[level];
  }

  /**
   * Private helper: Get related topics
   */
  private async getRelatedTopics(topic: string): Promise<string[]> {
    const relatedTopicsMap: Record<string, string[]> = {
      'AI Design': ['Machine Learning', 'Neural Networks', 'Generative Art', 'Automation'],
      'Web Design': [
        'User Experience',
        'Responsive Design',
        'Accessibility',
        'Performance Optimization',
      ],
      'Brand Identity': [
        'Logo Design',
        'Color Psychology',
        'Typography',
        'Brand Guidelines',
      ],
    };

    return relatedTopicsMap[topic] || ['Design', 'User Experience', 'Visual Communication'];
  }

  /**
   * Private helper: Get pattern trends
   */
  private getPatternTrends(): string[] {
    return [
      'Organic shapes',
      'Glassmorphism',
      'Dark mode',
      'Micro-interactions',
      'Asymmetric layouts',
      'Variable fonts',
      '3D elements',
      'Gradient overlays',
    ];
  }

  /**
   * Private helper: Get default trending topics
   */
  private getDefaultTrendingTopics(): any[] {
    return [
      { title: 'AI-Powered Design', trend: 'up', changePercent: 245 },
      { title: 'Web3 Design', trend: 'up', changePercent: 156 },
      { title: 'Sustainable Design', trend: 'up', changePercent: 189 },
      { title: 'Micro-interactions', trend: 'up', changePercent: 132 },
      { title: 'Accessibility Design', trend: 'up', changePercent: 203 },
    ];
  }
}
