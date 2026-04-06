'use client';

import { useEffect, useState } from 'react';
import { getClusters, triggerIngest, Cluster } from '@/lib/api';
import Link from 'next/link';

export default function Home() {
  const [clusters, setClusters] = useState<Cluster[]>([]);
  const [loading, setLoading] = useState(true);
  const [ingesting, setIngesting] = useState(false);

  useEffect(() => {
    loadClusters();
  }, []);

  const loadClusters = async () => {
    setLoading(true);
    try {
      const data = await getClusters();
      setClusters(data);
    } catch (error) {
      console.error('Failed to load clusters', error);
    } finally {
      setLoading(false);
    }
  };

  const handleIngest = async () => {
    setIngesting(true);
    try {
      await triggerIngest();
      // Wait a bit then reload
      setTimeout(loadClusters, 3000);
    } catch (error) {
      console.error('Ingest failed', error);
    } finally {
      setIngesting(false);
    }
  };

  return (
    <main className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">SignalRoom</h1>
        <button
          onClick={handleIngest}
          disabled={ingesting}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
        >
          {ingesting ? 'Ingesting...' : 'Refresh Data'}
        </button>
      </div>

      {loading ? (
        <p>Loading signals...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {clusters.map((cluster) => (
            <Link href={`/clusters/${cluster.id}`} key={cluster.id}>
              <div className="border rounded-lg p-4 hover:shadow-lg transition cursor-pointer">
                <h2 className="text-xl font-semibold mb-2">{cluster.topic}</h2>
                <p className="text-gray-600 mb-2">{cluster.summary || 'No summary yet'}</p>
                <div className="flex justify-between text-sm text-gray-500">
                  <span>Momentum: {cluster.momentum.toFixed(2)}</span>
                  <span>{cluster.items.length} items</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}