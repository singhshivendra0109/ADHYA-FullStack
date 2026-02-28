import React from 'react';
import Hero from '../components/Hero';
import SubjectSlider from '../components/SubjectSlider';
import HowItWorks from '../components/HowItWorks';
import FeaturedTutors from '../components/FeaturedTutors';
import SuccessWall from '../components/SuccessWall'; 
import Footer from '../components/Footer';          
import ReviewSlider from '../components/ReviewSlider';    

const Home = () => {
  return (
    // overflow-hidden prevents horizontal jitter on mobile swipes
    <main className="overflow-hidden bg-[#f7fdfd]">
      
      {/* 1. Header & Search (Impact Section) 
          Responsive Note: Hero handle its own pt-32 to clear the fixed Header */}
      <Hero />
      
      {/* 2. Categories Slider
          Added a subtle container-level padding for mobile flow */}
      <div className="bg-white border-y border-gray-100/50">
        <SubjectSlider />
      </div>
      
      {/* 3. The Onboarding Flow (Steps 01-04)
          Responsive Note: Stacks vertically on mobile automatically */}
      <HowItWorks />
      
      {/* 4. Live Teacher Data 
          Connected to FastAPI - Grid adjusts 1 to 4 columns */}
      <div className="bg-gray-50/30">
        <FeaturedTutors />
      </div>
      
      {/* 5. Social Proof (Testimonials)
          Centered on mobile for better readability */}
      <SuccessWall />
      
      {/* 6. Site Navigation & Final CTA
          CTA buttons become full-width on mobile */}

      <ReviewSlider/>
      
      <Footer />
    </main>
  );
};

export default Home;    