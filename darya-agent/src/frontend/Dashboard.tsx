/**
 * Darya Design Wizard - Main Dashboard Component
 * Bilingual React interface with Tailwind CSS and GSAP animations
 */

import React, { useState, useEffect, useRef } from 'react';
import gsap from 'gsap';
import { i18n } from '../i18n/translations.js';

interface Project {
  id: string;
  name: string;
  description?: string;
  status: 'draft' | 'in-progress' | 'review' | 'completed' | 'archived';
  estimatedHours: number;
  createdAt: Date;
  colorPalette?: string[];
  componentCount: number;
}

interface DashboardMetrics {
  totalProjects: number;
  completedProjects: number;
  totalHours: number;
  averageScore: number;
  recentTrends: string[];
}

interface Trend {
  topic: string;
  trendingScore: number;
  viralPotential: 'low' | 'medium' | 'high';
}

/**
 * Main Dashboard Component
 */
export const Dashboard: React.FC = () => {
  // State
  const [currentLanguage, setCurrentLanguage] = useState<'en' | 'es'>('en');
  const [projects, setProjects] = useState<Project[]>([]);
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [trends, setTrends] = useState<Trend[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'projects' | 'trends'>('overview');

  // Refs for animations
  const dashboardRef = useRef<HTMLDivElement>(null);
  const metricsRef = useRef<HTMLDivElement>(null);
  const projectsRef = useRef<HTMLDivElement>(null);

  // Initialize language
  useEffect(() => {
    i18n.setLanguage(currentLanguage);
  }, [currentLanguage]);

  // Fetch data on mount
  useEffect(() => {
    fetchDashboardData();
  }, []);

  // Animate on mount
  useEffect(() => {
    animateDashboard();
  }, [activeTab]);

  /**
   * Fetch dashboard data from API
   */
  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const userId = localStorage.getItem('userId') || 'demo-user';

      // Fetch metrics
      const metricsRes = await fetch(`/api/dashboard/metrics?userId=${userId}`);
      const metricsData = await metricsRes.json();
      if (metricsData.success) {
        setMetrics(metricsData.data);
      }

      // Fetch projects
      const projectsRes = await fetch(`/api/projects/list?userId=${userId}`);
      const projectsData = await projectsRes.json();
      if (projectsData.success) {
        setProjects(projectsData.data);
      }

      // Fetch trends
      const trendsRes = await fetch('/api/trends/trending?region=US');
      const trendsData = await trendsRes.json();
      if (trendsData.success) {
        setTrends(trendsData.data.slice(0, 5));
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Animate dashboard on load and tab change
   */
  const animateDashboard = () => {
    if (!dashboardRef.current) return;

    const tl = gsap.timeline();

    // Fade in dashboard
    tl.fromTo(
      dashboardRef.current,
      { opacity: 0, y: 20 },
      { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' },
    );

    // Stagger animate metrics cards
    if (metricsRef.current) {
      tl.fromTo(
        metricsRef.current.querySelectorAll('.metric-card'),
        { opacity: 0, scale: 0.9 },
        { opacity: 1, scale: 1, duration: 0.4, stagger: 0.1, ease: 'back.out' },
        '-=0.3',
      );
    }

    // Stagger animate project cards
    if (projectsRef.current && activeTab === 'projects') {
      tl.fromTo(
        projectsRef.current.querySelectorAll('.project-card'),
        { opacity: 0, x: -20 },
        { opacity: 1, x: 0, duration: 0.3, stagger: 0.05, ease: 'power2.out' },
        '-=0.2',
      );
    }
  };

  /**
   * Format date
   */
  const formatDate = (date: Date) => {
    return new Date(date).toLocaleDateString(currentLanguage === 'es' ? 'es-ES' : 'en-US');
  };

  /**
   * Get status badge color
   */
  const getStatusColor = (status: string): string => {
    const colors: Record<string, string> = {
      draft: 'bg-gray-100 text-gray-800',
      'in-progress': 'bg-blue-100 text-blue-800',
      review: 'bg-yellow-100 text-yellow-800',
      completed: 'bg-green-100 text-green-800',
      archived: 'bg-gray-200 text-gray-600',
    };
    return colors[status] || colors.draft;
  };

  /**
   * Get viral potential color
   */
  const getViralColor = (potential: string): string => {
    const colors: Record<string, string> = {
      low: 'text-gray-500',
      medium: 'text-yellow-500',
      high: 'text-red-500',
    };
    return colors[potential] || colors.low;
  };

  return (
    <div
      ref={dashboardRef}
      className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white"
    >
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-800 shadow-lg">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">{i18n.t('app.name')}</h1>
              <p className="mt-1 text-slate-300">{i18n.t('app.tagline')}</p>
            </div>
            <div className="flex items-center gap-4">
              {/* Language Switcher */}
              <div className="flex gap-2">
                <button
                  onClick={() => setCurrentLanguage('en')}
                  className={`rounded px-3 py-1 text-sm font-medium transition ${
                    currentLanguage === 'en'
                      ? 'bg-blue-600 text-white'
                      : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                  }`}
                >
                  EN
                </button>
                <button
                  onClick={() => setCurrentLanguage('es')}
                  className={`rounded px-3 py-1 text-sm font-medium transition ${
                    currentLanguage === 'es'
                      ? 'bg-blue-600 text-white'
                      : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                  }`}
                >
                  ES
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Tabs */}
        <div className="mb-8 border-b border-slate-700">
          <nav className="flex gap-4">
            {(['overview', 'projects', 'trends'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 font-medium transition ${
                  activeTab === tab
                    ? 'border-b-2 border-blue-500 text-blue-400'
                    : 'text-slate-400 hover:text-slate-300'
                }`}
              >
                {i18n.t(`dashboard.${tab === 'overview' ? 'title' : tab === 'projects' ? 'recentProjects' : 'trendingNow'}`)}
              </button>
            ))}
          </nav>
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="text-lg text-slate-400">{i18n.t('common.loading')}</div>
          </div>
        ) : (
          <>
            {/* Overview Tab */}
            {activeTab === 'overview' && (
              <div ref={metricsRef} className="space-y-8">
                {/* Metrics Grid */}
                <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
                  <MetricCard
                    label={i18n.t('projects.title')}
                    value={metrics?.totalProjects || 0}
                  />
                  <MetricCard
                    label={i18n.t('projects.statusCompleted')}
                    value={metrics?.completedProjects || 0}
                  />
                  <MetricCard
                    label={i18n.t('design.estimatedHours')}
                    value={metrics?.totalHours || 0}
                  />
                  <MetricCard
                    label="Avg Score"
                    value={metrics?.averageScore || 0}
                    format="percentage"
                  />
                </div>

                {/* Welcome Section */}
                <div className="rounded-lg border border-slate-700 bg-slate-800 p-6">
                  <h2 className="text-2xl font-bold">{i18n.t('dashboard.welcome')}</h2>
                  <p className="mt-2 text-slate-400">{i18n.t('dashboard.subtitle')}</p>

                  <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
                    <QuickActionButton
                      icon="✨"
                      label={i18n.t('dashboard.createProject')}
                      onClick={() => setActiveTab('projects')}
                    />
                    <QuickActionButton
                      icon="📊"
                      label={i18n.t('dashboard.browseTrends')}
                      onClick={() => setActiveTab('trends')}
                    />
                    <QuickActionButton
                      icon="📈"
                      label={i18n.t('dashboard.viewAnalytics')}
                      onClick={() => {}}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Projects Tab */}
            {activeTab === 'projects' && (
              <div ref={projectsRef} className="space-y-4">
                {projects.length === 0 ? (
                  <div className="rounded-lg border border-slate-700 bg-slate-800 p-8 text-center">
                    <p className="text-slate-400">{i18n.t('projects.noProjects')}</p>
                  </div>
                ) : (
                  projects.map((project) => (
                    <div
                      key={project.id}
                      className="project-card rounded-lg border border-slate-700 bg-slate-800 p-6 hover:border-blue-500 hover:bg-slate-750 transition"
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="text-lg font-semibold">{project.name}</h3>
                          <p className="mt-1 text-sm text-slate-400">{project.description}</p>
                          <div className="mt-2 flex gap-2">
                            <span
                              className={`inline-block rounded px-2 py-1 text-xs font-medium ${getStatusColor(project.status)}`}
                            >
                              {i18n.t(`projects.status${project.status.charAt(0).toUpperCase()}${project.status.slice(1)}`)}
                            </span>
                            <span className="text-xs text-slate-400">
                              {i18n.t('projects.created')}: {formatDate(project.createdAt)}
                            </span>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-2xl font-bold text-blue-400">
                            {project.componentCount}
                          </p>
                          <p className="text-xs text-slate-400">
                            {i18n.t('components.title')}
                          </p>
                        </div>
                      </div>

                      {project.colorPalette && project.colorPalette.length > 0 && (
                        <div className="mt-4 flex gap-2">
                          {project.colorPalette.map((color) => (
                            <div
                              key={color}
                              className="h-8 w-8 rounded border border-slate-600"
                              style={{ backgroundColor: color }}
                              title={color}
                            />
                          ))}
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            )}

            {/* Trends Tab */}
            {activeTab === 'trends' && (
              <div className="space-y-4">
                {trends.length === 0 ? (
                  <div className="rounded-lg border border-slate-700 bg-slate-800 p-8 text-center">
                    <p className="text-slate-400">{i18n.t('common.loading')}</p>
                  </div>
                ) : (
                  trends.map((trend, idx) => (
                    <div
                      key={idx}
                      className="rounded-lg border border-slate-700 bg-slate-800 p-6"
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="text-lg font-semibold">{trend.topic}</h3>
                          <div className="mt-2 flex gap-4">
                            <span className="text-sm text-slate-400">
                              {i18n.t('trends.trendScore')}: {trend.trendingScore}/100
                            </span>
                            <span
                              className={`text-sm font-medium ${getViralColor(trend.viralPotential)}`}
                            >
                              {i18n.t('trends.viralPotential')}:{' '}
                              {i18n.t(`trends.${trend.viralPotential}`)}
                            </span>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="h-12 w-12 rounded-full bg-blue-600 flex items-center justify-center text-lg font-bold">
                            {trend.trendingScore}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-700 bg-slate-800 py-6 text-center text-sm text-slate-400">
        <p>
          © 2024 {i18n.t('app.name')} • {i18n.t('app.tagline')}
        </p>
      </footer>
    </div>
  );
};

/**
 * Metric Card Component
 */
interface MetricCardProps {
  label: string;
  value: number | string;
  format?: 'default' | 'percentage';
}

const MetricCard: React.FC<MetricCardProps> = ({ label, value, format = 'default' }) => {
  const formattedValue =
    format === 'percentage' ? `${value}%` : format === 'default' ? value : value;

  return (
    <div className="metric-card rounded-lg border border-slate-700 bg-slate-800 p-6 hover:border-blue-500 transition">
      <p className="text-sm font-medium text-slate-400">{label}</p>
      <p className="mt-2 text-3xl font-bold text-blue-400">{formattedValue}</p>
    </div>
  );
};

/**
 * Quick Action Button Component
 */
interface QuickActionButtonProps {
  icon: string;
  label: string;
  onClick: () => void;
}

const QuickActionButton: React.FC<QuickActionButtonProps> = ({ icon, label, onClick }) => {
  return (
    <button
      onClick={onClick}
      className="rounded-lg border border-slate-600 bg-slate-700 p-4 text-center hover:border-blue-500 hover:bg-slate-600 transition"
    >
      <div className="text-2xl">{icon}</div>
      <p className="mt-2 text-sm font-medium">{label}</p>
    </button>
  );
};

export default Dashboard;
