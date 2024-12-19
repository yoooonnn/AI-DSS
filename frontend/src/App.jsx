import React, { useState, useEffect } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Loader2 } from "lucide-react";
import QueryInput from './components/dashboard/QueryInput';
import OverviewTab from './components/dashboard/OverviewTab';
import { getLogs } from './services/api';
import DevicesAnalytics from './components/dashboard/DevicesAnalytics';
import UsersAnalytics from './components/dashboard/UsersAnalytics';
import { useAIQuery } from './components/dashboard/useAIQuery';

const App = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [logs, setLogs] = useState([]); // raw 로그 데이터
  const [isLoading, setIsLoading] = useState(false);
  const [fetchError, setFetchError] = useState(null);

  // AI 쿼리 관련 상태와 함수
  const { loading: queryLoading, error: queryError, results: queryResults, sql, executeQuery } = useAIQuery();
  
  // 초기 데이터 로드
  const fetchData = async () => {
    try {
      setIsLoading(true);
      const logsData = await getLogs();
      setLogs(logsData);
      setFetchError(null);
    } catch (err) {
      setFetchError('데이터를 불러오는 중 오류가 발생했습니다.');
      console.error('Error fetching data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // 쿼리 결과가 있으면 그것을 사용, 아니면 전체 로그 사용
  // queryResults가 null일 수 있으므로 옵셔널 체이닝 또는 조건부 처리 필요
  const displayLogs = queryResults?.data?.length > 0 ? queryResults.data : logs;

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-4 space-y-4">
      <h1 className="text-3xl font-bold text-center mb-8">Decision Support System</h1>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <div className="space-y-4">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="devices">Devices</TabsTrigger>
            <TabsTrigger value="users">Users</TabsTrigger>
            <TabsTrigger value="query">Query</TabsTrigger>
          </TabsList>
        </div>

        {fetchError && (
          <div className="bg-red-50 text-red-500 p-4 rounded-md">
            {fetchError}
          </div>
        )}

        <TabsContent value="overview">
          <OverviewTab logs={displayLogs} />
        </TabsContent>

        <TabsContent value="devices">
          <DevicesAnalytics logs={displayLogs} />
        </TabsContent>

        <TabsContent value="users">
          <UsersAnalytics logs={displayLogs} />
        </TabsContent>

        <TabsContent value="query">
          <div className="space-y-4">
            <div className="text-gray-700">
              <h2 className="text-xl font-medium mb-4">AI 검색</h2>
              <p className="mb-2">
                자연어로 검색어를 입력하세요 (예: "켜져있는 모든 기기 보기").
              </p>
            </div>

            <QueryInput 
              onSearch={executeQuery}
              loading={queryLoading}
            />

            {queryError && (
              <div className="bg-red-50 text-red-500 p-4 rounded-md">
                {queryError}
              </div>
            )}
{/* 
            {sql && (
              <div className="bg-gray-50 p-4 rounded-md">
                <h3 className="font-medium mb-2">생성된 SQL:</h3>
                <pre className="text-sm bg-white p-3 rounded border">
                  {sql}
                </pre>
              </div>
            )} */}

            {queryResults && (
              <div className="bg-white p-4 rounded-md border">
                <h3 className="font-medium mb-2">검색 결과:</h3>
                {queryResults.total_rows > 0 ? (
                  <>
                    <div className="text-sm text-gray-500 mb-4">
                      총 {queryResults.total_rows}개의 결과가 있습니다.
                    </div>
                    <div className="overflow-x-auto">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            {queryResults.columns?.map((column) => (
                              <th
                                key={column}
                                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                              >
                                {column}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {queryResults.data?.slice(0, 10).map((row, i) => (
                            <tr key={i} className="hover:bg-gray-50">
                              {queryResults.columns?.map((column) => {
                                let value = row[column];
                                // device_id와 user_id가 긴 문자열인 경우 앞 10자리만 표시하고 ... 추가
                                if (column === 'device_id' || column === 'user_id') {
                                  if (typeof value === 'string' && value.length > 10) {
                                    value = value.substring(0, 10) + '...';
                                  }
                                }
                                return (
                                  <td
                                    key={column}
                                    className="px-6 py-4 text-sm text-gray-900"
                                  >
                                    {typeof value === 'object'
                                      ? JSON.stringify(value, null, 2)
                                      : String(value)}
                                  </td>
                                );
                              })}
                              </tr>
                          ))}
                        </tbody>
                      </table>
                      {queryResults.total_rows > 10 && (
                        <div className="text-sm text-gray-500 mt-2 p-2">
                          처음 10개의 결과만 표시됩니다.
                        </div>
                      )}
                    </div>
                  </>
                ) : (
                  <div className="text-sm text-gray-500">
                    검색 결과가 없습니다.
                  </div>
                )}
              </div>
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default App;