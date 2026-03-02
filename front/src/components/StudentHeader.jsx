
// import React, { useState } from 'react';
// import { GraduationCap, Menu, X, User, LogOut } from "lucide-react";
// import { Link, useLocation, useNavigate } from 'react-router-dom';

// const StudentHeader = () => {
//   const [isMenuOpen, setIsMenuOpen] = useState(false);
//   const location = useLocation();
//   const navigate = useNavigate();

//   // --- THE LOGOUT LOGIC ---
//   const handleLogout = () => {
//     // 1. Clear the session data
//     localStorage.removeItem('token');
//     localStorage.removeItem('role');

//     // 2. Redirect to the public home page
//     navigate('/');
    
//     // 3. Refresh to clear any remaining in-memory state
//     window.location.reload();
//   };

//   const scrollToSection = (e, id) => {
//     e.preventDefault();
//     if (location.pathname !== '/') {
//       navigate('/');
//       setTimeout(() => {
//         executeScroll(id);
//       }, 100);
//     } else {
//       executeScroll(id);
//     }
//   };

//   const executeScroll = (id) => {
//     const element = document.getElementById(id);
//     if (element) {
//       const headerOffset = 120;
//       const elementPosition = element.getBoundingClientRect().top;
//       const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

//       window.scrollTo({
//         top: offsetPosition,
//         behavior: "smooth"
//       });
//     }
//     setIsMenuOpen(false);
//   };

//   const navLinks = [
//     { name: 'Subjects', id: 'subjects' },
//     { name: 'Find Tutors', id: 'featured-tutors' },
//     { name: 'How It Works', id: 'how-it-works' },
//     { name: 'Results', id: 'success-wall' }, 
//     { name: 'Reviews', id: 'reviews' }
//   ];

//   return (
//     <header className="fixed top-0 left-0 right-0 z-50 bg-[#f7fdfd]/80 backdrop-blur-3xl border-b border-white/50">
//       <div className="w-full mx-auto px-6 md:px-10 lg:px-14 xl:px-20">
        
//         <div className="flex items-center justify-between h-20 md:h-24 lg:h-32">
          
//           {/* 1. Logo */}
//           <Link to="/" className="flex items-center gap-3 md:gap-4 flex-shrink-0 group cursor-pointer">
//             <div className="w-10 h-10 md:w-14 md:h-14 lg:w-16 lg:h-16 rounded-xl md:rounded-[22px] bg-[#2D8B8B] flex items-center justify-center shadow-2xl group-hover:scale-110 transition-transform duration-500">
//               <GraduationCap className="w-6 h-6 md:w-8 md:h-8 lg:w-9 lg:h-9 text-white" />
//             </div>
//             <span className="text-xl md:text-3xl lg:text-4xl font-black text-[#1a2e2e] tracking-tighter uppercase">ADHYA</span>
//           </Link>

//           {/* 2. Desktop Nav */}
//           <nav className="hidden xl:flex items-center justify-center gap-10 xxl:gap-16 mx-8">
//             {navLinks.map((link) => (
//               <a 
//                 key={link.name}
//                 href={`#${link.id}`} 
//                 onClick={(e) => scrollToSection(e, link.id)}
//                 className="text-[13px] lg:text-[15px] font-black text-[#4a6363] uppercase tracking-[3px] lg:tracking-[4px] hover:text-[#2D8B8B] transition-all whitespace-nowrap cursor-pointer"
//               >
//                 {link.name}
//               </a>
//             ))}
//           </nav>

//           {/* 3. Action Buttons */}
//           <div className="hidden xl:flex items-center gap-4 lg:gap-6 flex-shrink-0">
            
//             {/* LOGOUT BUTTON */}
//             <button 
//               onClick={handleLogout}
//               className="bg-white/40 border-2 border-red-100 text-red-500 px-8 lg:px-10 py-4 lg:py-5 rounded-[20px] lg:rounded-[24px] font-black uppercase tracking-[2px] text-xs lg:text-sm hover:bg-red-500 hover:text-white transition-all flex items-center gap-2"
//             >
//               <LogOut size={18} /> Logout
//             </button>

