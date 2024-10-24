import React from 'react';
import { Typography, Container } from '@mui/material';


const LandingPage = () => {
  return (
      <Container className="container">
        <Typography variant="h4" component="h1" gutterBottom className="header">
          Landing page
        </Typography>
        <Typography variant="body1" className="description">
          This is the main page of the application
        </Typography>    

      </Container>
  );
};

export default LandingPage;