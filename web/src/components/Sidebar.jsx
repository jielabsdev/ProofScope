import React from 'react';
import { History, ShieldCheck, ShieldAlert } from 'lucide-react';

const Sidebar = ({ history, onSelect, activeId }) => {
  return (
    <div className="w-72 bg-gray-900 text-gray-100 flex flex-col border-r border-gray-800 h-screen p-4 shrink-0">
      <div className="flex items-center space-x-2 mb-6 border-b border-gray-800 pb-4">
        <History className="h-5 w-5 text-blue-400" />
        <h2 className="text-lg font-bold tracking-tight">Audit Trail History</h2>
      </div>
      <div className="flex-1 overflow-y-auto space-y-2 pr-1">
        {history.length === 0 ? (
          <p className="text-gray-500 text-sm italic text-center pt-4">No recent verification passes stored.</p>
        ) : (
          history.map((item) => {
            const isActive = activeId === item.proof_id;
            return (
              <div 
                key={item.proof_id} 
                onClick={() => onSelect(item)}
                className={`p-3 rounded-md cursor-pointer transition-all duration-150 border
                  ${isActive ? 'bg-blue-600 border-blue-500 text-white shadow-md' : 'bg-gray-800 border-gray-700 hover:bg-gray-700 text-gray-300'}`}
              >
                <div className="flex justify-between items-center">
                  <span className="font-mono text-xs font-semibold">{item.proof_id.slice(0, 14)}...</span>
                  {item.status === 'PASS' ? (
                    <ShieldCheck className={`h-4 w-4 ${isActive ? 'text-white' : 'text-green-400'}`} />
                  ) : (
                    <ShieldAlert className={`h-4 w-4 ${isActive ? 'text-white' : 'text-red-400'}`} />
                  )}
                </div>
                <div className="flex justify-between text-xs mt-2 opacity-75">
                  <span>Model: {item.model_version}</span>
                  <span>{new Date(item.timestamp).toLocaleTimeString()}</span>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default Sidebar;
