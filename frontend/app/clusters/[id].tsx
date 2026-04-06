'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { getCluster, generateBrief, Cluster } from '@/lib/api';
import Link from 'next/link';

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
      // Refresh cluster to get updated summary
      loadCluster();
    } catch (error) {
      console.error('Brief generation failed', error);
    } finally {
      setGenerating(false);
    }
  };

  if (loading) return <p className="p-4">Loading...</p>;
  if (!cluster) return <p className="p-4">Cluster not found</p>;

  return (
    <main className="container mx-auto p-4">
      <Link href="/" className="text-blue-600 mb-4 inline-block">← Back to dashboard</Link>
      
      <h1 className="text-3xl font-bold mb-2">{cluster.topic}</h1>
      <div className="mb-4 text-gray-600">
        <span>Momentum: {cluster.momentum.toFixed(2)}</span> | 
        <span> {cluster.items.length} items</span>
      </div>

      {cluster.summary && (
        <div className="mb-6 p-4 bg-gray-50 rounded">
          <h2 className="text-xl font-semibold mb-2">Summary</h2>
          <p>{cluster.summary}</p>
        </div>
      )}

      <button
        onClick={handleGenerateBrief}
        disabled={generating}
        className="bg-green-600 text-white px-4 py-2 rounded mb-6 hover:bg-green-700 disabled:bg-gray-400"
      >
        {generating ? 'Generating...' : 'Generate Insight Brief'}
      </button>

      {brief && (
        <div className="mb-6 p-4 bg-blue-50 rounded">
          <h2 className="text-xl font-semibold mb-2">Generated Brief</h2>
          <p className="mb-2">{brief.summary}</p>
          <ul className="list-disc pl-5">
            {brief.bullets.map((b, i) => <li key={i}>{b}</li>)}
          </ul>
        </div>
      )}

      <h2 className="text-2xl font-semibold mb-4">Source Items</h2>
      <div className="space-y-4">
        {cluster.items.map((item) => (
          <div key={item.id} className="border p-4 rounded">
            <h3 className="text-lg font-medium">
              <a href={item.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                {item.title}
              </a>
            </h3>
            <p className="text-gray-600 text-sm mb-2">
              {item.author} • {new Date(item.published_at).toLocaleDateString()} • Score: {item.score}
            </p>
            <p className="text-gray-800">{item.content.slice(0, 200)}...</p>
          </div>
        ))}
      </div>
    </main>
  );
}