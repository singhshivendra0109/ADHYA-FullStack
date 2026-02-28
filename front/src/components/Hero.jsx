
// export default Hero;
import React, { useState, useEffect } from 'react';
import { Search, Star, Users, Award } from "lucide-react";
import { useNavigate } from 'react-router-dom';
import api from '../api/api'; // Using your existing api instance

const Hero = () => {
  const [query, setQuery] = useState("");
  const navigate = useNavigate();

  // New state for dynamic stats
  const [stats, setStats] = useState({
    total_tutors: 0,
    total_students: 0,
    average_rating: 0
  });

  // Fetch stats from database on load
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/admin/hero-stats');
        setStats(res.data);
      } catch (err) {
        console.error("Failed to fetch platform stats", err);
      }
    };
    fetchStats();
  }, []);

  const handleSearch = () => {
    if (!query.trim()) return;
    
    // 1. Update URL with search param and jump to the tutors section
    navigate(`/?search=${encodeURIComponent(query)}#featured-tutors`);
    
    // 2. Immediate scroll jump
    const element = document.getElementById('featured-tutors');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    /* Adjusted padding: Taller than original, but shorter than the "Grand" version */
    <section className="relative pt-36 pb-20 md:pt-52 md:pb-36 overflow-hidden bg-gradient-to-br from-[#2D8B8B] via-[#1F5F5F] to-[#0F172A] text-white">
      
      {/* Decorative Elements */}
      <div className="absolute top-20 left-10 w-80 h-80 bg-emerald-400/10 rounded-full blur-[100px] animate-pulse hidden md:block" />
      <div className="absolute bottom-10 right-10 w-[400px] h-[400px] bg-black/20 rounded-full blur-[80px]" />

      <div className="container mx-auto px-6 relative z-10 text-center">
        
        {/* Trusted Badge */}
        <div className="inline-flex items-center gap-2.5 px-4 py-2 md:px-5 md:py-2.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 mb-8 md:mb-10 shadow-xl">
          <Star className="w-4 h-4 text-[#F38137]" fill="currentColor" />
          <span className="text-[11px] md:text-sm font-bold tracking-widest uppercase">Connect . Learn . Excel</span>
        </div>

        {/* Headline: Clean and punchy */}
        <h1 className="text-4xl sm:text-5xl md:text-7xl lg:text-8xl font-black mb-6 md:mb-8 leading-[1.1] tracking-tight">
          Find Your Perfect <br className="hidden md:block" /> 
          <span className="text-emerald-300">Tutor Today</span>
        </h1>

        {/* Subheadline: Optimized for readability */}
        <p className="text-base md:text-xl text-white/80 max-w-3xl mx-auto mb-12 md:mb-16 px-4 leading-relaxed">
          Connect with expert tutors in any subject. Personalized learning that fits your schedule, goals, and learning style.
        </p>

        {/* Search Bar: Large and bold, but not oversized */}
        <div className="max-w-4xl mx-auto mb-16 md:mb-24">
          <div className="bg-white rounded-2xl md:rounded-[32px] p-2.5 md:p-3 shadow-2xl flex flex-col md:flex-row gap-2 items-center border border-white/10">
            <div className="flex-1 flex items-center px-4 md:px-6 w-full gap-3 md:gap-4">
              <Search className="w-5 h-5 md:w-7 md:h-7 text-emerald-600" />
              <input 
                type="text" 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Search by tutor name or subject..." 
                className="w-full py-4 md:py-5 bg-transparent text-[#0F172A] outline-none placeholder:text-gray-400 text-base md:text-xl font-bold"
              />
            </div>
            <button 
              onClick={handleSearch}
              className="w-full md:w-auto bg-[#F38137] hover:bg-[#e06d2a] text-white px-10 py-4 md:py-5 rounded-xl md:rounded-[22px] font-black text-base md:text-lg transition-all shadow-lg active:scale-95 uppercase tracking-wider"
            >
              Find Tutors
            </button>
          </div>
          
          <p className="mt-4 md:mt-6 text-white/50 text-xs md:text-sm font-medium">
            Popular: <span className="text-white/80">Mathematics, Physics, English, Coding</span>
          </p>
        </div>

        {/* Stats Grid - Now extracting from DB */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-10 sm:gap-4 max-w-5xl mx-auto pt-12 border-t border-white/10">
          <div className="flex flex-col items-center">
            <div className="flex items-center gap-2 mb-1">
              <Users className="w-6 h-6 md:w-8 md:h-8 text-emerald-400/80" />
              <span className="text-3xl md:text-5xl font-black">{stats.total_tutors}</span>
            </div>
            <p className="text-white/50 text-[10px] md:text-xs uppercase tracking-[3px] font-bold">Expert Tutors</p>
          </div>
          
          <div className="flex flex-col items-center sm:border-x border-white/10 px-4">
            <div className="flex items-center gap-2 mb-1">
              <Star className="w-6 h-6 md:w-8 md:h-8 text-[#F38137]" fill="currentColor" />
              <span className="text-3xl md:text-5xl font-black">{stats.average_rating}</span>
            </div>
            <p className="text-white/50 text-[10px] md:text-xs uppercase tracking-[3px] font-bold">Average Rating</p>
          </div>

          <div className="flex flex-col items-center">
            <div className="flex items-center gap-2 mb-1">
              <Award className="w-6 h-6 md:w-8 md:h-8 text-emerald-400/80" />
              <span className="text-3xl md:text-5xl font-black">{stats.total_students}</span>
            </div>
            <p className="text-white/50 text-[10px] md:text-xs uppercase tracking-[3px] font-bold">Students Joined</p>
          </div>
        </div>

      </div>
    </section>
  );
};

export default Hero;