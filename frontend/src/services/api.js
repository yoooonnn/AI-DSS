const API_BASE_URL = 'http://127.0.0.1:5000';

export const getLogs = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/get_logs`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
      // mode: 'no-cors' // 이 설정은 삭제하세요
    });

    if (!response.ok) {
      console.error('Response status:', response.status);
      console.error('Response statusText:', response.statusText);
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log('API Response:', result); // 디버깅용
    return result.data;
  } catch (error) {
    console.error('Error fetching logs:', error);
    throw error;
  }
};

