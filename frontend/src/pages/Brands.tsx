import React, { useState, useEffect } from 'react'
import { Table, Button, Modal, Form, Input, Switch, Tag, Space, message, Popconfirm } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import { getBrands, createBrand, updateBrand, deleteBrand } from '../services/api'

interface Brand {
  id: number
  name: string
  search_keywords: string
  category: string
  is_active: boolean
  created_at: string
}

const Brands: React.FC = () => {
  const [brands, setBrands] = useState<Brand[]>([])
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [editingBrand, setEditingBrand] = useState<Brand | null>(null)
  const [form] = Form.useForm()

  useEffect(() => {
    fetchBrands()
  }, [])

  const fetchBrands = async () => {
    try {
      setLoading(true)
      const data = await getBrands()
      setBrands(data)
    } catch (error) {
      message.error('获取品牌列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = () => {
    setEditingBrand(null)
    form.resetFields()
    setModalVisible(true)
  }

  const handleEdit = (brand: Brand) => {
    setEditingBrand(brand)
    form.setFieldsValue(brand)
    setModalVisible(true)
  }

  const handleDelete = async (id: number) => {
    try {
      await deleteBrand(id)
      message.success('删除成功')
      fetchBrands()
    } catch (error) {
      message.error('删除失败')
    }
  }

  const handleSave = async (values: any) => {
    try {
      if (editingBrand) {
        await updateBrand(editingBrand.id, values)
        message.success('更新成功')
      } else {
        await createBrand(values)
        message.success('创建成功')
      }
      setModalVisible(false)
      fetchBrands()
    } catch (error) {
      message.error('保存失败')
    }
  }

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '品牌名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '搜索关键词',
      dataIndex: 'search_keywords',
      key: 'search_keywords',
      render: (text: string) => text || '-',
    },
    {
      title: '品类',
      dataIndex: 'category',
      key: 'category',
      render: (text: string) => text || '-',
    },
    {
      title: '状态',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (isActive: boolean) => (
        <Tag color={isActive ? 'success' : 'default'}>
          {isActive ? '启用' : '停用'}
        </Tag>
      ),
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleString('zh-CN'),
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Brand) => (
        <Space size="middle">
          <Button type="primary" icon={<EditOutlined />} onClick={() => handleEdit(record)}>
            编辑
          </Button>
          <Popconfirm
            title="确定要删除这个品牌吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h2>🏢 品牌管理</h2>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
          添加品牌
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={brands}
        rowKey="id"
        loading={loading}
        pagination={{ pageSize: 10 }}
      />

      <Modal
        title={editingBrand ? '编辑品牌' : '添加品牌'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => form.submit()}
      >
        <Form form={form} onFinish={handleSave} layout="vertical">
          <Form.Item
            name="name"
            label="品牌名称"
            rules={[{ required: true, message: '请输入品牌名称' }]}
          >
            <Input placeholder="请输入品牌名称" />
          </Form.Item>
          <Form.Item
            name="search_keywords"
            label="搜索关键词"
            rules={[{ required: false }]}
          >
            <Input placeholder="多个关键词用逗号分隔" />
          </Form.Item>
          <Form.Item
            name="category"
            label="品类"
            rules={[{ required: false }]}
          >
            <Input placeholder="例如：美妆、食品、服装" />
          </Form.Item>
          <Form.Item
            name="is_active"
            label="启用监测"
            valuePropName="checked"
            initialValue={true}
          >
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default Brands
