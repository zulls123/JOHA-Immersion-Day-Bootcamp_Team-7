import React from 'react';
import {  Routes, Route } from 'react-router-dom';
import LandingPage from '../../pages/LandingPage/LandingPage';
import TabularPage from '../../pages/TabularPage/TabularPage';
import AppRoutes from '../../constants/AppRoutes';
import PieChartPage from '../../pages/PieChartPage/PieChartPage';
import BarChartPage from '../../pages/BarChartPage/BarChartPage';

const CustomRouter = () => {
 return (
    <Routes>
      <Route path={AppRoutes.Home} element={<LandingPage />} />
      <Route path={AppRoutes.PieChartExample} element={<PieChartPage />} />
      <Route path={AppRoutes.TableExample} element={<TabularPage />} />
      <Route path={AppRoutes.BarChartExample} element={<BarChartPage />} />
    </Routes>
  );
    
};

export default CustomRouter;