//             {/* MY PROFILE BUTTON - Points to /student-profile */}
//             <Link to="/student-profile">
//               <button className="bg-[#2D8B8B] text-white px-8 lg:px-10 py-4 lg:py-5 rounded-[20px] lg:rounded-[24px] font-black uppercase tracking-[2px] text-xs lg:text-sm shadow-xl hover:bg-[#1f6666] transition-all active:scale-95 flex items-center gap-2">
//                 <User size={18} /> My Profile
//               </button>
//             </Link>
//           </div>

//           {/* Mobile Menu Toggle */}
//           <button className="xl:hidden p-3 md:p-5 text-[#2D8B8B] bg-white/80 rounded-2xl border border-white" onClick={() => setIsMenuOpen(!isMenuOpen)}>
//             {isMenuOpen ? <X size={28} /> : <Menu size={28} />}
//           </button>
//         </div>

//         {/* Mobile View */}
//         {isMenuOpen && (
//           <div className="xl:hidden fixed inset-0 bg-white/98 backdrop-blur-3xl z-[100] p-8 md:p-12 flex flex-col justify-center items-center animate-in fade-in zoom-in-95">
//             <button onClick={() => setIsMenuOpen(false)} className="absolute top-6 right-6 md:top-10 md:right-10 text-[#2D8B8B]"><X size={32}/></button>
//             <nav className="flex flex-col gap-8 md:gap-12 text-center w-full">
//               {navLinks.map((link) => (
//                 <a 
//                   key={link.name} 
//                   href="#" 
//                   className="text-xl md:text-3xl font-black uppercase tracking-[4px] text-[#4a6363]" 
//                   onClick={(e) => scrollToSection(e, link.id)}
//                 >
//                   {link.name}
//                 </a>
//               ))}
//               <div className="flex flex-col gap-4 md:gap-6 mt-8 w-full max-w-[400px] mx-auto">
//                 {/* MOBILE LOGOUT */}
//                 <button 
//                    onClick={handleLogout}
//                    className="w-full py-5 md:py-7 text-red-500 font-black border-2 border-red-100 rounded-3xl text-base uppercase flex items-center justify-center gap-2"
//                 >
//                   <LogOut size={20} /> Logout
//                 </button>
//                 {/* MOBILE PROFILE - Points to /student-profile */}
//                 <Link to="/student-profile" onClick={() => setIsMenuOpen(false)} className="w-full">
//                   <button className="w-full bg-[#2D8B8B] text-white py-5 md:py-7 rounded-3xl font-black shadow-2xl text-base uppercase flex items-center justify-center gap-2">
//                     <User size={20} /> My Profile
//                   </button>
//                 </Link>
//               </div>
//             </nav>
//           </div>
//         )}
//       </div>
//     </header>
//   );
// };

// export default StudentHeader;
import React, { useState } from 'react';
import { GraduationCap, Menu, X, User, LogOut } from "lucide-react";
import { Link, useLocation, useNavigate } from 'react-router-dom';

