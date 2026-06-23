import React from 'react';
import ReactECharts from 'echarts-for-react';

interface TrendChartProps {
  dates: string[];
  outpatientCounts: number[];
  revenues: number[];
}

const TrendChart: React.FC<TrendChartProps> = ({ dates, outpatientCounts, revenues }) => {
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
      },
    },
    legend: {
      data: ['门诊量', '收入'],
      top: 0,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates,
      axisLabel: {
        rotate: 45,
        fontSize: 10,
      },
    },
    yAxis: [
      {
        type: 'value',
        name: '门诊量',
        position: 'left',
        axisLine: {
          lineStyle: {
            color: '#3b82f6',
          },
        },
      },
      {
        type: 'value',
        name: '收入(元)',
        position: 'right',
        axisLine: {
          lineStyle: {
            color: '#10b981',
          },
        },
      },
    ],
    series: [
      {
        name: '门诊量',
        type: 'line',
        smooth: true,
        data: outpatientCounts,
        itemStyle: {
          color: '#3b82f6',
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
              { offset: 1, color: 'rgba(59, 130, 246, 0.05)' },
            ],
          },
        },
      },
      {
        name: '收入',
        type: 'line',
        smooth: true,
        yAxisIndex: 1,
        data: revenues,
        itemStyle: {
          color: '#10b981',
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(16, 185, 129, 0.3)' },
              { offset: 1, color: 'rgba(16, 185, 129, 0.05)' },
            ],
          },
        },
      },
    ],
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">门诊量与收入趋势</h3>
      <ReactECharts option={option} style={{ height: '350px' }} />
    </div>
  );
};

export default TrendChart;
