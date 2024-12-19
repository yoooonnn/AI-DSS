// DevicesList.jsx
import React, { useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Lightbulb, Volume2, Power, Hash, User } from 'lucide-react';

// Device card component
const DeviceCard = ({ device }) => {
  const truncateId = (id) => {
    return id ? `${id.slice(0, 8)}...` : 'Unknown';
  };

  const getStateColor = (type, power) => {
    if (power !== 'on') return 'text-gray-400';
    return type === 'Light' ? 'text-yellow-400' : 'text-blue-400';
  };

  const getIcon = (type, power) => {
    const iconClass = getStateColor(type, power);
    return type === 'Light' ? (
      <Lightbulb className={`w-6 h-6 ${iconClass}`} />
    ) : (
      <Volume2 className={`w-6 h-6 ${iconClass}`} />
    );
  };

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <CardTitle className="text-base font-semibold">
              {device.type}
            </CardTitle>
            <div className="flex items-center text-xs text-muted-foreground gap-1">
              <Hash className="w-3 h-3" />
              {truncateId(device.device_id || device.id)}
            </div>
            <div className="flex items-center text-xs text-muted-foreground gap-1">
              <User className="w-3 h-3" />
              {truncateId(device.user_id)}
            </div>
          </div>
          {getIcon(device.type, device.state?.power)}
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-3">
          <div className="flex items-center gap-2 text-sm">
            <Power className="w-4 h-4" />
            <span className={`font-medium ${device.state?.power === 'on' ? 'text-green-500' : 'text-gray-500'}`}>
              {device.state?.power === 'on' ? 'ON' : 'OFF'}
            </span>
          </div>

          {device.type === 'Light' && (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Brightness</span>
                <span className="font-medium">{device.state?.brightness || 0}%</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Color</span>
                <span className="font-medium">{device.state?.color || 'Default'}</span>
              </div>
            </div>
          )}

          {device.type === 'Speaker' && (
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Volume</span>
              <span className="font-medium">{device.state?.volume || 0}%</span>
            </div>
          )}

          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Mode</span>
            <span className="font-medium capitalize">{device.state?.mode || 'Normal'}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

// Devices list component with configurable grid columns
const DevicesList = ({ logs, gridCols = "grid-cols-1 md:grid-cols-2 lg:grid-cols-3" }) => {
  const devices = useMemo(() => {
    const deviceMap = logs.reduce((acc, log) => {
      const deviceKey = `${log.device_type}#${log.device_id}`;
      if (!acc[deviceKey] || new Date(log.timestamp) > new Date(acc[deviceKey].timestamp)) {
        acc[deviceKey] = {
          type: log.device_type,
          device_id: log.device_id,
          user_id: log.user_id,
          state: log.state,
          timestamp: log.timestamp
        };
      }
      return acc;
    }, {});

    return Object.values(deviceMap);
  }, [logs]);

  return (
    <div className={`grid ${gridCols} gap-4`}>
      {devices.map((device) => (
        <DeviceCard 
          key={`${device.type}-${device.device_id}`} 
          device={device}
        />
      ))}
    </div>
  );
};

export default DevicesList;