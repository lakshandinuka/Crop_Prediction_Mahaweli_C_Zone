import React from 'react';
import { Link, Outlet } from 'react-router-dom';

export default function PublicLayout() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white text-slate-800 flex flex-col">
      <header className="mx-auto w-full max-w-6xl px-6 py-6">
        <nav className="flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-emerald-700">AgriWater AI</Link>
          <div className="flex gap-4 text-sm font-medium">
            <Link to="/predict">Evaporation Predictor</Link>
            <Link to="/crops">Crop Planning</Link>
            <Link to="/water">Water Calculator</Link>
            <Link to="/login">Login</Link>
          </div>
        </nav>
      </header>
      <main className="mx-auto w-full max-w-6xl px-6 pb-16 flex-1">
        <Outlet />
      </main>
      <footer className="border-t border-slate-200 bg-slate-50 mt-auto">
        <div className="mx-auto flex max-w-6xl flex-col gap-2 px-6 py-8 text-sm text-slate-600 md:flex-row md:justify-between">
          <div>Documentation · Data limitations · Contact</div>
          <div>Demo outputs are explicitly labelled and must not be mistaken for real ML predictions.</div>
        </div>
      </footer>
    </div>
  );
}
