import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { Upload, Loader2, CheckCircle } from 'lucide-react';
import api from '../api/axios';

const steps = ["Parsing PDF", "Generating Questions (AI)", "Validating Logic", "Finalizing"];

export default function UploadQuiz() {
  const [file, setFile] = useState(null);
  const [loadingStep, setLoadingStep] = useState(0);
  const navigate = useNavigate();

  const generateMutation = useMutation({
    mutationFn: async (formData) => {
      // Simulate steps for UX
      const interval = setInterval(() => {
        setLoadingStep((prev) => (prev < 3 ? prev + 1 : prev));
      }, 1000);
      
      const res = await api.post('/api/quizzes/generate', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      clearInterval(interval);
      return res.data;
    },
    onSuccess: (data) => {
      navigate(`/quiz/${data.id}`);
    },
  });

  const handleUpload = () => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    generateMutation.mutate(formData);
  };

  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">Create New Quiz</h1>
      
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-500 transition-colors">
        <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <input 
          type="file" 
          accept=".pdf" 
          onChange={(e) => setFile(e.target.files[0])}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
        <p className="mt-2 text-sm text-gray-500">{file ? file.name : "Drag PDF here"}</p>
      </div>

      {generateMutation.isPending && (
        <div className="mt-8 space-y-4">
          {steps.map((step, idx) => (
            <div key={idx} className={`flex items-center space-x-3 ${idx <= loadingStep ? 'text-blue-600' : 'text-gray-300'}`}>
              {idx < loadingStep ? <CheckCircle className="h-5 w-5" /> : idx === loadingStep ? <Loader2 className="h-5 w-5 animate-spin" /> : <div className="h-5 w-5 rounded-full border-2" />}
              <span className="font-medium">{step}</span>
            </div>
          ))}
        </div>
      )}

      <button 
        onClick={handleUpload}
        disabled={!file || generateMutation.isPending}
        className="mt-6 w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400"
      >
        {generateMutation.isPending ? 'Processing...' : 'Generate Quiz'}
      </button>
    </div>
  );
}
