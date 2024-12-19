// OverviewTab.jsx
import React from 'react';
import DevicesList from './DevicesList';

const OverviewTab = ({ logs }) => {
  return (
    <DevicesList 
      logs={logs} 
      gridCols="grid-cols-1 md:grid-cols-2 lg:grid-cols-4" 
    />
  );
};

export default OverviewTab;