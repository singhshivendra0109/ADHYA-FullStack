import React from 'react';
import { Calendar, X, Clock } from 'lucide-react';

const AvailabilityManager = ({ slots, onDelete }) => (
  <div className="space-y-4 text-left">
    {slots.length > 0 ? (
      slots.map((slot) => (
        <div key={slot.id} className="bg-white p-6 md:p-8 rounded-[2rem] md:rounded-[2.5rem] border border-emerald-50 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div className="flex items-center gap-4 md:gap-6">
            <div className="w-12 h-12 md:w-14 md:h-14 bg-emerald-50 rounded-2xl flex items-center justify-center text-[#2D8B8B]">
              <Clock size={24} />
            </div>
            <div>
              <h4 className="text-lg md:text-xl font-black text-[#0F172A]">{slot.time_slot}</h4>
              <p className="text-gray-400 font-bold text-[10px] md:text-xs uppercase tracking-widest">{slot.month_year}</p>
            </div>
          </div>
          <button onClick={() => onDelete(slot.id)} className="text-red-400 hover:bg-red-50 p-3 rounded-xl transition-all">
            <X size={20} />
          </button>
        </div>
      ))
    ) : (
      <div className="p-12 border-2 border-dashed border-emerald-100 rounded-[2.5rem] text-center text-emerald-200">
        <Calendar size={48} className="mx-auto mb-2 opacity-50" />
        <p className="font-black uppercase text-xs">No active slots</p>
      </div>
    )}
  </div>
);

export default AvailabilityManager;