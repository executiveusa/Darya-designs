import axios, { AxiosInstance } from 'axios';
import { Logger } from 'winston';
import { z } from 'zod';

/**
 * UI Design schema for validation
 */
const UIDesignSchema = z.object({
  id: z.string(),
  name: z.string(),
  components: z.array(
    z.object({
      type: z.string(),
      name: z.string(),
      props: z.record(z.any()),
      code: z.string(),
    }),
  ),
  layout: z.string(),
  styling: z.object({
    colors: z.array(z.string()),
    typography: z.record(z.string()),
    spacing: z.object({
      unit: z.string(),
      scale: z.array(z.number()),
    }),
  }),
  responsive: z.boolean(),
  accessibilityScore: z.number(),
  version: z.number(),
  createdAt: z.string(),
  updatedAt: z.string(),
});

export type UIDesign = z.infer<typeof UIDesignSchema>;

interface SuperDesignRequest {
  projectName: string;
  description: string;
  designStrategy?: Record<string, any>;
  colorPalette?: string[];
  typography?: Record<string, string>;
  componentTypes?: string[];
}

interface DesignIteration {
  version: number;
  changes: string[];
  designId: string;
  timestamp: string;
}

/**
 * SuperDesign Bridge
 * Integrates with SuperDesign API to generate UI designs
 */
export class SuperDesignBridge {
  private httpClient: AxiosInstance;
  private logger: Logger;
  private apiKey: string | undefined;
  private designCache: Map<string, UIDesign> = new Map();
  private iterationHistory: DesignIteration[] = [];

