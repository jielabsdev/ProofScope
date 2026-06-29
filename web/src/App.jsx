import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import DropZone from './components/DropZone';
import ReportView from './components/ReportView';

function App() {
  const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem('proofscope_audit_history');
    return saved ? JSON.parse(saved) : [];
  });
  const [selectedReport, setSelectedReport] = useState(null);

  // Sync historical state metrics back to client localStorage
  useEffect(() => {
    localStorage.setItem('proofscope_audit_history', JSON.stringify(history));
  }, [history]);

  const handleNewReport = (newReport) => {
    setHistory((prevHistory) => {
      // De-duplicate array items and slice constraints to top 5 historical logs
      const filtered = prevHistory.filter(item => item.proof_id !== newReport.proof_id);
      return [newReport, ...filtered].slice(0, 5);
    });
    setSelectedReport(newReport);
  };

  return (
    <div className="flex h-screen bg-gray-50 text-gray-800 overflow-hidden font-sans antialiased">
      {/* 1. Immutable Audit Record Trail Column */}
      <Sidebar 
        history={history} 
        onSelect={setSelectedReport} 
        activeId={selectedReport?.proof_id} 
      />
      
      {/* 2. Main Processing Canvas Target space */}
      <main className="flex-1 overflow-y-auto p-8 max-w-4xl mx-auto w-full">
        <header className="mb-8 border-b border-gray-200 pb-4">
          <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">ProofScope Compliance Inspector</h1>
          <p className="text-sm text-gray-500 mt-1">Production-Grade Zero-Knowledge Cryptographic Model Verification Suite</p>
        </header>

        <div className="space-y-6">
          <DropZone onReportReceived={handleNewReport} />
          <ReportView data={selectedReport} />
        </div>
      </main>
    </div>
  );
}

export default App;
