import React, { useState, useEffect } from 'react'
import { Card, Row, Col, Spin, Alert } from 'antd'
import ReactECharts from 'echarts-for-react'
import { getSentimentTrends, getBrandDistribution } from '../services/api'

interface TrendData {
  [date: string]: {
    positive: number
    negative: number
    neutral: number
  }
}

interface DistributionData {
  name: string
  value: number
}

const Analytics: React.FC = () => {
  const [trends, setTrends] = useState<TrendData>({})
  const [distribution, setDistribution] = useState<DistributionData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [trendsData, distributionData] = await Promise.all([
        getSentimentTrends(),
        getBrandDistribution()
      ])
      setTrends(trendsData)
      setDistribution(distributionData)
    } catch (err) {
      setError('数据加载失败')
    } finally {
      setLoading(false)
    }
  }

  // 情感趋势图配置
  const getTrendOption = () => {
    const dates = Object.keys(trends).sort()
    const positiveData = dates.map(date => trends[date].positive)
    const negativeData = dates.map(date => trends[date].negative)
    const neutralData = dates.map(date => trends[date].neutral)

    return {
      title: {
        text: '情感趋势分析',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        }
      },
      legend: {
        data: ['正面', '负面', '中性'],
        bottom: 0
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: dates
      },
      yAxis: {
        type: 'value',
        name: '新闻数量'
      },
      series: [
        {
          name: '正面',
          type: 'line',
          smooth: true,
          data: positiveData,
          itemStyle: { color: '#52c41a' }
        },
        {
          name: '负面',
          type: 'line',
          smooth: true,
          data: negativeData,
          itemStyle: { color: '#ff4d4f' }
        },
        {
          name: '中性',
          type: 'line',
          smooth: true,
          data: neutralData,
          itemStyle: { color: '#faad14' }
        }
      ]
    }
  }

  // 品牌分布图配置
  const getDistributionOption = () => {
    return {
      title: {
        text: '品牌新闻分布',
        left: 'center'
      },
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        top: 'middle'
      },
      series: [
        {
          name: '新闻数量',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 20,
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: distribution
        }
      ]
    }
  }

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
      <h2 style={{ marginBottom: '24px' }}>📈 数据分析</h2>
      
      <Row gutter={16}>
        <Col span={24}>
          <Card>
            <ReactECharts option={getTrendOption()} style={{ height: '400px' }} />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: '24px' }}>
        <Col span={24}>
          <Card>
            <ReactECharts option={getDistributionOption()} style={{ height: '400px' }} />
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default Analytics
