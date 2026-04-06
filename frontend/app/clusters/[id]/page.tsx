'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { getCluster, generateBrief, Cluster } from '@/lib/api';
import Link from 'next/link';
import Spinner from '@/components/Spinner';

export default function ClusterDetail() {
  const { id } = useParams();
  const [cluster, setCluster] = useState<Cluster | null>(null);
  const [loading, setLoading] = useState(true);
  const [brief, setBrief] = useState<{ summary: string; bullets: string[] } | null>(null);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    if (id) loadCluster();
  }, [id]);

  const loadCluster = async () => {
    setLoading(true);
    try {
      const data = await getCluster(Number(id));
      setCluster(data);
    } catch (error) {
      console.error('Failed to load cluster', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateBrief = async () => {
    setGenerating(true);
    try {
      const data = await generateBrief(Number(id));
      setBrief(data);
      loadCluster(); // refresh to get updated summary
    } catch (error) {
      console.error('Brief generation failed', error);
    } finally {
      setGenerating(false);
    }
  };

  if (loading) return <Spinner />;
  if (!cluster) return <div className="text-center py-16">Cluster not found</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <Link href="/" className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-6">
          ← Back to dashboard
        </Link>

        <div className="bg-white rounded-xl shadow-sm border p-6 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{cluster.topic}</h1>
          <div className="flex items-center gap-4 text-sm text-gray-500 mb-6">
            <span>🔥 Momentum: {Math.round(cluster.momentum)}%</span>
            <span>📄 {cluster.items.length} source items</span>
          </div>

          {cluster.summary && (
            <div className="bg-blue-50 border border-blue-100 rounded-lg p-4 mb-6">
              <h2 className="font-semibold text-gray-900 mb-2">Summary</h2>
              <p className="text-gray-700">{cluster.summary}</p>
            </div>
          )}

          <button
            onClick={handleGenerateBrief}
            disabled={generating}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 transition"
          >
            {generating ? 'Generating...' : '✨ Generate Insight Brief'}
          </button>
        </div>

        {brief && (
          <div className="bg-white rounded-xl shadow-sm border p-6 mb-8 animate-fadeIn">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">AI‑Generated Brief</h2>
            <p className="text-gray-700 mb-4">{brief.summary}</p>
            <ul className="space-y-2">
              {brief.bullets.map((bullet, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">•</span>
                  <span className="text-gray-700">{bullet}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
          <div className="px-6 py-4 border-b bg-gray-50">
            <h2 className="font-semibold text-gray-900">Source Items</h2>
          </div>
          <div className="divide-y">
            {cluster.items.map((item) => (
              <div key={item.id} className="p-6 hover:bg-gray-50 transition">
                <div className="flex justify-between items-start gap-4">
                  <div className="flex-1">
                    <a
                      href={item.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-lg font-medium text-blue-600 hover:underline"
                    >
                      {item.title}
                    </a>
                    <div className="flex items-center gap-3 text-sm text-gray-500 mt-1">
                      <span>{item.author || 'Unknown author'}</span>
                      <span>•</span>
                      <span>{new Date(item.published_at).toLocaleDateString()}</span>
                      <span>•</span>
                      <span className="inline-flex items-center gap-1">
                        ⭐ {item.score}
                      </span>
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs bg-gray-100">
                        {item.source?.name || 'RSS'}
                      </span>
                    </div>
                    <p className="mt-2 text-gray-600 line-clamp-3">{item.content}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}