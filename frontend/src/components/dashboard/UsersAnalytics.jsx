import React, { useMemo } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Users, Activity, Smartphone, Clock } from 'lucide-react';

const StatCard = ({ title, value, icon: Icon, description }) => (
  <Card>
    <CardHeader>
      <CardTitle className="text-sm flex items-center gap-2">
        {Icon && <Icon className="w-4 h-4" />}
        {title}
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div className="text-2xl font-bold">{value}</div>
      {description && (
        <div className="text-sm text-muted-foreground mt-1">{description}</div>
      )}
    </CardContent>
  </Card>
);

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

const UsersAnalytics = ({ logs = [] }) => {
  // 사용자 활동 데이터 계산
  const userAnalytics = useMemo(() => {
    const userActivities = {};
    const userDevices = {};

    logs.forEach(log => {
      if (!log.user_id) return;

      // 활동 수 집계
      userActivities[log.user_id] = (userActivities[log.user_id] || 0) + 1;

      // 사용한 디바이스 집계
      if (!userDevices[log.user_id]) {
        userDevices[log.user_id] = new Set();
      }
      userDevices[log.user_id].add(log.device_id);
    });

    // 가장 활동적인 사용자 정렬
    const mostActiveUsers = Object.entries(userActivities)
      .map(([user_id, activity]) => ({ user_id, activity }))
      .sort((a, b) => b.activity - a.activity);

    // 가장 많은 디바이스를 사용한 사용자 정렬
    const mostActiveUsersByUsage = Object.entries(userDevices)
      .map(([user_id, devices]) => ({
        user_id,
        totalDevicesUsed: devices.size
      }))
      .sort((a, b) => b.totalDevicesUsed - a.totalDevicesUsed);

    return {
      mostActiveUsers,
      mostActiveUsersByUsage,
      userActivities
    };
  }, [logs]);

  // 시간별/디바이스별 인사이트 계산
  const insights = useMemo(() => {
    if (!logs.length) {
      return {
        devicePreferenceData: [],
        hourlyActivityData: Array(24).fill(0).map((_, hour) => ({
          hour: `${hour}:00`,
          count: 0
        }))
      };
    }

    // 시간대별 활동
    const hourlyActivity = Array(24).fill(0);
    // 디바이스 선호도
    const devicePreferences = {};
    
    logs.forEach(log => {
      if (!log || !log.timestamp || !log.device_type) return;

      const hour = new Date(log.timestamp).getHours();
      hourlyActivity[hour]++;
      devicePreferences[log.device_type] = (devicePreferences[log.device_type] || 0) + 1;
    });

    return {
      devicePreferenceData: Object.entries(devicePreferences).map(([name, value]) => ({
        name,
        value
      })),
      hourlyActivityData: hourlyActivity.map((count, hour) => ({
        hour: `${hour}:00`,
        count
      }))
    };
  }, [logs]);

  // 사용자 활동 차트 데이터
  const activityData = useMemo(() => {
    return userAnalytics.mostActiveUsers.slice(0, 10).map(user => ({
      user_id: user.user_id.slice(0, 5),
      actions: user.activity,
      fullId: user.user_id
    }));
  }, [userAnalytics.mostActiveUsers]);

  // 커스텀 툴팁 컴포넌트
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const fullUserId = payload[0].payload.fullId;
      const userLogs = logs.filter(log => log.user_id === fullUserId);
      
      const deviceStats = userLogs.reduce((acc, log) => {
        if (log.device_type) {
          acc[log.device_type] = (acc[log.device_type] || 0) + 1;
        }
        return acc;
      }, {});

      return (
        <div className="bg-white p-4 border rounded shadow">
          <p className="font-bold">{`사용자 ID: ${fullUserId}`}</p>
          <p>{`총 활동 수: ${payload[0].value}회`}</p>
          <div className="mt-2">
            <p className="font-bold">디바이스 사용 통계:</p>
            {Object.entries(deviceStats).map(([device, count]) => (
              <p key={device}>{`${device}: ${count}회`}</p>
            ))}
          </div>
        </div>
      );
    }
    return null;
  };

  // 통계 계산 함수들
  const getAverageActivityPerUser = () => {
    if (!logs.length || !Object.keys(userAnalytics.userActivities).length) return 0;
    return (logs.length / Object.keys(userAnalytics.userActivities).length).toFixed(1);
  };

  const getPeakHour = () => {
    if (!insights.hourlyActivityData.length) return '00:00';
    const peakHourIndex = insights.hourlyActivityData.reduce((maxIdx, curr, idx) => 
      curr.count > insights.hourlyActivityData[maxIdx].count ? idx : maxIdx, 0);
    return insights.hourlyActivityData[peakHourIndex].hour;
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold flex items-center gap-2">
        <Users className="w-6 h-6" />
        사용자 분석
      </h2>

      {/* 주요 통계 카드 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard 
          title="가장 활동적인 사용자" 
          value={`${userAnalytics.mostActiveUsers[0]?.activity || 0}회`}
          icon={Activity}
          description={userAnalytics.mostActiveUsers[0]?.user_id ? 
            `ID: ${userAnalytics.mostActiveUsers[0].user_id.slice(0, 8)}...` : 
            '데이터 없음'
          }
        />
        <StatCard 
          title="최다 디바이스 사용자" 
          value={`${userAnalytics.mostActiveUsersByUsage[0]?.totalDevicesUsed || 0}개`}
          icon={Smartphone}
          description={userAnalytics.mostActiveUsersByUsage[0]?.user_id ? 
            `ID: ${userAnalytics.mostActiveUsersByUsage[0].user_id.slice(0, 8)}...` : 
            '데이터 없음'
          }
        />
        <StatCard 
          title="평균 일일 활동" 
          value={`${getAverageActivityPerUser()}회`}
          icon={Activity}
          description="사용자당 평균"
        />
        <StatCard 
          title="피크 시간대" 
          value={getPeakHour()}
          icon={Clock}
          description="가장 활동적인 시간"
        />
      </div>

      {/* 사용자 활동 그래프 */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="w-4 h-4" />
            상위 10명 사용자 활동량
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={activityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="user_id" />
                <YAxis />
                <Tooltip content={<CustomTooltip />} />
                <Bar 
                  dataKey="actions" 
                  fill="#8884d8"
                  name="활동 수"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* 시간대별 활동 분포 */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="w-4 h-4" />
            시간대별 활동 분포
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={insights.hourlyActivityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="hour" />
                <YAxis />
                <Tooltip />
                <Bar 
                  dataKey="count" 
                  fill="#82ca9d"
                  name="활동 수"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* 디바이스 선호도 */}
      {insights.devicePreferenceData.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Smartphone className="w-4 h-4" />
              디바이스 선호도
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={insights.devicePreferenceData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label={({name, percent}) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {insights.devicePreferenceData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
          </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default UsersAnalytics;