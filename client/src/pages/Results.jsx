import { useLocation, Link } from 'react-router-dom';
import { CheckCircle, XCircle } from 'lucide-react';

export default function Results() {
  const { state } = useLocation();
  const { result, quizTitle } = state;

  return (
    <div className="max-w-4xl mx-auto p-8">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold mb-2">{quizTitle}</h1>
        <div className="inline-flex items-center justify-center w-32 h-32 rounded-full border-8 border-blue-500 text-3xl font-bold text-blue-600">
          {Math.round(result.percentage)}%
        </div>
        <p className="mt-4 text-gray-500">You scored {result.score} out of {result.analysis.length}</p>
      </div>

      <div className="space-y-4">
        {result.analysis.map((item, idx) => (
          <div key={idx} className={`border rounded-lg p-4 ${item.is_correct ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
            <div className="flex items-start gap-3">
              {item.is_correct ? <CheckCircle className="text-green-600 mt-1" /> : <XCircle className="text-red-600 mt-1" />}
              <div>
                <h3 className="font-semibold text-lg">{item.question_text}</h3>
                <p className="mt-2 text-sm"><span className="font-bold">Your Answer:</span> {item.user_answer}</p>
                {!item.is_correct && (
                  <p className="text-sm text-green-700"><span className="font-bold">Correct Answer:</span> {item.correct_answer}</p>
                )}
                <div className="mt-3 bg-white p-3 rounded text-gray-600 text-sm border">
                  <strong>Explanation:</strong> {item.explanation}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 text-center">
        <Link to="/upload" className="inline-block bg-gray-800 text-white px-6 py-3 rounded-lg">Create Another Quiz</Link>
      </div>
    </div>
  );
}
