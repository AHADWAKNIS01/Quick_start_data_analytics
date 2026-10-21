import React from 'react';

interface LandingProps {
  onOpenDashboard: () => void;
}

export const LandingPage: React.FC<LandingProps> = ({ onOpenDashboard }) => {
  return (
    <div className="landing-wrap">
      {/* 1. Hero & Project Overview */}
      <section className="landing-hero">
        <div className="landing-badge">BATCH GROCERY ANALYTICS PLATFORM</div>
        <h1 className="landing-title">
          QuickCart <span>Analytics</span> Platform
        </h1>
        <p className="landing-lead">
          QuickCart Analytics is a Big Data batch analytics platform that processes historical Instacart grocery order data to identify customer purchasing patterns, product reorder rates, department-wise sales distribution, and hourly and weekly demand trends.
        </p>

        <div className="landing-cta-group">
          <button className="landing-btn primary" onClick={onOpenDashboard}>
            Explore Dashboard ➔
          </button>
          <a href="#workflow" className="landing-btn secondary">
            View Architecture &amp; Workflow
          </a>
        </div>

        <div className="landing-tags">
          <span>Python 3.11</span>
          <span>FastAPI</span>
          <span>Pandas / PySpark</span>
          <span>React 19</span>
          <span>TypeScript</span>
          <span>Vite</span>
          <span>Recharts</span>
          <span>Instacart 2017 Dataset</span>
        </div>
      </section>

      {/* 2. Key Features */}
      <section className="landing-section" id="features">
        <div className="section-head-pill">PROJECT CAPABILITIES</div>
        <h2>Key Features</h2>
        <p className="landing-subtitle">Core analytical modules implemented in the system.</p>

        <div className="landing-features-grid">
          <div className="feature-card">
            <span className="feature-number">01</span>
            <h4>Executive Dashboard</h4>
            <p>Summary KPI metrics displaying total order volume, unique customer count, total units sold, and overall dataset reorder ratio.</p>
          </div>

          <div className="feature-card">
            <span className="feature-number">02</span>
            <h4>Demand Analysis</h4>
            <p>Explores historical ordering distributions across all 24 hours of the day and across day-of-week indexes (0–6).</p>
          </div>

          <div className="feature-card">
            <span className="feature-number">03</span>
            <h4>Product Explorer</h4>
            <p>Interactive table and charts to search, filter by department, filter by minimum repeat purchase rate, and sort products.</p>
          </div>

          <div className="feature-card">
            <span className="feature-number">04</span>
            <h4>Repeat Purchase Analysis</h4>
            <p>Visual breakdown comparing first-time product trials against repeat customer purchases to evaluate product stickiness.</p>
          </div>

          <div className="feature-card">
            <span className="feature-number">05</span>
            <h4>Department Analytics</h4>
            <p>Calculates and charts item volume distribution across grocery categories (Produce, Dairy, Snacks, Beverages, etc.).</p>
          </div>

          <div className="feature-card">
            <span className="feature-number">06</span>
            <h4>REST API Service</h4>
            <p>FastAPI backend exposing clean JSON endpoints (<code>/api/summary</code>, <code>/api/analytics/*</code>) with automatic OpenAPI docs.</p>
          </div>
        </div>
      </section>

      {/* 3. How It Works & Architecture */}
      <section className="landing-section" id="workflow">
        <div className="section-head-pill">DATA PIPELINE</div>
        <h2>How It Works (System Architecture)</h2>
        <p className="landing-subtitle">
          <strong>Workflow:</strong> CSV Data ➔ ETL Processing ➔ FastAPI ➔ React Dashboard ➔ Business Insights
        </p>

        <div className="architecture-steps">
          <div className="arch-step">
            <div className="step-badge">STAGE 1</div>
            <h4>Data Ingestion</h4>
            <p>Load historical grocery transaction tables from CSV files.</p>
            <code>orders, products, departments, prior/train baskets</code>
          </div>

          <div className="arch-arrow">➔</div>

          <div className="arch-step">
            <div className="step-badge">STAGE 2</div>
            <h4>ETL Processing</h4>
            <p>Clean, join relational tables, and compute aggregated summaries using Pandas / PySpark.</p>
            <code>ETL Batch Processor</code>
          </div>

          <div className="arch-arrow">➔</div>

          <div className="arch-step">
            <div className="step-badge">STAGE 3</div>
            <h4>API Layer</h4>
            <p>FastAPI reads processed aggregates and serves high-speed JSON endpoints with CORS.</p>
            <code>FastAPI REST Server (:8000)</code>
          </div>

          <div className="arch-arrow">➔</div>

          <div className="arch-step">
            <div className="step-badge">STAGE 4</div>
            <h4>Dashboard</h4>
            <p>React + TypeScript client fetches endpoints and renders interactive Recharts graphs.</p>
            <code>Vite Dev Server (:5173)</code>
          </div>
        </div>
      </section>

      {/* 4. Who Can Use It & 5. Real-World Applications */}
      <div className="landing-features-grid" style={{ marginBottom: '44px' }}>
        <div className="feature-card" style={{ gridColumn: 'span 1' }}>
          <div className="section-head-pill">TARGET AUDIENCE</div>
          <h4>👥 Who Can Use It?</h4>
          <ul style={{ paddingLeft: '18px', fontSize: '13px', lineHeight: '1.9', color: '#60687d', margin: '10px 0 0' }}>
            <li><strong>Data engineering &amp; analytics students:</strong> Understand end-to-end data pipelines, ETL batches, and web integration.</li>
            <li><strong>Business &amp; data analysts:</strong> Track customer repeat behaviors and category performance.</li>
            <li><strong>Quick-commerce operations teams:</strong> Study order timing trends to support delivery staffing plans.</li>
            <li><strong>Inventory &amp; category managers:</strong> Identify top-purchased products and high-loyalty staples.</li>
          </ul>
        </div>

        <div className="feature-card" style={{ gridColumn: 'span 2' }}>
          <div className="section-head-pill">PRACTICAL VALUE</div>
          <h4>🏢 Real-World Applications</h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '14px', marginTop: '10px' }}>
            <div style={{ background: '#f8f9fd', border: '1px solid #e7ebf5', borderRadius: '10px', padding: '14px' }}>
              <strong style={{ fontSize: '13px', color: '#20283d' }}>Demand &amp; Delivery Staffing</strong>
              <p style={{ fontSize: '12px', color: '#687084', margin: '6px 0 0', lineHeight: '1.5' }}>
                Analyze peak order hours to better plan delivery rider shifts during high-volume periods.
              </p>
            </div>
            <div style={{ background: '#f8f9fd', border: '1px solid #e7ebf5', borderRadius: '10px', padding: '14px' }}>
              <strong style={{ fontSize: '13px', color: '#20283d' }}>Inventory &amp; Replenishment</strong>
              <p style={{ fontSize: '12px', color: '#687084', margin: '6px 0 0', lineHeight: '1.5' }}>
                Stock high-demand grocery items and fast-moving categories ahead of peak weekend cycles.
              </p>
            </div>
            <div style={{ background: '#f8f9fd', border: '1px solid #e7ebf5', borderRadius: '10px', padding: '14px' }}>
              <strong style={{ fontSize: '13px', color: '#20283d' }}>Customer Reorder &amp; Loyalty</strong>
              <p style={{ fontSize: '12px', color: '#687084', margin: '6px 0 0', lineHeight: '1.5' }}>
                Identify staple items with strong reorder ratios to guide customer retention strategies.
              </p>
            </div>
            <div style={{ background: '#f8f9fd', border: '1px solid #e7ebf5', borderRadius: '10px', padding: '14px' }}>
              <strong style={{ fontSize: '13px', color: '#20283d' }}>Department &amp; Promotion Strategy</strong>
              <p style={{ fontSize: '12px', color: '#687084', margin: '6px 0 0', lineHeight: '1.5' }}>
                Evaluate category share to optimize product catalog placement and promotional discounts.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* 6. Technology Stack Summary */}
      <section className="landing-section">
        <div className="section-head-pill">ARCHITECTURE STACK</div>
        <h2>Technology Stack</h2>
        <div className="landing-tags" style={{ marginTop: '14px' }}>
          <span style={{ padding: '8px 14px' }}>🐍 Python 3.11</span>
          <span style={{ padding: '8px 14px' }}>⚡ FastAPI (REST Backend)</span>
          <span style={{ padding: '8px 14px' }}>🐼 Pandas &amp; PySpark (Batch ETL)</span>
          <span style={{ padding: '8px 14px' }}>⚛️ React 19 + TypeScript (Frontend)</span>
          <span style={{ padding: '8px 14px' }}>⚡ Vite (Build &amp; Dev Tool)</span>
          <span style={{ padding: '8px 14px' }}>📊 Recharts (Data Visualizations)</span>
          <span style={{ padding: '8px 14px' }}>📦 Instacart Market Basket Dataset (2017)</span>
        </div>
      </section>

      {/* Final Action Banner */}
      <section className="landing-final-cta">
        <h2>Explore the Live Analytics Dashboard</h2>
        <p>View interactive charts, apply department filters, search products, and inspect KPIs.</p>
        <button className="landing-btn primary large" onClick={onOpenDashboard}>
          Explore Dashboard ➔
        </button>
      </section>
    </div>
  );
};