const StudentHeader = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    navigate('/');
    window.location.reload();
  };

  const scrollToSection = (e, id) => {
    e.preventDefault();
    if (location.pathname !== '/') {
      navigate('/');
      setTimeout(() => executeScroll(id), 100);
    } else {
      executeScroll(id);
    }
  };

  const executeScroll = (id) => {
    const element = document.getElementById(id);
    if (element) {
      const headerOffset = 80; // Adjusted for smaller header
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      window.scrollTo({ top: offsetPosition, behavior: "smooth" });
    }
    setIsMenuOpen(false);
  };

  const navLinks = [
    { name: 'Subjects', id: 'subjects' },
    { name: 'Find Tutors', id: 'featured-tutors' },
    { name: 'How It Works', id: 'how-it-works' },
    { name: 'Results', id: 'success-wall' }, 
    { name: 'Reviews', id: 'reviews' }
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#f7fdfd]/90 backdrop-blur-xl border-b border-white/50">
      <div className="w-full mx-auto px-4 md:px-8 lg:px-12">
        
        {/* Header Height Scaled Down (h-16 to h-20 instead of h-32) */}
        <div className="flex items-center justify-between h-20 md:h-24 lg:h-32">
          
          {/* 1. Logo Scaled Down */}
          <Link to="/" className="flex items-center gap-2 md:gap-3 flex-shrink-0 group">
            <div className="w-8 h-8 md:w-10 md:h-10 rounded-lg bg-[#2D8B8B] flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform duration-300">
              <GraduationCap className="w-5 h-5 md:w-6 md:h-6 text-white" />
            </div>
            <span className="text-lg md:text-xl font-black text-[#1a2e2e] tracking-tighter uppercase">ADHYA</span>
          </Link>

          {/* 2. Desktop Nav (Spacing and Font-Size reduced) */}
          <nav className="hidden xl:flex items-center justify-center gap-6 lg:gap-8 mx-4">
            {navLinks.map((link) => (
              <a 
                key={link.name}
                href={`#${link.id}`} 
                onClick={(e) => scrollToSection(e, link.id)}
                className="text-[11px] lg:text-[12px] font-bold text-[#4a6363] uppercase tracking-[2px] hover:text-[#2D8B8B] transition-all whitespace-nowrap"
              >
                {link.name}
              </a>
            ))}
          </nav>

          {/* 3. Action Buttons (Padding and Padding-X reduced) */}
          <div className="hidden xl:flex items-center gap-3">
            
            <button 
              onClick={handleLogout}
              className="bg-white/40 border border-red-100 text-red-500 px-5 py-2.5 rounded-xl font-bold uppercase tracking-[1px] text-[10px] lg:text-[11px] hover:bg-red-500 hover:text-white transition-all flex items-center gap-2"
            >
              <LogOut size={14} /> Logout
            </button>

            <Link to="/student-profile">
              <button className="bg-[#2D8B8B] text-white px-5 py-2.5 rounded-xl font-bold uppercase tracking-[1px] text-[10px] lg:text-[11px] shadow-lg hover:bg-[#1f6666] transition-all active:scale-95 flex items-center gap-2">
                <User size={14} /> My Profile
              </button>
            </Link>
          </div>

          {/* Mobile Menu Toggle */}
          <button className="xl:hidden p-2 text-[#2D8B8B] bg-white/80 rounded-xl border border-white" onClick={() => setIsMenuOpen(!isMenuOpen)}>
            {isMenuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        {/* Mobile View Scaled */}
        {isMenuOpen && (
          <div className="xl:hidden fixed inset-0 bg-white/98 backdrop-blur-3xl z-[100] p-6 flex flex-col justify-center items-center">
            <button onClick={() => setIsMenuOpen(false)} className="absolute top-5 right-5 text-[#2D8B8B]"><X size={24}/></button>
            <nav className="flex flex-col gap-6 text-center w-full">
              {navLinks.map((link) => (
                <a 
                  key={link.name} 
                  href="#" 
                  className="text-lg font-black uppercase tracking-[3px] text-[#4a6363]" 
                  onClick={(e) => scrollToSection(e, link.id)}
                >
                  {link.name}
                </a>
              ))}
              <div className="flex flex-col gap-3 mt-6 w-full max-w-[300px] mx-auto">
                <button 
                   onClick={handleLogout}
                   className="w-full py-4 text-red-500 font-bold border border-red-100 rounded-2xl text-sm uppercase flex items-center justify-center gap-2"
                >
                  <LogOut size={18} /> Logout
                </button>
                <Link to="/student-profile" onClick={() => setIsMenuOpen(false)} className="w-full">
                  <button className="w-full bg-[#2D8B8B] text-white py-4 rounded-2xl font-bold shadow-xl text-sm uppercase flex items-center justify-center gap-2">
                    <User size={18} /> My Profile
                  </button>
                </Link>
              </div>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default StudentHeader;