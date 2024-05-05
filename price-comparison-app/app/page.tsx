'use client';

import React, { useState } from 'react';
import axios from 'axios';

const ProductSearch = () => {
  const [productName, setProductName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState(null);

  const handleSearch = async () => {
    if (!productName.trim()) {
      setError("Please enter a product name.");
      return;
    }

    setLoading(true);
    setError('');
    setResults(null);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await axios.get(`${apiUrl}/api/compare-prices?product_name=${encodeURIComponent(productName)}`);
      setResults(response.data);
      setError('');
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Failed to fetch data. Please try again.');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-200 to-blue-300 flex items-center justify-center">
      <div className="w-full max-w-lg bg-white rounded-lg shadow-xl p-8">
        <h2 className="text-xl font-semibold text-gray-800 mb-6 text-center">Product Price Search</h2>
        <input 
          className="w-full p-4 mb-4 text-gray-700 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          type="text"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
          placeholder="Type a product name..."
        />
        <button 
          className={`w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition-colors duration-200 ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
          onClick={handleSearch} 
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Search'}
        </button>
        {error && <p className="text-red-600 text-center mt-2">{error}</p>}
        {results && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold text-gray-800">Results:</h3>
            <table className="w-full mt-4 bg-white border-b border-gray-200 shadow-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="text-left p-3 font-semibold text-gray-600">Store</th>
                  <th className="text-left p-3 font-semibold text-gray-600">Product Name</th>
                  <th className="text-left p-3 font-semibold text-gray-600">Price</th>
                </tr>
              </thead>
              <tbody className="text-gray-800">
                {Object.entries(results).map(([store, { price, product_url }], index) => (
                  <tr key={store} className={`${index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}`}>
                    <td className="p-3">{store}</td>
                    <td className="p-3">
                      <a href={product_url} className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
                        {productName}
                      </a>
                    </td>
                    <td className="p-3">{price}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductSearch;