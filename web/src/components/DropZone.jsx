import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { Loader2, AlertCircle, UploadCloud } from 'lucide-react';

const DropZone = ({ onReportReceived }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:8057/verify', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      onReportReceived(response.data);
    } catch (err) {
      console.error(err);
      setError("Cryptographic audit execution failed. Ensure the proof binary artifact is structurally valid.");
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop, disabled: loading });

  return (
    <div {...getRootProps()} className={`p-10 border-2 border-dashed rounded-lg text-center transition-all duration-200 bg-white
      ${loading ? 'border-blue-400 bg-blue-50 opacity-75' : 'border-gray-300 hover:border-blue-500 cursor-pointer'}`}>
      <input {...getInputProps()} />
      {loading ? (
        <div className="flex flex-col items-center justify-center space-y-3 text-blue-600">
          <Loader2 className="h-10 w-10 animate-spin" />
          <p className="font-medium text-lg">C++ Verifier Engine executing arithmetic validation matrix...</p>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center space-y-2">
          <UploadCloud className="h-10 w-10 text-gray-400" />
          <p className="text-gray-600 font-medium text-lg">Drag & drop your ZK-proof file here, or click to browse</p>
          <span className="text-sm text-gray-400">Verifying structures over pybind11 pipeline layer</span>
        </div>
      )}
      {error && (
        <div className="flex items-center justify-center mt-4 p-3 bg-red-50 text-red-700 rounded-md text-sm font-medium space-x-2">
          <AlertCircle className="h-5 w-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};

export default DropZone;
