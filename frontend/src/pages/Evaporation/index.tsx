import React, { useState } from 'react';

const EvaporationPrediction = () => {
  const [formData, setFormData] = useState({
    temperature_c: '',
    humidity_pct: '',
    wind_speed_kmh: '',
    sunshine_hours: ''
  });
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Use the backend mock API
    setPrediction({ value: 4.5, unit: 'mm/day' });
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Evaporation Prediction</h1>
      <form onSubmit={handleSubmit} className="space-y-4 max-w-md">
        <div>
          <label className="block text-sm font-medium">Temperature (°C)</label>
          <input
            type="number"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            value={formData.temperature_c}
            onChange={(e) => setFormData({ ...formData, temperature_c: e.target.value })}
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Humidity (%)</label>
          <input
            type="number"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            value={formData.humidity_pct}
            onChange={(e) => setFormData({ ...formData, humidity_pct: e.target.value })}
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Wind Speed (km/h)</label>
          <input
            type="number"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            value={formData.wind_speed_kmh}
            onChange={(e) => setFormData({ ...formData, wind_speed_kmh: e.target.value })}
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Sunshine Hours</label>
          <input
            type="number"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            value={formData.sunshine_hours}
            onChange={(e) => setFormData({ ...formData, sunshine_hours: e.target.value })}
          />
        </div>
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700"
        >
          Predict
        </button>
      </form>
      {prediction && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded text-green-800">
          <p className="font-bold">Predicted Evaporation: {prediction.value} {prediction.unit}</p>
        </div>
      )}
    </div>
  );
};

export default EvaporationPrediction;
