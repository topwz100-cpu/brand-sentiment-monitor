import React, { useState, useEffect } from 'react'
import { Card, Row, Col, Statistic, Table, Tag, Spin, Alert } from 'antd'
import { RiseOutlined, FallOutlined, TeamOutlined, FileTextOutlined, ExclamationCircleOutlined } from '@ant-design/icons'
import { getDashboardStats, getTop20News } from '../services/api'

interface NewsItem {
  rank: number
  brand_name: string
  title: string
  content: string
  url: string
  source: string
  published_at: string
  sentiment_label: string
  sentiment_score: number
  heat_score: number
}

interface DashboardData {
  total_brands: number
  total_news_today: number
  negative_news_count: number
  top_brands: { name: string; count: number }[]
}

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState<DashboardData | null>(null)
  const [topNews, setTopNews] = useState<NewsItem[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [statsData, topNewsData] = await Promise.all([
        getDashboardStats(),
        getTop20News()
      ])
      setStats(statsData)
      setTopNews(topNewsData)
    } catch (err) {
      setError('数据加载失败，请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  const getSentimentTag = (label: string) => {
    switch (label) {
      case 'positive':
        return <Tag color="success">正面</Tag>
      case 'negative':
        return <Tag color="error">负面</Tag>
      default:
        return <Tag color="default">中性</Tag>
    }
  }

  const columns = [
    {
      title: '排名',
      dataIndex: 'rank',
      key: 'rank',
      width: 80,
      render: (rank: number) => (
        <span style={{ fontWeight: 'bold', color: rank <= 3 ? '#ff4d4f' : '#666' }}>
          {rank}
        </span>
      ),
    },
    {
      title: '品牌',
      dataIndex: 'brand_name',
      key: 'brand_name',
      width: 150,
    },
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      render: (text: string, record: NewsItem) => (
        <a href={record.url} target="_blank" rel="noopener noreferrer" style={{ color: '#1890ff' }}>
          {text}
        </a>
      ),
    },
    {
      title: '来源',
      dataIndex: 'source',
      key: 'source',
      width: 120,
    },
    {
      title: '情感',
      dataIndex: 'sentiment_label',
      key: 'sentiment_label',
      width: 100,
      render: (label: string) => getSentimentTag(label),
    },
    {
      title: '热度',
      dataIndex: 'heat_score',
      key: 'heat_score',
      width: 100,
      render: (score: number) => (
        <span style={{ color: score > 80 ? '#ff4d4f' : score > 50 ? '#faad14' : '#52c41a' }}>
          {score?.toFixed(1)}
        </span>
      ),
    },
    {
      title: '时间',
      dataIndex: 'published_at',
      key: 'published_at',
      width: 180,
      render: (date: string) => new Date(date).toLocaleString('zh-CN'),
    },
  ]

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
        <p>正在加载数据...</p>
      </div>
    )
  }

  if (error) {
    return <Alert message={error} type="error" showIcon />
  }

  return (
    <div>
      <h2 style={{ marginBottom: '24px' }}>📊 今日舆情概览</h2>
      
      {/* 统计卡片 */}
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="监测品牌数"
              value={stats?.total_brands || 0}
              prefix={<TeamOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="今日新闻数"
              value={stats?.total_news_today || 0}
              prefix={<FileTextOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="负面新闻"
              value={stats?.negative_news_count || 0}
              prefix={<ExclamationCircleOutlined />}
              valueStyle={{ color: '#ff4d4f' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="正面新闻占比"
              value={stats?.total_news_today ? 
                Math.round(((stats.total_news_today - stats.negative_news_count) / stats.total_news_today) * 100) : 0}
              suffix="%"
              prefix={<RiseOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Top20 新闻表格 */}
      <Card 
        title="🔥 今日Top20热门新闻" 
        extra={<span style={{ color: '#999' }}>每日自动更新</span>}
      >
        <Table
          columns={columns}
          dataSource={topNews}
          rowKey="rank"
          pagination={false}
          scroll={{ x: 1200 }}
        />
      </Card>
    </div>
  )
}

export default Dashboard
