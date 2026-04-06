import { Logger } from 'winston';
import { z } from 'zod';

/**
 * Animation Configuration schema
 */
const AnimationConfigSchema = z.object({
  id: z.string(),
  name: z.string(),
  type: z.enum(['gsap', 'framer-motion', 'hybrid']),
  duration: z.number().positive(),
  delay: z.number().nonnegative(),
  easing: z.string(),
  properties: z.record(z.any()),
  description: z.string(),
  performanceOptimized: z.boolean(),
});

export type AnimationConfig = z.infer<typeof AnimationConfigSchema>;

interface AnimationGenerationInput {
  elementType: string;
  duration?: number;
  intensity?: 'subtle' | 'moderate' | 'dramatic';
  useVR?: boolean;
}

/**
 * Animations Service
 * Generates and manages GSAP and Framer Motion animations
 */
export class AnimationsService {
  private logger: Logger;
  private animationLibrary: Map<string, AnimationConfig> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
    this.initializeAnimationLibrary();
  }

  /**
   * Generate animation configuration for an element
   */
  generateAnimation(input: AnimationGenerationInput): AnimationConfig {
    try {
      this.logger.info('Generating animation', input);

      const animationConfig = this.buildAnimationConfig(input);

      // Cache animation
      this.animationLibrary.set(animationConfig.id, animationConfig);

      this.logger.info('Animation generated', {
        id: animationConfig.id,
        type: animationConfig.type,
      });

      return animationConfig;
    } catch (error) {
      this.logger.error('Failed to generate animation', { error, input });
      throw error;
    }
  }

  /**
   * Generate GSAP animation code
   */
  generateGSAPAnimation(config: AnimationConfig): string {
    const { properties, duration, delay, easing } = config;

    const propString = Object.entries(properties)
      .map(([key, value]) => `${key}: "${value}"`)
      .join(', ');

    return `gsap.to(".${config.id}", {
  ${propString},
  duration: ${duration},
  delay: ${delay},
  ease: "${easing}",
  repeat: 0,
  yoyo: false
});`;
  }

  /**
   * Generate Framer Motion animation code
   */
  generateFramerMotionAnimation(config: AnimationConfig): string {
    const variants = {
      hidden: this.getInitialState(config),
      visible: config.properties,
    };

    return `const ${config.id}Variants = {
  hidden: ${JSON.stringify(variants.hidden, null, 4)},
  visible: ${JSON.stringify(variants.visible, null, 4)}
};

export const ${config.id} = () => (
  <motion.div
    variants={${config.id}Variants}
    initial="hidden"
    animate="visible"
    transition={{
      duration: ${config.duration},
      delay: ${config.delay},
      ease: "${config.easing}"
    }}
  >
    {/* Content */}
  </motion.div>
);`;
  }

  /**
   * Generate VR/XR animation effects
   */
  generateVRAnimation(config: AnimationConfig): {
    three: string;
    babylon: string;
    performance: string;
  } {
    const threeCode = `// Three.js VR Animation
const scene = new THREE.Scene();
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);

function animate() {
  requestAnimationFrame(animate);
  mesh.rotation.x += ${config.properties.rotationX || 0.01};
  mesh.rotation.y += ${config.properties.rotationY || 0.01};
  renderer.render(scene, camera);
}`;

    const babylonCode = `// Babylon.js VR Animation
const scene = new BABYLON.Scene(engine);
const box = BABYLON.MeshBuilder.CreateBox("box", {}, scene);
const animation = new BABYLON.Animation(
  "animation",
  "rotation.y",
  30,
  BABYLON.Animation.ANIMATIONTYPE_FLOAT,
  BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE
);

const keys = [
  { frame: 0, value: 0 },
  { frame: ${config.duration * 30}, value: Math.PI * 2 }
];
animation.setKeys(keys);
box.animations.push(animation);
scene.beginAnimation(box, 0, ${config.duration * 30}, true);`;

    const performance = `// Performance Optimization
- Use requestAnimationFrame for smooth 60fps rendering
- Implement LOD (Level of Detail) for complex models
- Cache calculations and geometries
- Use WebGL optimizations
- Monitor frame rate and adjust quality accordingly`;

    return { three: threeCode, babylon: babylonCode, performance };
  }

  /**
   * Optimize animation for performance
   */
  optimizeForPerformance(config: AnimationConfig): AnimationConfig {
    try {
      this.logger.info('Optimizing animation for performance', { id: config.id });

      const optimized = {
        ...config,
        // Reduce duration slightly for better performance
        duration: Math.max(0.3, config.duration * 0.9),
        // Use GPU-accelerated properties only
        properties: this.filterGPUAcceleratedProperties(config.properties),
        performanceOptimized: true,
      };

      return optimized;
    } catch (error) {
      this.logger.error('Failed to optimize animation', { error });
      throw error;
    }
  }

  /**
   * Get animation by ID
   */
  getAnimation(id: string): AnimationConfig | undefined {
    return this.animationLibrary.get(id);
  }

  /**
   * Get all animations
   */
  getAllAnimations(): AnimationConfig[] {
    return Array.from(this.animationLibrary.values());
  }

  /**
   * Private helper: Build animation config
   */
  private buildAnimationConfig(input: AnimationGenerationInput): AnimationConfig {
    const id = `anim-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const duration = input.duration || 0.8;
    const intensity = input.intensity || 'moderate';
    const useVR = input.useVR || false;

    const { properties, easing } = this.getAnimationProperties(input.elementType, intensity);

    return {
      id,
      name: `${input.elementType}-animation`,
      type: useVR ? 'hybrid' : 'gsap',
      duration,
      delay: 0,
      easing,
      properties,
      description: `${intensity} animation for ${input.elementType}`,
      performanceOptimized: false,
    };
  }

  /**
   * Private helper: Get animation properties based on element type
   */
  private getAnimationProperties(
    elementType: string,
    intensity: 'subtle' | 'moderate' | 'dramatic',
  ): { properties: Record<string, any>; easing: string } {
    const propertyMap: Record<string, Record<string, any>> = {
      button: {
        subtle: {
          scale: 1.05,
          opacity: 1,
        },
        moderate: {
          scale: 1.1,
          opacity: 0.9,
          boxShadow: '0 10px 25px rgba(0,0,0,0.2)',
        },
        dramatic: {
          scale: 1.2,
          opacity: 0.8,
          boxShadow: '0 20px 40px rgba(0,0,0,0.3)',
          rotate: 5,
        },
      },
      card: {
        subtle: {
          y: -5,
          opacity: 1,
        },
        moderate: {
          y: -10,
          opacity: 0.95,
          boxShadow: '0 20px 40px rgba(0,0,0,0.15)',
        },
        dramatic: {
          y: -20,
          opacity: 0.9,
          boxShadow: '0 40px 80px rgba(0,0,0,0.25)',
          rotate: -2,
        },
      },
      text: {
        subtle: {
          opacity: 1,
          y: -2,
        },
        moderate: {
          opacity: 0.95,
          y: -5,
          letterSpacing: 1,
        },
        dramatic: {
          opacity: 0.9,
          y: -10,
          letterSpacing: 2,
          scale: 1.05,
        },
      },
    };

    const easing = intensity === 'subtle' ? 'power1.inOut' : 'power3.inOut';

    const defaultProperties = {
      opacity: 1,
      scale: 1,
    };

    return {
      properties: propertyMap[elementType]?.[intensity] || defaultProperties,
      easing,
    };
  }

  /**
   * Private helper: Get initial state for animations
   */
  private getInitialState(config: AnimationConfig): Record<string, any> {
    return {
      opacity: 0,
      scale: 0.8,
      y: 20,
    };
  }

  /**
   * Private helper: Filter for GPU-accelerated properties
   */
  private filterGPUAcceleratedProperties(properties: Record<string, any>): Record<string, any> {
    const gpuProperties = ['transform', 'opacity', 'scale', 'rotate', 'x', 'y', 'z'];
    const filtered: Record<string, any> = {};

    Object.entries(properties).forEach(([key, value]) => {
      if (
        gpuProperties.includes(key) ||
        key.startsWith('rotate') ||
        key.startsWith('scale') ||
        key.includes('Scale')
      ) {
        filtered[key] = value;
      }
    });

    return Object.keys(filtered).length > 0 ? filtered : properties;
  }

  /**
   * Private helper: Initialize animation library with presets
   */
  private initializeAnimationLibrary(): void {
    const presets: AnimationConfig[] = [
      {
        id: 'fade-in',
        name: 'Fade In',
        type: 'gsap',
        duration: 0.5,
        delay: 0,
        easing: 'power1.inOut',
        properties: { opacity: 1 },
        description: 'Simple fade-in animation',
        performanceOptimized: true,
      },
      {
        id: 'slide-up',
        name: 'Slide Up',
        type: 'framer-motion',
        duration: 0.6,
        delay: 0,
        easing: 'easeOut',
        properties: { y: 0, opacity: 1 },
        description: 'Slide element up from bottom',
        performanceOptimized: true,
      },
      {
        id: 'bounce',
        name: 'Bounce',
        type: 'gsap',
        duration: 0.8,
        delay: 0,
        easing: 'back.out',
        properties: { scale: 1 },
        description: 'Bouncy scale animation',
        performanceOptimized: true,
      },
      {
        id: 'scale-pulse',
        name: 'Scale Pulse',
        type: 'gsap',
        duration: 1.5,
        delay: 0,
        easing: 'sine.inOut',
        properties: { scale: 1.1 },
        description: 'Pulsing scale effect',
        performanceOptimized: true,
      },
    ];

    presets.forEach((preset) => {
      this.animationLibrary.set(preset.id, preset);
    });

    this.logger.info('Animation library initialized', {
      presetCount: presets.length,
    });
  }
}
