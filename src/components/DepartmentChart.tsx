import React from 'react';
import ReactECharts from 'echarts-for-react';

interface Department {
  name: string;
  outpatientCount: number;
  revenue: number;
}

interface DepartmentChartProps {
  departments: Department[];
}

const DepartmentChart: React.FC<DepartmentChartProps> = ({ departments }) => {
  const barOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
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
      type: 'value',
    },
    yAxis: {
      type: 'category',
      data: departments.map((d) => d.name),
    },
    series: [
      {
        name: '门诊量',
        type: 'bar',
        data: departments.map((d) => d.outpatientCount),
        itemStyle: {
          color: '#3b82f6',
        },
      },
      {
        name: '收入',
        type: 'bar',
        data: departments.map((d) => d.revenue / 1000),
        itemStyle: {
          color: '#10b981',
        },
      },
    ],
  };

  const pieOption = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)',
    },
    legend: {
      orient: 'vertical',
      left: 'left',
    },
    series: [
      {
        name: '收入占比',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: false,
          position: 'center',
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold',
          },
        },
        labelLine: {
          show: false,
        },
        data: departments.map((d, index) => ({
          value: d.revenue,
          name: d.name,
          itemStyle: {
            color: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'][index],
          },
        })),
      },
    ],
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">科室对比</h3>
        <ReactECharts option={barOption} style={{ height: '300px' }} />
        <p className="text-xs text-gray-500 mt-2 text-center">* 收入单位：千元</p>
      </div>
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">收入占比</h3>
        <ReactECharts option={pieOption} style={{ height: '300px' }} />
      </div>
    </div>
  );
};

export default DepartmentChart;
