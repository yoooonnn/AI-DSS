import React, { useMemo } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, LineChart, Line, ResponsiveContainer } from 'recharts';
import { Power, Clock, Settings, Zap } from 'lucide-react';

const DevicesAnalytics = ({ logs }) => {
  // 기존 useMemo 로직들은 유지
  const devices = useMemo(() => {
    const deviceMap = logs.reduce((acc, log) => {
      const deviceKey = `${log.device_type}#${log.device_id}`;
      if (!acc[deviceKey] || new Date(log.timestamp) > new Date(acc[deviceKey].timestamp)) {
        acc[deviceKey] = {
          type: log.device_type,
          id: log.device_id,
          state: log.state,
          timestamp: log.timestamp
        };
      }
      return acc;
    }, {});
    return Object.values(deviceMap);
  }, [logs]);

  const usageData = useMemo(() => {
    const hourlyData = Array(24).fill().map((_, i) => ({
      time: `${i}:00`,
      lights: 0,
      speakers: 0
    }));

    logs.forEach(log => {
      const hour = new Date(log.timestamp).getHours();
      if (log.device_type === 'Light' && log.state.power === 'on') {
        hourlyData[hour].lights++;
      } else if (log.device_type === 'Speaker' && log.state.power === 'on') {
        hourlyData[hour].speakers++;
      }
    });

    return hourlyData;
  }, [logs]);

  // 디바이스 타입별 기능 사용량 분리
  const deviceFunctionUsage = useMemo(() => {
    const usage = {
      light: {},
      speaker: {}
    };

    logs.forEach(log => {
      if (!log.func) return;

      if (log.device_type === 'Light') {
        usage.light[log.func] = (usage.light[log.func] || 0) + 1;
      } else if (log.device_type === 'Speaker') {
        usage.speaker[log.func] = (usage.speaker[log.func] || 0) + 1;
      }
    });

    return {
      lightFunctions: Object.entries(usage.light)
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count),
      speakerFunctions: Object.entries(usage.speaker)
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count)
    };
  }, [logs]);

  const deviceStats = useMemo(() => ({
    lights: {
      total: devices.filter(d => d.type === 'Light').length,
      on: devices.filter(d => d.type === 'Light' && d.state?.power === 'on').length,
      avgBrightness: devices
        .filter(d => d.type === 'Light' && d.state?.brightness)
        .reduce((acc, curr) => acc + curr.state.brightness, 0) / 
        devices.filter(d => d.type === 'Light' && d.state?.brightness).length || 0
    },
    speakers: {
      total: devices.filter(d => d.type === 'Speaker').length,
      on: devices.filter(d => d.type === 'Speaker' && d.state?.power === 'on').length,
      avgVolume: devices
        .filter(d => d.type === 'Speaker' && d.state?.volume)
        .reduce((acc, curr) => acc + curr.state.volume, 0) /
        devices.filter(d => d.type === 'Speaker' && d.state?.volume).length || 0
    }
  }), [devices]);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold flex items-center gap-2">
        <Settings className="w-6 h-6" />
        디바이스 현황
      </h2>

      {/* 디바이스 상태 카드 */}
      <div className="grid md:grid-cols-2 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-2">
              <h3 className="text-lg font-medium flex items-center gap-2">
                <Power className="w-4 h-4" />
                조명 상태
              </h3>
              <div className="text-3xl font-bold">
                {deviceStats.lights.on}/{deviceStats.lights.total}
              </div>
              <div className="text-sm text-muted-foreground">
                평균 밝기: {deviceStats.lights.avgBrightness.toFixed(1)}%
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="space-y-2">
              <h3 className="text-lg font-medium flex items-center gap-2">
                <Power className="w-4 h-4" />
                스피커 상태
              </h3>
              <div className="text-3xl font-bold">
                {deviceStats.speakers.on}/{deviceStats.speakers.total}
              </div>
              <div className="text-sm text-muted-foreground">
                평균 볼륨: {deviceStats.speakers.avgVolume.toFixed(1)}%
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 시간대별 사용량 */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="w-4 h-4" />
            시간대별 사용량
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={usageData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="lights" name="조명" stroke="#8884d8" />
                <Line type="monotone" dataKey="speakers" name="스피커" stroke="#82ca9d" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* 조명 기능별 사용량 */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="w-4 h-4" />
            조명 기능별 사용량
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={deviceFunctionUsage.lightFunctions}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#8884d8" name="사용 횟수" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* 스피커 기능별 사용량 */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="w-4 h-4" />
            스피커 기능별 사용량
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={deviceFunctionUsage.speakerFunctions}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#82ca9d" name="사용 횟수" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default DevicesAnalytics;