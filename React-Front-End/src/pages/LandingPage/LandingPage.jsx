import React, { useState } from 'react';
import { 
  Container,
  Grid,
  Paper,
  Typography,
  ToggleButton,
  ToggleButtonGroup,
  Button,
  Box,
  Card,
  CardContent,
  CardHeader,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import BarChartIcon from '@mui/icons-material/BarChart';
import PieChartIcon from '@mui/icons-material/PieChart';
import TableChartIcon from '@mui/icons-material/TableChart';
import BarChartPage from '../../pages/BarChartPage/BarChartPage';
import PieChartPage from '../../pages/PieChartPage/PieChartPage';
import TabularPage from '../../pages/TabularPage/TabularPage';

// Styled components
const StyledCard = styled(Card)(({ theme }) => ({
  height: '100%',
  boxShadow: theme.shadows[2],
}));

const StyledButton = styled(Button)(({ theme }) => ({
  marginBottom: theme.spacing(1),
  width: '100%',
}));

const Dashboard = () => {
  const [chartType, setChartType] = useState('bar');
  const [selectedModel, setSelectedModel] = useState(null);

  const handleChartTypeChange = (event, newValue) => {
    if (newValue !== null) {
      setChartType(newValue);
    }
  };

  const renderChartComponent = () => {
    switch (chartType) {
      case 'bar':
        return <BarChartPage />;
      case 'pie':
        return <PieChartPage />;
      case 'table':
        return <TabularPage />;
      default:
        return <BarChartPage />;
    }
  };

  const getRecommendation = () => {
    switch (chartType) {
      case 'bar':
        return "Based on the bar chart analysis, Drug C shows the highest performance metrics.";
      case 'pie':
        return "The pie chart distribution indicates Drug C dominates the efficacy ratings.";
      case 'table':
        return "Tabular data analysis suggests focusing on Drug C for optimal results.";
      default:
        return "";
    }
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Pharmaceutical Analysis
      </Typography>
      
      <Grid container spacing={3}>
        {/* Main Content */}
        <Grid item xs={12} md={9}>
          <StyledCard>
            <CardHeader title="Data Visualization" />
            <CardContent>
              {/* Chart Component */}
              <Box sx={{ minHeight: 400 }}>
                {renderChartComponent()}
              </Box>
              
              {/* Recommendation Section */}
              <Paper 
                elevation={0} 
                sx={{ 
                  mt: 3, 
                  p: 2, 
                  bgcolor: 'grey.50'
                }}
              >
                <Typography variant="h6" gutterBottom>
                  Recommendation
                </Typography>
                <Typography variant="body1">
                  {getRecommendation()}
                </Typography>
              </Paper>
            </CardContent>
          </StyledCard>
        </Grid>
        {/* right Sidebar */}
        <Grid item xs={12} md={3}>
          {/* Chart Type Selection */}
          <StyledCard sx={{ mb: 3 }}>
            <CardHeader title="Chart Type" />
            <CardContent>
              <ToggleButtonGroup
                value={chartType}
                exclusive
                onChange={handleChartTypeChange}
                orientation="horizontal"
                fullWidth
              >
                <ToggleButton value="bar" aria-label="bar chart">
                  <BarChartIcon />
                </ToggleButton>
                <ToggleButton value="pie" aria-label="pie chart">
                  <PieChartIcon />
                </ToggleButton>
                <ToggleButton value="table" aria-label="table">
                  <TableChartIcon />
                </ToggleButton>
              </ToggleButtonGroup>
            </CardContent>

             {/* Model Selection */}
    
            <CardHeader title="Models" />
            <CardContent>
              <StyledButton
                variant={selectedModel === 'regression' ? 'contained' : 'outlined'}
                onClick={() => setSelectedModel('regression')}
                color="primary"
              >
                Model 1
              </StyledButton>
              <StyledButton
                variant={selectedModel === 'classification' ? 'contained' : 'outlined'}
                onClick={() => setSelectedModel('classification')}
                color="primary"
              >
                Model 2
              </StyledButton>
              <StyledButton
                variant={selectedModel === 'clustering' ? 'contained' : 'outlined'}
                onClick={() => setSelectedModel('clustering')}
                color="primary"
              >
                Model 3
              </StyledButton>
              <StyledButton
                variant="contained"
                disabled={!selectedModel}
                color="secondary"
              >
                Generate Analysis
              </StyledButton>
            </CardContent>
          </StyledCard>

        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;