import React, { useState } from 'react';
import { GraduationCap, Mail, Lock, ArrowRight } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/api';

const SignUp = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    role: 'student' 
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      // Sends { "email": "...", "password": "...", "role": "student" OR "teacher" }
      const response = await api.post('/users/', {
        email: formData.email,
        password: formData.password,
        role: formData.role
      });
      
      console.log("Registration Successful:", response.data);
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.detail || "Connection failed. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f1fcf9] flex items-center justify-center p-4 md:p-8 lg:p-12">
      
      <div className="w-full max-w-[550px] bg-white rounded-[2.5rem] md:rounded-[3.5rem] shadow-[0_30px_60px_-15px_rgba(16,185,129,0.15)] border border-emerald-50 p-10 md:p-16">
        
        {/* Branding Section */}
        <div className="flex flex-col items-center mb-12">
          <div className="w-16 h-16 md:w-20 md:h-20 rounded-[1.5rem] bg-[#2D8B8B] flex items-center justify-center mb-6 shadow-2xl shadow-emerald-900/20 hover:scale-105 transition-transform duration-500">
            <GraduationCap className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl md:text-4xl font-black text-[#0F172A] tracking-tighter uppercase text-center leading-tight">
            Create Account
          </h1>
          <p className="text-[#2D8B8B] font-black mt-3 uppercase tracking-[4px] text-[10px] md:text-xs text-center">
            Start your journey with ADHYA
          </p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-5 rounded-2xl mb-8 text-sm font-bold border border-red-100 text-center animate-shake">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          
          {/* Role Selection: Updates state to 'teacher' when Tutor is clicked */}
          <div className="flex flex-col sm:flex-row gap-4 mb-10">
            <button
              type="button"
              onClick={() => setFormData({ ...formData, role: 'student' })}
              className={`flex-1 py-5 md:py-6 rounded-2xl font-black uppercase tracking-[3px] text-[10px] md:text-[12px] border-2 transition-all duration-300 ${
                formData.role === 'student' 
                ? 'bg-[#2D8B8B] border-[#2D8B8B] text-white shadow-xl shadow-teal-900/20' 
                : 'bg-emerald-50/30 border-transparent text-[#4a6363] hover:border-[#2D8B8B]/30'
              }`}
            >
              I'm a Student
            </button>
            <button
              type="button"
              // CHANGED: Sets role to 'teacher' for the database while keeping button text as 'Tutor'
              onClick={() => setFormData({ ...formData, role: 'teacher' })}
              className={`flex-1 py-5 md:py-6 rounded-2xl font-black uppercase tracking-[3px] text-[10px] md:text-[12px] border-2 transition-all duration-300 ${
                formData.role === 'teacher' 
                ? 'bg-[#2D8B8B] border-[#2D8B8B] text-white shadow-xl shadow-teal-900/20' 
                : 'bg-emerald-50/30 border-transparent text-[#4a6363] hover:border-[#2D8B8B]/30'
              }`}
            >
              I'm a Tutor
            </button>
          </div>

          {/* Email Input */}
          <div className="relative group">
            <Mail className="absolute left-6 top-1/2 -translate-y-1/2 text-[#2D8B8B] group-focus-within:scale-110 transition-transform" size={22} />
            <input
              type="email"
              placeholder="Email Address"
              required
              className="w-full pl-16 pr-8 py-5 md:py-6 bg-emerald-50/30 border-2 border-transparent rounded-[1.5rem] focus:bg-white focus:border-[#2D8B8B]/20 outline-none transition-all font-bold text-[#0F172A] text-base md:text-lg"
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            />
          </div>

          {/* Password Input */}
          <div className="relative group">
            <Lock className="absolute left-6 top-1/2 -translate-y-1/2 text-[#2D8B8B] group-focus-within:scale-110 transition-transform" size={22} />
            <input
              type="password"
              placeholder="Create Password"
              required
              className="w-full pl-16 pr-8 py-5 md:py-6 bg-emerald-50/30 border-2 border-transparent rounded-[1.5rem] focus:bg-white focus:border-[#2D8B8B]/20 outline-none transition-all font-bold text-[#0F172A] text-base md:text-lg"
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#2D8B8B] text-white py-6 md:py-7 rounded-[1.5rem] md:rounded-[2rem] font-black uppercase tracking-[4px] text-xs md:text-sm shadow-2xl shadow-teal-900/40 hover:bg-[#1f6666] hover:-translate-y-1.5 transition-all flex items-center justify-center gap-4 mt-8 active:scale-95 disabled:opacity-50"
          >
            {loading ? "Creating Account..." : "Create Free Account"}
            {!loading && <ArrowRight size={20} className="hidden sm:block" />}
          </button>
        </form>

        <p className="text-center mt-12 text-gray-400 font-bold text-sm">
          Joined us before?{' '}
          <Link to="/login" className="text-[#2D8B8B] font-black uppercase tracking-widest hover:underline decoration-2 underline-offset-8">
            Sign In here
          </Link>
        </p>
      </div>
    </div>
  );
};

export default SignUp;