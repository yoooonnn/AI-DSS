import { useState } from 'react';

export const useAIQuery = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [queryResponse, setQueryResponse] = useState(null);
  const [sql, setSql] = useState('');

  const executeQuery = async (query) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          execute: true
        })
      });

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      setQueryResponse(data);
      setSql(data.sql || '');
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Query failed');
      setQueryResponse(null);
      setSql('');
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    results: queryResponse?.results || null,  // null이 아닌 빈 배열로 초기화
    sql,
    executeQuery
  };
};