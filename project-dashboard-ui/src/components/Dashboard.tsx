// project-dashboard-ui/src/components/Dashboard.tsx

import React, { useState, useEffect } from 'react';
import { fetchContributors, fetchStatusCounts } from '../api/github';

// --- INTERFACES ---

interface DashboardCardProps {
    title: string;
    value: number;
    color: string;
}

interface Contributor {
    id: number;
    login: string;
    html_url: string;
    avatar_url: string;
    contributions: number;
}

interface ContributorItemProps {
    contributor: Contributor;
    rank: number;
}

// The error 'Property id does not exist on type 'never'' usually means TypeScript
// cannot infer the type of the `contributors` array; defining the Contributors type fixes this.

// --- HELPER COMPONENTS ---

// Fixed: Added DashboardCardProps type annotation
const DashboardCard = ({ title, value, color }: DashboardCardProps) => (
    <div className="dashboard-card" style={{ borderColor: color }}>
        <h4 style={{ color }}>{value}</h4>
        <p>{title}</p>
    </div>
);

// Fixed: Added ContributorItemProps type annotation
const ContributorItem = ({ contributor, rank }: ContributorItemProps) => (
    <div className="contributor-item">
        {/* The existence error for 'id' is fixed by defining the Contributor interface */}
        <span className="contributor-rank">{rank}.</span>
        <a href={contributor.html_url} target="_blank" rel="noopener noreferrer">
            <img 
                src={contributor.avatar_url} 
                alt={contributor.login} 
                className="contributor-avatar" 
            />
            {contributor.login}
        </a>
        <span className="contributor-count">{contributor.contributions} commits</span>
    </div>
);

// --- MAIN COMPONENT ---

const Dashboard = () => {
    // Fixed: Defined contributors state as an array of Contributor
    const [stats, setStats] = useState({ open_prs: 0, open_issues: 0, total_open: 0 });
    const [contributors, setContributors] = useState<Contributor[]>([]);
    
    const [loading, setLoading] = useState(true);
    // Fixed: Set initial state to null, and only assign string on error
    const [error, setError] = useState<string | null>(null); 

    useEffect(() => {
        const loadData = async () => {
            try {
                // ... (API calls unchanged)
                const [statusCounts, contributorList] = await Promise.all([
                    fetchStatusCounts(),
                    fetchContributors()
                ]);

                setStats(statusCounts);
                // TypeScript now knows this is an array of Contributor
                setContributors(contributorList); 

            } catch (err) {
                console.error("Dashboard error:", err);
                // Fixed: The error parameter must be handled as an unknown type
                setError('Failed to load GitHub data. Check console for details.'); 
            } finally {
                setLoading(false);
            }
        };
        loadData();
    }, []);

    if (loading) {
        return <div style={{ textAlign: 'center', padding: '20px' }}>Loading Hacktoberfest Dashboard...</div>;
    }

    if (error) {
        return <div style={{ color: 'red', textAlign: 'center', padding: '20px' }}>Error loading dashboard: {error}</div>;
    }

    return (
        <div className="project-dashboard" style={{ maxWidth: '800px', margin: 'auto', fontFamily: 'Arial, sans-serif' }}>
            <h1 style={{ textAlign: 'center' }}>Hacktoberfest Project Dashboard</h1>

            {/* Status Cards */}
            <div style={{ display: 'flex', justifyContent: 'space-around', margin: '20px 0', border: '1px solid #ccc', padding: '15px' }}>
                <DashboardCard title="Total Open PRs" value={stats.open_prs} color="#28a745" />
                <DashboardCard title="Total Open Issues" value={stats.open_issues} color="#d73a49" />
                <DashboardCard title="Total Open Items" value={stats.total_open} color="#0366d6" />
                <DashboardCard title="Total Contributors" value={contributors.length} color="#6f42c1" />
            </div>

            {/* Top Contributors List */}
            <h2 style={{ borderBottom: '1px solid #eee', paddingBottom: '10px' }}>Top Contributors</h2>
            <div className="contributor-list">
                {/* TypeScript now verifies 'c' has an 'id' property */}
                {contributors.map((c, index) => ( 
                    <ContributorItem key={c.id} contributor={c} rank={index + 1} />
                ))}
            </div>
        </div>
    );
};

export default Dashboard;