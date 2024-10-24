import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Typography, Container } from '@mui/material';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const data = {
  labels: ['Product 1', 'Product 2', 'Product 3'],
  datasets: [
    {
      label: 'Revenue',
      data: [12000, 735.7376834293268, 1000],
      backgroundColor: ['#0033a0', '#0072ce', '#00a3e0']
    },
  ],
};

const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Product Revenues',
    },
  },
};

const BarChartPage = () => {
  return (
    <Container className="container">
         <Typography variant="h4" component="h1" gutterBottom className="header">
        Bar Chart Example Page
      </Typography>
      <Typography variant="body1" className="description">
        This page provides an example of results displayed in a bar chart format.
      </Typography>
          
          <section>
              <figure>
                  <Bar data={data} options={options} />
              </figure >
          </section>
              
    </Container>
  );
};

export default BarChartPage;