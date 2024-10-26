import React, { useEffect, useState } from 'react';
import axios from 'axios';

function DataDisplay() {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Fetch data from the FastAPI endpoint
    axios.get('http://127.0.0.1:8000/api/data')
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);

  return (
    <div>
      <h1>Data from FastAPI</h1>
      <ul>
        {data.map((item, index) => (
          <li key={index}>
            {JSON.stringify(item)}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default DataDisplay;
