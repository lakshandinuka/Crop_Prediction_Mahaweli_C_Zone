import React from 'react';
import { Link, Outlet } from 'react-router-dom';

export default function AdminLayout() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex">
      <aside className="w-64 bg-emerald-900 text-emerald-100 flex flex-col hidden md:flex">
        <div className="p-6 text-xl font-bold text-white border-b border-emerald-800">AgriWater Admin</div>
        <nav className="flex-1 p-4 space-y-2">
          <Link to="/admin" className="block px-4 py-2 rounded bg-emerald-800 text-white">Dashboard</Link>
          <Link to="/admin/users" className="block px-4 py-2 rounded hover:bg-emerald-800">Users</Link>
          <Link to="/admin/system" className="block px-4 py-2 rounded hover:bg-emerald-800">System Logs</Link>
        </nav>
        <div className="p-4 border-t border-emerald-800">
          <Link to="/" className="block px-4 py-2 rounded hover:bg-emerald-800 text-sm">Sign out</Link>
        </div>
      </aside>
      <main className="flex-1 p-8">
        <Outlet />
      </main>
    </div>
  );
}
