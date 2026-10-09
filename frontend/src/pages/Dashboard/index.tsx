import React from 'react';

const Dashboard = () => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Specialist Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded shadow border border-gray-200">
          <h2 className="text-lg font-semibold mb-2">Crop Catalogue</h2>
          <p className="text-gray-600">View and manage crop data.</p>
        </div>
        <div className="bg-white p-4 rounded shadow border border-gray-200">
          <h2 className="text-lg font-semibold mb-2">Water Calculator</h2>
          <p className="text-gray-600">Calculate water requirements.</p>
        </div>
        <div className="bg-white p-4 rounded shadow border border-gray-200">
          <h2 className="text-lg font-semibold mb-2">Scenario Simulator</h2>
          <p className="text-gray-600">Simulate different climate scenarios.</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
