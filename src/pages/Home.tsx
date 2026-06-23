import React, { useState, useEffect } from 'react';
import DashboardCard from '../components/DashboardCard';
import TrendChart from '../components/TrendChart';
import DepartmentChart from '../components/DepartmentChart';
import AIChat from '../components/AIChat';
import { api, DashboardParams, DashboardResponse } from '../lib/api';

const Home: React.FC = () => {
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [showAIChat, setShowAIChat] = useState(false);
  const [dateRange, setDateRange] = useState({ start: '', end: '' });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const params: DashboardParams = {};
      if (dateRange.start) params.startDate = dateRange.start;
      if (dateRange.end) params.endDate = dateRange.end;
      const result = await api.getDashboard(params);
      setData(result);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = (type: string) => {
    const params: DashboardParams = {};
    if (dateRange.start) params.startDate = dateRange.start;
    if (dateRange.end) params.endDate = dateRange.end;
    const url = api.getExportUrl(type, params);
    window.open(url, '_blank');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-4 text-gray-600">加载中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      <nav className="bg-white shadow-lg sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="text-2xl mr-2">🏥</div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-green-600 bg-clip-text text-transparent">
                MedDash
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <input
                  type="date"
                  value={dateRange.start}
                  onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
                  className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <span className="text-gray-500">至</span>
                <input
                  type="date"
                  value={dateRange.end}
                  onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
                  className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  onClick={fetchData}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
                >
                  查询
                </button>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => handleExport('all')}
                  className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm"
                >
                  📥 导出数据
                </button>
                <button
                  onClick={() => setShowAIChat(true)}
                  className="px-4 py-2 bg-gradient-to-r from-blue-600 to-green-600 text-white rounded-lg hover:from-blue-700 hover:to-green-700 transition-all text-sm flex items-center"
                >
                  <span className="mr-1">🤖</span> AI 助手
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800">医院运营数据看板</h1>
          <p className="text-gray-600 mt-2">实时监控医院运营状况，智能分析数据趋势</p>
        </div>

        {data && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <DashboardCard
                title="今日门诊量"
                value={data.overview.dailyOutpatient}
                change={data.overview.outpatientChange}
                color="blue"
                icon="👥"
              />
              <DashboardCard
                title="总收入"
                value={Math.round(data.overview.totalRevenue)}
                change={data.overview.revenueChange}
                unit="¥"
                color="green"
                icon="💰"
              />
              <DashboardCard
                title="在院人数"
                value={data.overview.inHospital}
                change={5.2}
                color="orange"
                icon="🏨"
              />
              <DashboardCard
                title="科室数量"
                value={data.departments.length}
                change={0}
                color="purple"
                icon="🏥"
              />
            </div>

            <div className="mb-8">
              <TrendChart
                dates={data.trends.dates}
                outpatientCounts={data.trends.outpatientCounts}
                revenues={data.trends.revenues}
              />
            </div>

            <DepartmentChart departments={data.departments} />
          </>
        )}
      </main>

      {showAIChat && <AIChat onClose={() => setShowAIChat(false)} />}
    </div>
  );
};

export default Home;