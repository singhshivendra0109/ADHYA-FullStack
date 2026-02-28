

import React, { useState } from 'react';
import { GraduationCap, Mail, Lock, ArrowRight, Eye, EyeOff } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/api';

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // 1. Prepare form data for FastAPI OAuth2
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      // 2. Updated Endpoint: Removed extra '/api' to match api.js baseURL
      const response = await api.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

      // 3. Store the token and role
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('role', response.data.role);

      // 4. Role-Based Redirect (Updated with Admin logic)
      const userRole = response.data.role;
      
      if (userRole === 'admin') {
        // Direct redirection to Admin Dashboard
        navigate('/admin-dashboard');
      } else if (userRole === 'teacher') {
        navigate('/teacher-dashboard');
      } else if (userRole === 'student') {
        navigate('/student-dashboard');
      } else {
        navigate('/');
      }

      // 5. Force refresh to update the App Header
      window.location.reload();

    } catch (err) {
      setError(err.response?.data?.detail || "Invalid Credentials. Check your email or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f1fcf9] flex items-center justify-center p-4 md:p-8 lg:p-12">
      <div className="w-full max-w-[550px] bg-white rounded-[2.5rem] md:rounded-[3.5rem] shadow-[0_30px_60px_-15px_rgba(16,185,129,0.15)] border border-emerald-50 p-10 md:p-16">
        
        <div className="flex flex-col items-center mb-12">
          <Link to="/" className="w-16 h-16 md:w-20 md:h-20 rounded-[1.5rem] bg-[#2D8B8B] flex items-center justify-center mb-8 shadow-2xl shadow-emerald-900/20 hover:scale-105 transition-transform duration-500">
            <GraduationCap className="w-10 h-10 text-white" />
          </Link>
          <h1 className="text-3xl md:text-4xl font-black text-[#0F172A] tracking-tighter uppercase text-center leading-tight">
            Welcome Back
          </h1>
          <p className="text-[#2D8B8B] font-black mt-3 uppercase tracking-[4px] text-[10px] md:text-xs text-center">
            Enter your ADHYA credentials
          </p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-5 rounded-2xl mb-8 text-sm font-bold border border-red-100 text-center animate-shake">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="relative group">
            <Mail className="absolute left-6 top-1/2 -translate-y-1/2 text-[#2D8B8B] group-focus-within:scale-110 transition-transform" size={22} />
            <input
              type="email"
              placeholder="Email Address"
              required
              value={email}
              className="w-full pl-16 pr-8 py-5 md:py-6 bg-emerald-50/30 border-2 border-transparent rounded-[1.5rem] focus:bg-white focus:border-[#2D8B8B]/20 outline-none transition-all font-bold text-[#0F172A] text-base md:text-lg"
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="relative group">
            <Lock className="absolute left-6 top-1/2 -translate-y-1/2 text-[#2D8B8B] group-focus-within:scale-110 transition-transform" size={22} />
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Enter Password"
              required
              value={password}
              className="w-full pl-16 pr-16 py-5 md:py-6 bg-emerald-50/30 border-2 border-transparent rounded-[1.5rem] focus:bg-white focus:border-[#2D8B8B]/20 outline-none transition-all font-bold text-[#0F172A] text-base md:text-lg"
              onChange={(e) => setPassword(e.target.value)}
            />
            <button 
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-6 top-1/2 -translate-y-1/2 text-gray-400 hover:text-[#2D8B8B] transition-colors p-2"
            >
              {showPassword ? <EyeOff size={22} /> : <Eye size={22} />}
            </button>
          </div>

          <div className="flex justify-end px-4">
            <button type="button" className="text-xs md:text-sm font-black text-[#2D8B8B] uppercase tracking-widest hover:underline decoration-2 underline-offset-4">
              Forgot Password?
            </button>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#2D8B8B] text-white py-6 md:py-7 rounded-[1.5rem] md:rounded-[2rem] font-black uppercase tracking-[4px] text-xs md:text-sm shadow-2xl shadow-teal-900/40 hover:bg-[#1f6666] hover:-translate-y-1.5 transition-all flex items-center justify-center gap-4 mt-6 active:scale-95 disabled:opacity-50"
          >
            {loading ? "Authenticating..." : "Login to Account"}
            {!loading && <ArrowRight size={20} />}
          </button>
        </form>

        <p className="text-center mt-12 text-gray-400 font-bold text-sm">
          New to the platform?{' '}
          <Link to="/signup" className="text-[#2D8B8B] font-black uppercase tracking-widest hover:underline decoration-2 underline-offset-8">
            Join Adhya
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Login;