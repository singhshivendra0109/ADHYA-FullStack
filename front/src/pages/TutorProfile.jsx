
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/api';
import { Clock, ArrowLeft, Star, MapPin, Award, User, ShieldCheck } from 'lucide-react';

const TutorProfile = () => {
  const { id } = useParams(); 
  const [tutor, setTutor] = useState(null);
  const [slots, setSlots] = useState([]);
  const [userBookings, setUserBookings] = useState([]); 
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // STEP 1: Fetch Profile Details via User ID
        const profileRes = await api.get(`/profiles/user/${id}`);
        const profileData = profileRes.data;
        setTutor(profileData);

        // STEP 2: Fetch Availability for this specific mentor
        const slotsRes = await api.get(`/profiles/availability/${profileData.user_id}`, {
            params: { month_year: "March 2026" } 
        });
        setSlots(slotsRes.data);

        // STEP 3: Fetch current student's bookings to check slot status
        const bookingsRes = await api.get('/bookings/my-bookings');
        setUserBookings(bookingsRes.data);

      } catch (err) {
        console.error("Data Sync Failed:", err.response?.data || err.message);
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchData();
  }, [id]);

  // ACTION: Withdraw a pending request
  const handleWithdraw = async (bookingId) => {
    if (!window.confirm("Are you sure you want to withdraw this request?")) return;
    try {
      await api.delete(`/bookings/${bookingId}`);
      alert("Request Withdrawn.");
      window.location.reload(); 
    } catch (err) {
      alert("Withdraw failed. Request might already be processed.");
    }
  };

  // ACTION: Create a new booking request
  const handleBooking = async (slot) => {
    try {
      await api.post('/bookings/', {
        teacher_id: tutor.user_id,
        subject: tutor.subject,
        month_year: slot.month_year,
        time_slot: slot.time_slot
      });
      alert("Booking Request Sent! Mentor will review your request.");
      window.location.reload(); 
    } catch (err) {
      const detail = err.response?.data?.detail;
      alert(detail || "Only student accounts can book mentors.");
    }
  };

  // HELPER: Map time slots to current booking status
  const getSlotStatus = (timeSlot) => {
    const booking = userBookings.find(b => b.time_slot === timeSlot && b.teacher_id === tutor.user_id);
    return booking ? { status: booking.status, id: booking.id } : null;
  };

  if (loading) return (
    <div className="h-screen flex items-center justify-center bg-[#fcfefd]">
      <div className="flex flex-col items-center gap-4">
        <div className="w-12 h-12 border-4 border-[#1F6666] border-t-transparent rounded-full animate-spin"></div>
        <p className="font-black text-[#1F6666] uppercase tracking-[4px] text-[10px]">Syncing Mentor Intelligence...</p>
      </div>
    </div>
  );

  if (!tutor) return (
    <div className="h-screen flex flex-col items-center justify-center bg-white text-center">
        <p className="font-black text-red-500 uppercase tracking-widest mb-4 text-sm">Mentor Profile Not Found</p>
        <button onClick={() => window.history.back()} className="text-[10px] font-black uppercase underline tracking-widest">Return to Discovery</button>
    </div>
  );

  return (
    <div className="min-h-screen bg-[#fcfefd] pb-24 text-left font-sans">
      <div className="max-w-7xl mx-auto px-6 pt-12">
        
        {/* Navigation */}
        <button 
          onClick={() => window.history.back()} 
          className="flex items-center gap-2 font-black text-[#0F172A] uppercase text-[10px] tracking-widest mb-12 hover:text-[#1F6666] transition-all group"
        >
          <ArrowLeft size={16} className="group-hover:-translate-x-1 transition-transform" /> Back to Discovery
        </button>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-16">
          
          {/* LEFT SIDE: Details & Slots */}
          <div className="lg:col-span-8">
            <h1 className="text-5xl md:text-7xl font-black text-[#0F172A] leading-[1.1] mb-8 uppercase tracking-tighter">
              {tutor.subject} Mastery <br /> Starts <span className="text-[#1F6666]">Here</span>.
            </h1>

            <div className="flex flex-wrap gap-4 mb-12">
               <div className="flex items-center gap-2 px-6 py-3 bg-white rounded-2xl border border-gray-100 font-bold text-[#0F172A]">
                  <MapPin size={18} className="text-[#1F6666]" /> {tutor.city || "Remote Learning"}
               </div>
               <div className="flex items-center gap-2 px-6 py-3 bg-white rounded-2xl border border-gray-100 font-bold text-[#0F172A]">
                  <Award size={18} className="text-[#F38137]" /> {tutor.experience_years} Years Experience
               </div>
            </div>

            <section className="mb-20">
               <h3 className="text-3xl font-black text-[#0F172A] uppercase mb-8">About the Mentor</h3>
               <div className="border-l-4 border-emerald-100 pl-8 text-left">
                 <p className="text-xl md:text-2xl text-gray-600 font-medium leading-relaxed italic">
                    "{tutor.bio || "A dedicated professional mentor focused on your personalized growth and success."}"
                 </p>
               </div>
            </section>

            {/* ENHANCED SCHEDULE BOXES */}
            <section className="mb-20">
               <h3 className="text-3xl font-black text-[#0F172A] uppercase mb-8">Schedule <span className="text-[#1F6666]">Sessions</span></h3>
               <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {slots.length > 0 ? slots.map((slot) => {
                    const bookingInfo = getSlotStatus(slot.time_slot);
                    return (
                      <div key={slot.id} className="bg-white p-8 rounded-[3rem] border border-gray-100 flex items-center justify-between transition-all shadow-sm hover:shadow-md hover:border-[#1F6666]/20 group">
                        <div className="text-left">
                          <p className="font-black text-[#1F6666] uppercase text-[11px] tracking-[2px] mb-2">{slot.month_year}</p>
                          <p className="text-[#0F172A] font-black text-xl uppercase tracking-tighter">{slot.time_slot}</p>
                        </div>
                        <div className="flex flex-col items-end">
                        {!bookingInfo ? (
                          <button 
                            onClick={() => handleBooking(slot)} 
                            className="bg-[#1F6666] text-white px-8 py-4 rounded-[1.5rem] font-black text-[11px] uppercase tracking-widest hover:bg-[#0F172A] transition-all shadow-lg active:scale-95"
                          >
                            Book Now
                          </button>
                        ) : bookingInfo.status === 'accepted' ? (
                          <div className="bg-emerald-50 text-emerald-600 px-8 py-4 rounded-[1.5rem] font-black text-[11px] uppercase tracking-widest border border-emerald-100 flex items-center gap-2">
                            <ShieldCheck size={16}/> Booked
                          </div>
                        ) : (
                          <div className="flex flex-col gap-3 items-center">
                             <span className="text-orange-500 font-black text-[10px] uppercase tracking-widest px-4 py-1 bg-orange-50 rounded-full">Requested</span>
                             <button 
                              onClick={() => handleWithdraw(bookingInfo.id)} 
                              className="bg-red-50 text-red-500 px-6 py-3 rounded-2xl font-black text-[10px] uppercase tracking-widest border border-red-100 hover:bg-red-500 hover:text-white transition-all shadow-sm"
                             >
                               Withdraw
                             </button>
                          </div>
                        )}
                        </div>
                      </div>
                    );
                  }) : <div className="col-span-full py-16 text-center text-gray-400 font-bold uppercase text-xs tracking-widest border-2 border-dashed border-gray-100 rounded-[3rem]">No sessions available for this period.</div>}
               </div>
            </section>
          </div>

          {/* RIGHT SIDEBAR: Profile Identity */}
          <div className="lg:col-span-4 lg:sticky lg:top-12 h-fit text-left">
            <div className="bg-[#f0f9f9] p-10 rounded-[4rem] shadow-xl border border-[#1F6666]/10 flex flex-col items-center">
               
               <div className="relative w-48 h-48 mb-8">
                  {tutor.profile_picture ? (
                    <img src={tutor.profile_picture} className="w-full h-full object-cover rounded-[3.5rem] border-4 border-white shadow-xl" alt={tutor.full_name}/>
                  ) : (
                    <div className="w-full h-full bg-[#1F6666]/10 rounded-[3.5rem] flex items-center justify-center text-[#1F6666]"><User size={64} /></div>
                  )}
                  <div className="absolute -bottom-2 -right-2 bg-[#F38137] text-white p-4 rounded-2xl shadow-lg border-4 border-white">
                    <Star size={24} className="fill-white" />
                  </div>
               </div>

               <h2 className="text-4xl font-black uppercase mb-2 text-center text-[#1F6666] tracking-tighter leading-none">{tutor.full_name}</h2>
               
               <div className="flex items-center gap-2 mb-10">
                  <Star size={16} className="text-orange-500 fill-orange-500" />
                  <span className="font-black text-lg text-[#0F172A]">{tutor.average_rating || "5.0"}</span>
                  <span className="text-gray-400 font-bold text-[10px] uppercase tracking-widest">({tutor.total_reviews || 0} Reviews)</span>
               </div>

               <div className="w-full space-y-6 text-left">
                  <div className="flex justify-between items-center py-4 border-b border-[#1F6666]/10">
                    <span className="text-gray-400 font-black uppercase text-[10px] tracking-widest">Monthly Rate</span>
                    <span className="text-3xl font-black text-[#1F6666]">₹{tutor.monthly_rate}</span>
                  </div>
                  <div className="flex justify-between items-center py-4 border-b border-[#1F6666]/10">
                    <span className="text-gray-400 font-black uppercase text-[10px] tracking-widest">Experience</span>
                    <span className="text-lg font-black text-[#0F172A]">{tutor.experience_years} Yrs</span>
                  </div>
               </div>
               
               <div className="mt-10 p-6 bg-white rounded-3xl border border-[#1F6666]/10 w-full text-center">
                  <p className="text-[10px] font-black uppercase tracking-widest text-[#1F6666] mb-1">Mentor Status</p>
                  <p className="text-xs font-bold uppercase tracking-widest text-[#0F172A]">Verified Expert</p>
               </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default TutorProfile;