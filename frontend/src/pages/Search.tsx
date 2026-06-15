import React, { useState } from 'react'
import { Input, Button, Card, List, Tag, Spin, Alert, Select, Space } from 'antd'
import { SearchOutlined } from '@ant-design/icons'
import { searchNews } from '../services/api'

const { Search } = Input
const { Option } = Select

interface NewsItem {
  id: number
  title: string
  content: string
  url: string
  source: string
  source_type: string
  published_at: string
  brand_name: string
  sentiment_label?: string
  sentiment_score?: number
}

const SearchPage: React.FC = () => {
  const [keyword, setKeyword] = useState('')
  const [days, setDays] = useState(7)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<NewsItem[]>([])
  const [total, setTotal] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [searched, setSearched] = useState(false)

  const handleSearch = async () => {
    if (!keyword.trim()) return
    
    try {
      setLoading(true)
      setError(null)
      setSearched(true)
      
      const data = await searchNews(keyword, days)
      setResults(data.articles)
      setTotal(data.total)
    } catch (err) {
      setError('搜索失败，请稍后重试')
    } finally {
      setLoading(false)
    }
  }

  const getSentimentTag = (label?: string) => {
    switch (label) {
      case 'positive':
        return <Tag color="success">正面</Tag>
      case 'negative':
        return <Tag color="error">负面</Tag>
      default:
        return <Tag color="default">中性</Tag>
    }
  }

  const getSourceTag = (type: string) => {
    switch (type) {
      case 'weibo':
        return <Tag color="blue">微博</Tag>
      default:
        return <Tag color="green">新闻</Tag>
    }
  }

  return (
    <div>
      <h2 style={{ marginBottom: '24px' }}>🔍 舆情搜索</h2>
      
      {/* 搜索区域 */}
      <Card style={{ marginBottom: '24px' }}>
        <Space direction="vertical" size="middle" style={{ width: '100%' }}>
          <Search
            placeholder="输入品牌名称或关键词搜索..."
            allowClear
            enterButton={<><SearchOutlined /> 搜索</>}
            size="large"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            onSearch={handleSearch}
            loading={loading}
          />
          <Space>
            <span>时间范围：</span>
            <Select value={days} onChange={setDays} style={{ width: 120 }}>
              <Option value={1}>今天</Option>
              <Option value={3}>近3天</Option>
              <Option value={7}>近7天</Option>
              <Option value={30}>近30天</Option>
            </Select>
          </Space>
        </Space>
      </Card>

      {/* 搜索结果 */}
      {searched && (
        <Card title={`搜索结果 (${total}条)`}>
          {loading ? (
            <div style={{ textAlign: 'center', padding: '50px' }}>
              <Spin size="large" />
              <p>正在搜索...</p>
            </div>
          ) : error ? (
            <Alert message={error} type="error" showIcon />
          ) : results.length === 0 ? (
            <Alert message="未找到相关资讯" type="info" showIcon />
          ) : (
            <List
              itemLayout="vertical"
              dataSource={results}
              renderItem={(item) => (
                <List.Item
                  key={item.id}
                  actions={[
                    <span>来源: {item.source || '未知'}</span>,
                    <span>时间: {new Date(item.published_at).toLocaleString('zh-CN')}</span>,
                    getSentimentTag(item.sentiment_label),
                    getSourceTag(item.source_type),
                  ]}
                >
                  <List.Item.Meta
                    title={
                      <a href={item.url} target="_blank" rel="noopener noreferrer" style={{ fontSize: '16px' }}>
                        {item.title}
                      </a>
                    }
                    description={
                      <div>
                        <p style={{ color: '#666', marginTop: '8px' }}>
                          {item.content?.substring(0, 200)}...
                        </p>
                        {item.brand_name && (
                          <Tag color="blue" style={{ marginTop: '8px' }}>
                            {item.brand_name}
                          </Tag>
                        )}
                      </div>
                    }
                  />
                </List.Item>
              )}
            />
          )}
        </Card>
      )}
    </div>
  )
}

export default SearchPage
