
// export default App;
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import StudentHeader from './components/StudentHeader'; 
import TeacherHeader from './components/teacher/TeacherHeader';
import Home from './pages/Home';
import SignUp from './pages/SignUp';
import Login from './pages/Login';
import StudentDashboard from './pages/StudentDashboard'; 
import TeacherDashboard from './pages/TeacherDashboard'; 
import TutorProfile from './pages/TutorProfile'; 
import AdminDashboard from './pages/AdminDashboard';
// 1. IMPORT YOUR NEW STUDENT PROFILE PAGE
import StudentProfile from './pages/StudentProfile'; 

function App() {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');
  
  const isStudent = token && role === 'student';
  const isTeacher = token && role === 'teacher';

  return (
    <Router>
      <div className="min-h-screen bg-white">
        {/* Dynamic Header Selection */}
        {isStudent ? (
          <StudentHeader />
        ) : isTeacher ? (
          <TeacherHeader />
        ) : (
          <Header />
        )}
        
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/login" element={<Login />} />
          
          <Route path="/student-dashboard" element={<StudentDashboard />} />
          
          {/* 2. ADD THIS ROUTE TO CONNECT THE "MY PROFILE" BUTTON */}
          <Route path="/student-profile" element={<StudentProfile />} />
          
          <Route path="/teacher-dashboard" element={<TeacherDashboard />} />
          <Route path="/tutor/:id" element={<TutorProfile />} />
          <Route path="/admin-dashboard" element={<AdminDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;