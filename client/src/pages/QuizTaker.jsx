import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import api from '../api/axios';

export default function QuizTaker() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answers, setAnswers] = useState({});

  const { data: quiz, isLoading } = useQuery({
    queryKey: ['quiz', id],
    queryFn: async () => (await api.get(`/api/quizzes/${id}`)).data
  });

  const submitMutation = useMutation({
    mutationFn: async (payload) => api.post(`/api/quizzes/submit/${id}`, payload),
    onSuccess: (data) => {
      navigate('/results', { state: { result: data.data, quizTitle: quiz.title } });
    }
  });

  if (isLoading) return <div>Loading Quiz...</div>;

  const question = quiz.questions[currentIdx];
  const progress = ((currentIdx + 1) / quiz.questions.length) * 100;

  const handleSelect = (option) => {
    setAnswers(prev => ({ ...prev, [question.id]: option }));
  };

  const handleNext = () => {
    if (currentIdx < quiz.questions.length - 1) {
      setCurrentIdx(currentIdx + 1);
    } else {
      submitMutation.mutate({ answers });
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <div className="mb-6">
        <div className="flex justify-between text-sm text-gray-500 mb-2">
          <span>Question {currentIdx + 1} of {quiz.questions.length}</span>
          <span>{Math.round(progress)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: `${progress}%` }}></div>
        </div>
      </div>

      <div className="bg-white shadow-lg rounded-xl p-8 mb-6">
        <h2 className="text-xl font-bold mb-6">{question.text}</h2>
        <div className="space-y-3">
          {question.options.map((opt) => (
            <div 
              key={opt}
              onClick={() => handleSelect(opt)}
              className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                answers[question.id] === opt 
                  ? 'border-blue-500 bg-blue-50' 
                  : 'border-gray-200 hover:border-blue-300'
              }`}
            >
              {opt}
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-end">
        <button 
          onClick={handleNext}
          className="bg-blue-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-700"
        >
          {currentIdx === quiz.questions.length - 1 ? 'Submit Quiz' : 'Next Question'}
        </button>
      </div>
    </div>
  );
}