  constructor(logger: Logger) {
    this.logger = logger;
    this.apiKey = process.env.SUPERDESIGN_API_KEY;

    this.httpClient = axios.create({
      baseURL: process.env.SUPERDESIGN_API_URL || 'https://api.superdesign.io',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
        ...(this.apiKey && { Authorization: `Bearer ${this.apiKey}` }),
      },
    });
  }

  /**
   * Generate UI design from request
   */
  async generateUIDesign(request: SuperDesignRequest): Promise<UIDesign> {
    try {
      this.logger.info('Generating UI design', { projectName: request.projectName });

      // Check cache first
      const cached = this.designCache.get(request.projectName);
      if (cached) {
        this.logger.debug('Returning cached design', { projectName: request.projectName });
        return cached;
      }

      // Generate design
      const design = await this.callSuperDesignAPI(request);

      // Cache result
      this.designCache.set(request.projectName, design);

      this.logger.info('UI design generated successfully', {
        projectName: request.projectName,
        componentCount: design.components.length,
      });

      return design;
    } catch (error) {
      this.logger.error('Failed to generate UI design', {
        error,
        projectName: request.projectName,
      });
      // Return fallback design
      return this.generateFallbackDesign(request);
    }
  }

  /**
   * Generate specific components
   */
  async generateComponents(
    types: string[],
    config?: Record<string, any>,
  ): Promise<
    Array<{
      type: string;
      name: string;
      code: string;
      preview: string;
    }>
  > {
    try {
      this.logger.info('Generating components', { types });

      const components = types.map((type) => this.generateComponentCode(type, config));

      return components;
    } catch (error) {
      this.logger.error('Failed to generate components', { error, types });
      throw error;
    }
  }

  /**
   * Iterate on design
   */
  async iterateDesign(
    designId: string,
    changes: string[],
  ): Promise<{
    newDesign: UIDesign;
    iteration: DesignIteration;
  }> {
    try {
      this.logger.info('Iterating on design', { designId, changeCount: changes.length });

      const currentDesign = this.designCache.get(designId);
      if (!currentDesign) {
        throw new Error(`Design ${designId} not found in cache`);
      }

      // Update design based on changes
      const updatedDesign = this.applyDesignChanges(currentDesign, changes);

      // Record iteration
      const iteration: DesignIteration = {
        version: currentDesign.version + 1,
        changes,
        designId,
        timestamp: new Date().toISOString(),
      };

      this.iterationHistory.push(iteration);
      this.designCache.set(designId, updatedDesign);

      this.logger.info('Design iterated successfully', {
        designId,
        newVersion: updatedDesign.version,
      });

      return { newDesign: updatedDesign, iteration };
    } catch (error) {
      this.logger.error('Failed to iterate design', { error, designId });
      throw error;
    }
  }

  /**
   * Export design to code
   */
  async exportToCode(
    design: UIDesign,
    format: 'react' | 'vue' | 'svelte' | 'html',
  ): Promise<{
    code: string;
    components: Record<string, string>;
    styles: string;
  }> {
    try {
      this.logger.info('Exporting design to code', { designId: design.id, format });

      const code = this.generateFullCode(design, format);
      const components = this.generateComponentFiles(design, format);
      const styles = this.generateStylesheet(design);

      return { code, components, styles };
    } catch (error) {
      this.logger.error('Failed to export design', { error, designId: design.id });
      throw error;
    }
  }

  /**
   * Get design iterations
   */
  getIterationHistory(designId: string): DesignIteration[] {
    return this.iterationHistory.filter((i) => i.designId === designId);
  }

  /**
   * Private helper: Call SuperDesign API
   */
  private async callSuperDesignAPI(request: SuperDesignRequest): Promise<UIDesign> {
    try {
      const response = await this.httpClient.post('/designs/generate', {
        name: request.projectName,
        description: request.description,
        config: {
          colorPalette: request.colorPalette,
          typography: request.typography,
          componentTypes: request.componentTypes || [
            'Button',
            'Card',
            'Navigation',
            'Form',
            'Footer',
          ],
        },
      });

      return this.parseDesignResponse(response.data, request.projectName);
    } catch (error) {
      this.logger.warn('SuperDesign API call failed, using fallback', { error });
      throw error;
    }
  }

  /**
   * Private helper: Parse API response
   */
  private parseDesignResponse(data: any, projectName: string): UIDesign {
    return {
      id: data.id || `design-${Date.now()}`,
      name: projectName,
      components: data.components || [],
      layout: data.layout || 'grid',
      styling: data.styling || this.getDefaultStyling(),
      responsive: data.responsive !== false,
      accessibilityScore: data.accessibilityScore || 75,
      version: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
  }

  /**
   * Private helper: Generate fallback design
   */
  private generateFallbackDesign(request: SuperDesignRequest): UIDesign {
    return {
      id: `design-${Date.now()}`,
      name: request.projectName,
      components: [
        {
          type: 'Header',
          name: 'Header',
          props: { title: request.projectName },
          code: '<header><h1>${title}</h1></header>',
        },
        {
          type: 'Hero',
          name: 'Hero Section',
          props: { subtitle: request.description },
          code: '<section class="hero"><p>${subtitle}</p></section>',
        },
        {
          type: 'Features',
          name: 'Features Grid',
          props: { columns: 3 },
          code: '<section class="features"><div class="grid"></div></section>',
        },
        {
          type: 'CTA',
          name: 'Call to Action',
          props: { buttonText: 'Get Started' },
          code: '<section class="cta"><button>${buttonText}</button></section>',
        },
        {
          type: 'Footer',
          name: 'Footer',
          props: {},
          code: '<footer></footer>',
        },
      ],
      layout: 'flex-column',
      styling: this.getDefaultStyling(),
      responsive: true,
      accessibilityScore: 80,
      version: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
  }

  /**
   * Private helper: Get default styling
   */
  private getDefaultStyling() {
    return {
      colors: ['#1F2937', '#3B82F6', '#10B981', '#F59E0B', '#EF4444'],
      typography: {
        primary: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
        secondary: 'Georgia, serif',
      },
      spacing: {
        unit: 'rem',
        scale: [0.25, 0.5, 0.75, 1, 1.25, 1.5, 2, 3, 4, 6, 8],
      },
    };
  }

  /**
   * Private helper: Generate component code
   */
  private generateComponentCode(
    type: string,
    config?: Record<string, any>,
  ): {
    type: string;
    name: string;
    code: string;
    preview: string;
  } {
    const componentTemplates: Record<string, string> = {
      Button: `export const Button = ({ label, variant = 'primary' }) => (
  <button className={\`btn btn-\${variant}\`}>{label}</button>
);`,
      Card: `export const Card = ({ title, description, image }) => (
  <div className="card">
    {image && <img src={image} alt={title} />}
    <h3>{title}</h3>
    <p>{description}</p>
  </div>
);`,
      Input: `export const Input = ({ label, type = 'text', ...props }) => (
  <div className="input-group">
    {label && <label>{label}</label>}
    <input type={type} {...props} />
  </div>
);`,
      Navigation: `export const Navigation = ({ links }) => (
  <nav className="navbar">
    <ul>
      {links.map(link => (
        <li key={link.href}>
          <a href={link.href}>{link.label}</a>
        </li>
      ))}
    </ul>
  </nav>
);`,
      Hero: `export const Hero = ({ title, subtitle, ctaText }) => (
  <section className="hero">
    <div className="hero-content">
      <h1>{title}</h1>
      <p>{subtitle}</p>
      <button className="btn btn-primary">{ctaText}</button>
    </div>
  </section>
);`,
    };

    const code = componentTemplates[type] || componentTemplates.Card;
    const name = `${type}Component`;

    return {
      type,
      name,
      code,
      preview: `<${name} {...defaultProps} />`,
    };
  }

  /**
   * Private helper: Apply design changes
   */
  private applyDesignChanges(design: UIDesign, changes: string[]): UIDesign {
    const updated = { ...design };
    updated.version += 1;
    updated.updatedAt = new Date().toISOString();

    changes.forEach((change) => {
      // Parse and apply changes
      if (change.includes('color:')) {
        const colorMatch = change.match(/color:\s*(.+)/);
        if (colorMatch) {
          updated.styling.colors = [colorMatch[1], ...updated.styling.colors];
        }
      }
      if (change.includes('layout:')) {
        const layoutMatch = change.match(/layout:\s*(.+)/);
        if (layoutMatch) {
          updated.layout = layoutMatch[1];
        }
      }
    });

    return updated;
  }

  /**
   * Private helper: Generate full code
   */
  private generateFullCode(design: UIDesign, format: string): string {
    const header = this.generateCodeHeader(format);
    const components = design.components
      .map((c) => `// ${c.name}\n${c.code}`)
      .join('\n\n');

    return `${header}\n\n${components}`;
  }

  /**
   * Private helper: Generate component files
   */
  private generateComponentFiles(
    design: UIDesign,
    format: string,
  ): Record<string, string> {
    const files: Record<string, string> = {};

    design.components.forEach((component) => {
      const filename = `${component.name.replace(/\s+/g, '')}.${format === 'react' ? 'tsx' : 'vue'}`;
      files[filename] = component.code;
    });

    return files;
  }

  /**
   * Private helper: Generate stylesheet
   */
  private generateStylesheet(design: UIDesign): string {
    const colors = design.styling.colors
      .map((color, i) => `  --color-${i}: ${color};`)
      .join('\n');

    return `:root {
${colors}
}

/* Typography */
body {
  font-family: ${design.styling.typography.primary};
}

h1, h2, h3 {
  font-family: ${design.styling.typography.secondary};
}

/* Layout */
.container {
  display: ${design.layout === 'grid' ? 'grid' : 'flex'};
  gap: 2rem;
  padding: 2rem;
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    gap: 1rem;
    padding: 1rem;
  }
}`;
  }

  /**
   * Private helper: Generate code header
   */
  private generateCodeHeader(format: string): string {
    const headers: Record<string, string> = {
      react: `import React from 'react';
import './styles.css';`,
      vue: `<template>
  <div class="app">
    <!-- Components go here -->
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>`,
      html: `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Design</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>`,
    };

    return headers[format] || headers.react;
  }
}
