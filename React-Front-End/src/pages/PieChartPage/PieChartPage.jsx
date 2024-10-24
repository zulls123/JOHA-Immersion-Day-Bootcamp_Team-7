import React, { useEffect, useState } from 'react';
import { Typography, Container } from '@mui/material';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import PredictiveModelAPI from '../../api/PredictiveModelApi';
import './PieChartPage.css';

ChartJS.register(ArcElement, Tooltip, Legend);

const PieChartPage = () => {
  const [data, setData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      const result = await PredictiveModelAPI.getResults();
      const { product1Revenue, product2Revenue, product3Revenue } = result[0];
      setData({
        labels: ['Product 1 Revenue', 'Product 2 Revenue', 'Product 3 Revenue'],
        datasets: [
          {
            data: [product1Revenue, product2Revenue, product3Revenue],
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
            hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
          },
        ],
      });
    };
    fetchData();
  }, []);

  return (
    <Container className="container">
      <Typography variant="h4" component="h1" gutterBottom className="header">
        Pie Chart Example Page
      </Typography>
      <Typography variant="body1" className="description">
        This page provides an example of results displayed in a pie chart format.
      </Typography>
      {data.labels && <Pie data={data} />}
    </Container>
  );
};

export default PieChartPage;