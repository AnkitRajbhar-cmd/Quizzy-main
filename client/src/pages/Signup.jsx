import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/axios';

export default function Signup(){
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try{
      await api.post('/auth/signup', { email, password, full_name: fullName });
      navigate('/login');
    }catch(err){
      alert('Signup failed');
    }finally{
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">Create account</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input value={fullName} onChange={(e)=>setFullName(e.target.value)} placeholder="Full name" className="w-full p-3 border rounded" />
        <input value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="Email" className="w-full p-3 border rounded" />
        <input value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="Password" type="password" className="w-full p-3 border rounded" />
        <button className="w-full bg-blue-600 text-white py-3 rounded" disabled={loading}>{loading ? 'Creating...' : 'Create account'}</button>
      </form>
      <p className="mt-4 text-sm">Already have an account? <Link to="/login" className="text-blue-600">Sign in</Link></p>
    </div>
  );
}
