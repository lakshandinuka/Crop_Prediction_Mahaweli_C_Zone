import React from 'react';
import { Link, Outlet } from 'react-router-dom';

export default function SpecialistLayout() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex">
      <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col hidden md:flex">
        <div className="p-6 text-xl font-bold text-white border-b border-slate-800">AgriWater AI</div>
        <nav className="flex-1 p-4 space-y-2">
          <Link to="/specialist" className="block px-4 py-2 rounded bg-slate-800 text-white">Dashboard</Link>
          <Link to="/specialist/crops" className="block px-4 py-2 rounded hover:bg-slate-800">Crop Data</Link>
          <Link to="/specialist/reports" className="block px-4 py-2 rounded hover:bg-slate-800">Reports</Link>
        </nav>
        <div className="p-4 border-t border-slate-800">
          <Link to="/" className="block px-4 py-2 rounded hover:bg-slate-800 text-sm">Sign out</Link>
        </div>
      </aside>
      <main className="flex-1 p-8">
        <Outlet />
      </main>
    </div>
  );
}
