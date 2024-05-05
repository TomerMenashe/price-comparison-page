'use client'
// Importing necessary libraries and styles
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Select from 'react-select';
import './App.css';

// Define the ProductSearch component
const ProductSearch = () => {
  // State hooks for managing component state
  const [productName, setProductName] = useState(''); // Stores the current product name input
  const [loading, setLoading] = useState(false); // Manages the loading state for API requests
  const [error, setError] = useState(''); // Captures and displays errors
  const [results, setResults] = useState(null); // Stores the search results
  const [productFact, setProductFact] = useState(''); // Stores a fun fact about the product
  const [page, setPage] = useState('landing'); // Controls which page/view to show

  // API keys and endpoint configurations
  const OPENAI_API_KEY = 'sk-proj-iWgMsC1oo6HlffQ39uAPT3BlbkFJ6eVOZidz9D0aiJ8m92Rc'; // API key for OpenAI (should be moved to environment variables)
  const OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'; // OpenAI API endpoint

  // Function to fetch a fun fact about the product using the OpenAI API
  const fetchProductFact = async (product) => {
    const headers = {
      'Authorization': `Bearer ${OPENAI_API_KEY}`,
      'Content-Type': 'application/json'
    };

    const data = {
      model: 'gpt-4',
      messages: [
        {role: "system", content: "Generate a very fun fact about the product:"},
        {role: "user", content: product}
      ],
      temperature: 0.7,
      max_tokens: 512
    };

    try {
      const response = await axios.post(OPENAI_API_URL, data, { headers });
      if (response.data && response.data.choices && response.data.choices.length > 0) {
        const productFact = response.data.choices[0].message.content.trim();
        console.log('Product Fact:', productFact);
        setProductFact(productFact);
      } else {
        throw new Error('No valid response from OpenAI');
      }
    } catch (error) {
      console.error("API Error:", error.response ? JSON.stringify(error.response.data) : error.message);
      throw new Error('Failed to fetch data from the OpenAI API.');
    }
  };

  // Handler for input changes, updating the product name in state
  const handleInput = (e) => {
    setProductName(e.target.value);
  };

  // Handler for initiating a search when the search button is clicked
  const handleSearch = async () => {
    if (!productName.trim()) {
      setError("Please enter a product name.");
      return;
    }
    setLoading(true);
    setError('');
    setResults(null);
    setProductFact('');

    // Fetch a product fact while other data is loading
    await fetchProductFact(productName);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await axios.get(`${apiUrl}/api/compare-prices?product_name=${encodeURIComponent(productName)}`);
      setResults(response.data);
      setPage('results');
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Failed to fetch data. Please try again.');
    }

    setLoading(false);
  };

  // Component rendering based on current page state
  return (
    <div className="app-container">
      {page === 'landing' && (
        <>
          <h1 className="welcome-title">Welcome to Price Comparison Page</h1>
          <h2 className="subtitle">by Tomer Menashe & Guy Abarbanel</h2>
          <div className="card">
            <button className="button" onClick={() => setPage('search')}>Start Searching</button>
          </div>
        </>
      )}
      {page === 'search' && (
        <div className="search-container">
          <h1 className="search-title">It's time to search for a product!</h1>
          <div className="search-card">
            <h2>Search for Products</h2>
            <input 
              className="input"
              type="text"
              value={productName}
              onChange={handleInput}
              placeholder="Enter a product name..."
            />
            <button className="button" onClick={handleSearch} disabled={loading}>
              {loading ? 'Loading...' : 'Search'}
            </button>
            {error && <p className="error">{error}</p>}
          </div>
        </div>
      )}
      {page === 'results' && results && (
        <div className="results-container">
          <h2 className="results-title">Here are the Results</h2>
          {/* Display the results table */}
          <table className="results-table">
            <thead>
              <tr>
                <th>Store</th>
                <th>Product Name</th>
                <th>Price</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(results).map(([store, { price, product_url }], index) => (
                <tr key={store}>
                  <td>{store}</td>
                  <td><a href={product_url} target="_blank" rel="noopener noreferrer" className="link">{productName}</a></td>
                  <td>{price}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <button className="button" onClick={() => setPage('search')}>Search Again</button>
        </div>
      )}
      {/* Display the product fact container */}
      {loading && productFact && (
        <div className="fact-container">
          <div className="cloud">
            <h3 className="fact-title">Fun Fact:</h3>
            <p>{productFact}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductSearch;
