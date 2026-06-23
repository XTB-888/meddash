import React from 'react';

interface DashboardCardProps {
  title: string;
  value: number | string;
  change: number;
  unit?: string;
  icon?: React.ReactNode;
  color?: 'blue' | 'green' | 'orange' | 'purple';
}

const DashboardCard: React.FC<DashboardCardProps> = ({
  title,
  value,
  change,
  unit = '',
  icon,
  color = 'blue',
}) => {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    orange: 'from-orange-500 to-orange-600',
    purple: 'from-purple-500 to-purple-600',
  };

  const isPositive = change >= 0;

  return (
    <div className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 overflow-hidden">
      <div className={`bg-gradient-to-r ${colorClasses[color]} p-6 text-white`}>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-blue-100 text-sm font-medium">{title}</p>
            <p className="text-3xl font-bold mt-2">
              {unit === '¥' && '¥'}
              {typeof value === 'number' ? value.toLocaleString() : value}
              {unit === '%' && '%'}
            </p>
          </div>
          {icon && <div className="text-4xl opacity-80">{icon}</div>}
        </div>
      </div>
      <div className="p-4">
        <div className="flex items-center">
          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
            isPositive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          }`}>
            <span className={`mr-1 ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
              {isPositive ? '↑' : '↓'}
            </span>
            {Math.abs(change)}%
          </span>
          <span className="text-gray-500 text-sm ml-2">较昨日</span>
        </div>
      </div>
    </div>
  );
};

export default DashboardCard;
