import React from 'react';
import { Download, FileCheck, Cpu, Zap, Activity } from 'lucide-react';

const ReportView = ({ data }) => {
  if (!data) return null;

  const downloadReport = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `proofscope_audit_${data.proof_id}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="mt-6 p-6 bg-white rounded-lg border border-gray-200 shadow-sm">
      <div className="flex justify-between items-start border-b border-gray-100 pb-4 mb-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 flex items-center space-x-2">
            <FileCheck className="h-5 w-5 text-blue-600" />
            <span>Audit Frame Verified</span>
          </h2>
          <p className="text-xs font-mono text-gray-500 mt-1">ID: {data.proof_id}</p>
        </div>
        <button 
          onClick={downloadReport}
          className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-md text-sm transition shadow-sm"
        >
          <Download className="h-4 w-4" />
          <span>Export Audit Log</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm mb-6">
        <div className="p-3 bg-gray-50 rounded-md">
          <p className="text-gray-500 font-medium">Status Verification</p>
          <span className={`text-lg font-bold ${data.status === 'PASS' ? 'text-green-600' : 'text-red-600'}`}>{data.status}</span>
        </div>
        <div className="p-3 bg-gray-50 rounded-md">
          <p className="text-gray-500 font-medium">Model Architecture Version</p>
          <span className="text-lg font-semibold text-gray-800">{data.model_version}</span>
        </div>
        <div className="p-3 bg-gray-50 rounded-md">
          <p className="text-gray-500 font-medium flex items-center space-x-1"><Zap className="h-4 w-4 text-amber-500" /> <span>Core Latency</span></p>
          <span className="text-lg font-semibold text-gray-800">{data.execution_time_ms.toFixed(2)} ms</span>
        </div>
        <div className="p-3 bg-gray-50 rounded-md">
          <p className="text-gray-500 font-medium flex items-center space-x-1"><Cpu className="h-4 w-4 text-indigo-500" /> <span>Gate Complexity</span></p>
          <span className="text-lg font-semibold text-gray-800">{data.gate_count.toLocaleString()} gates (Depth: {data.circuit_depth})</span>
        </div>
        <div className="p-3 bg-gray-50 rounded-md">
          <p className="text-gray-500 font-medium">Confidence Coefficient</p>
          <span className="text-lg font-semibold text-gray-800">{(data.confidence_score * 100).toFixed(1)}%</span>
        </div>
        <div className="p-3 bg-gray-50 rounded-md">
          <p className="text-gray-500 font-medium">Circuit Constraint Utilization</p>
          <span className="text-lg font-semibold text-gray-800">{(data.constraint_utilization * 100).toFixed(1)}%</span>
        </div>
      </div>

      <div className="p-4 bg-gray-900 text-gray-100 rounded-md">
        <div className="flex items-center space-x-2 text-xs font-semibold text-gray-400 mb-2 uppercase tracking-wider">
          <Activity className="h-3 w-3" />
          <span>Cryptographic Execution Path Trace Hash</span>
        </div>
        <code className="text-xs break-all font-mono block text-green-400 bg-black p-2 rounded border border-gray-800">{data.execution_path_hash}</code>
      </div>
    </div>
  );
};

export default ReportView;
