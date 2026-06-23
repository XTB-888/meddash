import React, { useState, useRef, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import { api, AIQueryResponse } from '../lib/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sql?: string;
  data?: Record<string, any>[];
  chartType?: 'line' | 'bar' | 'pie';
  explanation?: string;
}

interface AIChatProps {
  onClose: () => void;
}

const AIChat: React.FC<AIChatProps> = ({ onClose }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: '你好！我是MedDash智能助手。你可以用自然语言提问，例如：\n\n• 查看内科收入趋势\n• 各科室门诊量对比\n• 急诊量统计\n\n请告诉我你想了解什么？',
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const data: AIQueryResponse = await api.aiQuery(input);
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.explanation,
        sql: data.sql,
        data: data.result,
        chartType: data.chartType,
        explanation: data.explanation,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: '抱歉，发生了错误，请稍后重试。' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const renderChart = (msg: Message) => {
    if (!msg.data || msg.data.length === 0) return null;

    let option: any = {};
    const keys = Object.keys(msg.data[0]);

    if (msg.chartType === 'line') {
      option = {
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: msg.data.map((d: any) => d[keys[0]]) },
        yAxis: { type: 'value' },
        series: keys.slice(1).map((key, i) => ({
          name: key,
          type: 'line',
          smooth: true,
          data: msg.data.map((d: any) => d[key]),
        })),
      };
    } else if (msg.chartType === 'bar') {
      option = {
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        xAxis: { type: 'category', data: msg.data.map((d: any) => d[keys[0]]) },
        yAxis: { type: 'value' },
        series: keys.slice(1).map((key, i) => ({
          name: key,
          type: 'bar',
          data: msg.data.map((d: any) => d[key]),
        })),
      };
    } else if (msg.chartType === 'pie') {
      option = {
        tooltip: { trigger: 'item' },
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: msg.data.map((d: any, i: number) => ({
              value: d[keys[1]],
              name: d[keys[0]],
            })),
          },
        ],
      };
    }

    return (
      <div className="mt-4 bg-gray-50 rounded-lg p-4">
        <ReactECharts option={option} style={{ height: '250px' }} />
        {msg.sql && (
          <div className="mt-3">
            <p className="text-xs text-gray-500 mb-1">生成的 SQL：</p>
            <pre className="bg-gray-800 text-green-400 text-xs p-3 rounded-md overflow-x-auto">
              {msg.sql}
            </pre>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[90vh] flex flex-col">
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 rounded-t-2xl flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold flex items-center">
              <span className="mr-2">🤖</span> MedDash 智能助手
            </h2>
            <p className="text-blue-200 text-sm mt-1">用自然语言查询医院运营数据</p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:text-blue-200 text-2xl"
          >
            ×
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-2xl rounded-tr-sm'
                    : 'bg-white text-gray-800 rounded-2xl rounded-tl-sm shadow'
                } p-4`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>
                {msg.role === 'assistant' && renderChart(msg)}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white rounded-2xl rounded-tl-sm shadow p-4">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-6 border-t">
          <div className="flex space-x-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="输入你的问题，例如：查看内科收入趋势..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={isLoading}
            />
            <button
              onClick={handleSend}
              disabled={isLoading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-xl transition-colors"
            >
              发送
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIChat;
