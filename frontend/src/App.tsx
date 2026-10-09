import React, { useState, useEffect } from 'react';
import { BrowserRouter, Link, Navigate, Route, Routes } from 'react-router-dom';
import PublicLayout from './layouts/PublicLayout';
import SpecialistLayout from './layouts/SpecialistLayout';
import AdminLayout from './layouts/AdminLayout';
import api from './services/api';

function LandingPage() {
  const [modelStatus, setModelStatus] = useState<any>(null);

  useEffect(() => {
    api.get('/evaporation/model-status')
      .then((res) => setModelStatus(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <section className="grid gap-10 py-12 md:grid-cols-2 md:items-center">
      <div>
        <p className="mb-4 inline-flex rounded-full bg-emerald-100 px-3 py-1 text-sm font-semibold text-emerald-700">Agricultural decision support</p>
        <h1 className="text-4xl font-bold tracking-tight text-slate-900 md:text-6xl">Smarter irrigation and crop planning for every season.</h1>
        <p className="mt-6 max-w-xl text-lg text-slate-600">AgriWater AI helps farmers, agronomists, and extension teams assess evaporation, compare crop options, and screen daily water demand with clear, defensible calculations.</p>
        <div className="mt-8 flex gap-4">
          <Link to="/predict" className="rounded-lg bg-emerald-600 px-5 py-3 font-semibold text-white shadow hover:bg-emerald-700">Open evaporation predictor</Link>
          <Link to="/crops" className="rounded-lg border border-slate-300 px-5 py-3 font-semibold text-slate-700 hover:bg-slate-50">Plan crops</Link>
        </div>
      </div>
      <div className="rounded-2xl border border-emerald-100 bg-white p-6 shadow-lg">
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="rounded-xl bg-emerald-50 p-4">
            <div className="text-sm text-slate-500">Demo prediction</div>
            <div className="mt-2 text-3xl font-bold text-emerald-700">4.8 mm/day</div>
          </div>
          <div className="rounded-xl bg-amber-50 p-4">
            <div className="text-sm text-slate-500">Crop water demand</div>
            <div className="mt-2 text-3xl font-bold text-amber-700">5.2 mm/day</div>
          </div>
          <div className="rounded-xl bg-sky-50 p-4 sm:col-span-2">
            <div className="text-sm text-slate-500">Model status</div>
            <div className="mt-2 text-lg font-semibold text-sky-700">
              {modelStatus ? `${modelStatus.provider_type === 'mock' ? 'Mock provider active' : 'Real model active'} (${modelStatus.model_version})` : 'Loading...'}
            </div>
          </div>
        </div>
      </div>
      <div className="mt-16 grid gap-6 md:grid-cols-3 md:col-span-2">
        {[
          ['Weather-driven planning', 'Estimate daily evaporation to inform irrigation and crop selection.'],
          ['Crop suitability', 'Compare crops by season, location, rainfall, and agronomic conditions.'],
          ['Water screening', 'Estimate crop water demand and simplified net irrigation needs.'],
        ].map(([title, text]) => (
          <div key={title} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-3 text-lg font-semibold text-slate-900">{title}</div>
            <p className="text-slate-600">{text}</p>
          </div>
        ))}
      </div>
    </section>
  )
}


function PredictPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    const formData = new FormData(e.currentTarget);
    const payload = {
      observation_date: formData.get('observation_date'),
      location: formData.get('location'),
      rainfall_mm: Number(formData.get('rainfall_mm')),
      temperature_c: Number(formData.get('temperature_c')),
      humidity_pct: Number(formData.get('humidity_pct')),
      sunshine_hours: Number(formData.get('sunshine_hours')),
      soil_temperature_c: Number(formData.get('soil_temperature_c')),
      wind_speed_kmh: Number(formData.get('wind_speed_kmh')),
      pressure_hpa: Number(formData.get('pressure_hpa')),
      input_type: 'manual'
    };

    try {
      const { data } = await api.post('/evaporation/predict', payload);
      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred during prediction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-3xl border border-emerald-200 bg-white p-8 shadow-lg max-w-4xl mx-auto mt-12">
      <h2 className="text-3xl font-bold text-slate-900">Evaporation predictor</h2>
      <p className="mt-2 text-slate-600">Enter meteorological conditions and receive a clear prediction result with provider labeling.</p>
      <form className="mt-6 grid gap-4 md:grid-cols-2" onSubmit={handleSubmit}>
        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Observation date
          <input name="observation_date" type="date" className="rounded-lg border border-slate-300 px-3 py-2" defaultValue="2025-03-15" required />
        </label>
        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Location
          <input name="location" type="text" className="rounded-lg border border-slate-300 px-3 py-2" defaultValue="Anuradhapura" required />
        </label>
        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Rainfall (mm)
          <input name="rainfall_mm" type="number" step="0.1" className="rounded-lg border border-slate-300 px-3 py-2" defaultValue={15} required />
        </label>
        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Air temperature (°C)
          <input name="temperature_c" type="number" step="0.1" className="rounded-lg border border-slate-300 px-3 py-2" defaultValue={30} required />
        </label>
        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Relative humidity (%)
          <input name="humidity_pct" type="number" step="0.1" className="rounded-lg border border-slate-300 px-3 py-2" defaultValue={65} required />
        </label>
        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Sunshine duration (hours)
          <input name="sunshine_hours" type="number" step="0.1" className="rounded-lg border border-slate-300 px-3 py-2" defaultValue={8} required />
        </label>
        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Soil temperature (°C)
          <input name="soil_temperature_c" type="number" step="0.1" className="rounded-lg border border-slate-300 px-3 py-2" defaultValue={29} required />
        </label>
        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Wind speed (km/h)
          <input name="wind_speed_kmh" type="number" step="0.1" className="rounded-lg border border-slate-300 px-3 py-2" defaultValue={8} required />
        </label>
        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700 md:col-span-2">
          Atmospheric pressure (hPa)
          <input name="pressure_hpa" type="number" step="0.1" className="rounded-lg border border-slate-300 px-3 py-2" defaultValue={1012} required />
        </label>
        
        <button type="submit" disabled={loading} className="mt-6 rounded-lg bg-emerald-600 px-5 py-3 font-semibold text-white hover:bg-emerald-700 md:col-span-2 disabled:opacity-50">
          {loading ? 'Predicting...' : 'Run prediction'}
        </button>
      </form>
      
      {error && <div className="mt-4 p-4 text-red-700 bg-red-50 rounded-lg">{error}</div>}

      {result && (
        <div className="mt-8 rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <div className="text-sm font-medium uppercase tracking-wide text-amber-700">Prediction result</div>
          <div className="mt-2 text-4xl font-bold text-amber-800">{result.value} {result.unit}</div>
          <p className="mt-2 text-sm text-amber-900">Source: {result.provider_type === 'mock' ? 'DEMO mock provider — not a scientific ML prediction.' : result.explanation}</p>
        </div>
      )}
    </div>
  )
}

function CropPlanningPage() {
  return (
    <div className="mx-auto max-w-5xl px-6 py-12">
      <h2 className="text-3xl font-bold text-slate-900">Crop recommendation</h2>
      <div className="mt-6 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="grid gap-4 md:grid-cols-2">
            <input placeholder="Location" className="rounded-lg border border-slate-300 px-3 py-2" />
            <input placeholder="Planting date" type="date" className="rounded-lg border border-slate-300 px-3 py-2" />
            <input placeholder="Season" defaultValue="Yala" className="rounded-lg border border-slate-300 px-3 py-2" />
            <input placeholder="Soil type" defaultValue="Loam" className="rounded-lg border border-slate-300 px-3 py-2" />
            <input placeholder="Water availability (mm)" className="rounded-lg border border-slate-300 px-3 py-2" />
            <input placeholder="Field size (ha)" className="rounded-lg border border-slate-300 px-3 py-2" />
          </div>
          <button className="mt-5 rounded-lg bg-emerald-600 px-5 py-3 font-semibold text-white">Get recommendations</button>
        </div>
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
          <h3 className="text-xl font-semibold text-slate-900">Candidate crops</h3>
          <ul className="mt-4 space-y-3">
            <li className="rounded-xl bg-white p-3">Rice · 88% · Maha</li>
            <li className="rounded-xl bg-white p-3">Maize · 81% · Yala</li>
            <li className="rounded-xl bg-white p-3">Chilli · 74% · Yala</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

function WaterPage() {
  return (
    <div className="mx-auto max-w-4xl px-6 py-12">
      <h2 className="text-3xl font-bold text-slate-900">Crop-water calculator</h2>
      <div className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="grid gap-4 md:grid-cols-2">
          <input placeholder="Crop" defaultValue="Rice" className="rounded-lg border border-slate-300 px-3 py-2" />
          <input placeholder="Growth stage" defaultValue="Mid-season" className="rounded-lg border border-slate-300 px-3 py-2" />
          <input placeholder="ETc (mm/day)" defaultValue="5" className="rounded-lg border border-slate-300 px-3 py-2" />
          <input placeholder="Effective rainfall (mm/day)" defaultValue="2" className="rounded-lg border border-slate-300 px-3 py-2" />
          <input placeholder="Field area (m²)" defaultValue="1000" className="rounded-lg border border-slate-300 px-3 py-2" />
          <input placeholder="Irrigation efficiency (%)" defaultValue="70" className="rounded-lg border border-slate-300 px-3 py-2" />
        </div>
        <div className="mt-6 rounded-2xl border border-emerald-200 bg-emerald-50 p-5">
          <div className="text-sm font-medium uppercase tracking-wide text-emerald-700">Estimated result</div>
          <div className="mt-2 text-3xl font-bold text-slate-900">Net irrigation: 3.0 mm/day</div>
          <p className="mt-2 text-sm text-slate-600">Simplified daily screening estimate only. It does not model soil-water storage, runoff, or drainage.</p>
        </div>
      </div>
    </div>
  )
}

function ScenarioSimulatorPage() {
  return (
    <div className="mx-auto max-w-4xl px-6 py-12">
      <h2 className="text-3xl font-bold text-slate-900">Scenario simulator</h2>
      <div className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="grid gap-4 md:grid-cols-2">
          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
            Temperature modifier (°C)
            <input type="number" step="0.1" defaultValue={1.5} className="rounded-lg border border-slate-300 px-3 py-2" />
          </label>
          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
            Rainfall modifier (%)
            <input type="number" step="1" defaultValue={-10} className="rounded-lg border border-slate-300 px-3 py-2" />
          </label>
        </div>
        <button className="mt-5 rounded-lg bg-emerald-600 px-5 py-3 font-semibold text-white">Simulate impact</button>
        <div className="mt-6 rounded-2xl border border-sky-200 bg-sky-50 p-5">
          <div className="text-sm font-medium uppercase tracking-wide text-sky-700">Simulation result</div>
          <div className="mt-2 text-3xl font-bold text-slate-900">Yield impact: -15%</div>
          <p className="mt-2 text-sm text-slate-600">Based on historical data and projected climate variations.</p>
        </div>
      </div>
    </div>
  )
}

function LoginPage() {
  return (
    <div className="mx-auto max-w-md px-6 py-20">
      <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-lg">
        <h2 className="text-3xl font-bold text-slate-900">Access AgriWater AI</h2>
        <form className="mt-6 space-y-4">
          <input type="email" placeholder="Email" className="w-full rounded-lg border border-slate-300 px-3 py-2" defaultValue="admin@example.com" />
          <input type="password" placeholder="Password" className="w-full rounded-lg border border-slate-300 px-3 py-2" defaultValue="StrongPass!123" />
          <button className="w-full rounded-lg bg-emerald-600 px-5 py-3 font-semibold text-white">Login</button>
        </form>
      </div>
    </div>
  )
}

function SpecialistPage() {
  return (
    <div>
      <h2 className="text-3xl font-bold text-slate-900">Specialist dashboard</h2>
      <p className="mt-2 text-slate-600">Protected specialist workspace</p>
    </div>
  )
}

function AdminPage() {
  return (
    <div>
      <h2 className="text-3xl font-bold text-slate-900">Administrator dashboard</h2>
      <p className="mt-2 text-slate-600">Protected admin workspace</p>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<PublicLayout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/predict" element={<PredictPage />} />
          <Route path="/crops" element={<CropPlanningPage />} />
          <Route path="/water" element={<WaterPage />} />
          <Route path="/scenario" element={<ScenarioSimulatorPage />} />
          <Route path="/login" element={<LoginPage />} />
        </Route>
        
        <Route path="/specialist" element={<SpecialistLayout />}>
          <Route index element={<SpecialistPage />} />
          <Route path="crops" element={<div>Crops List Placeholder</div>} />
          <Route path="reports" element={<div>Reports Placeholder</div>} />
        </Route>

        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<AdminPage />} />
          <Route path="users" element={<div>Users List Placeholder</div>} />
          <Route path="system" element={<div>System Logs Placeholder</div>} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
