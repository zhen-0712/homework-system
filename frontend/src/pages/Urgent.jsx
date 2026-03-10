import { useState, useEffect } from 'react'
import { RefreshCw, AlertCircle, CheckCircle2 } from 'lucide-react'
import { getUrgentHomeworks } from '../api'
import Card from '../components/Card'
import PageHeader from '../components/PageHeader'

const MARK_STYLE = {
  today:  { bg: '#fef2f2', color: '#ef4444', border: '#fecaca' },
  urgent: { bg: '#fff7ed', color: '#f97316', border: '#fed7aa' },
  normal: { bg: '#f8fafc', color: '#334155', border: '#e2e8f0' },
}

function getMarkStyle(mark) {
  return MARK_STYLE[mark] || MARK_STYLE.normal
}

function markLabel(mark) {
  if (mark === 'today')  return '今天'
  if (mark === 'urgent') return '緊急'
  return ''
}

function fetchUrgent(setter) {
  return getUrgentHomeworks().then(d => setter(d))
}

export default function Urgent() {
  const [data, setData]       = useState({ items: [], total_incomplete: 0 })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    let cancelled = false
    getUrgentHomeworks().then(d => {
      if (!cancelled) setData(d)
    })
    return () => { cancelled = true }
  }, [])

  const load = () => {
    setLoading(true)
    fetchUrgent(setData).then(() => setLoading(false))
  }

  return (
    <div>
      <PageHeader title="本週待辦" subtitle="未來 7 天內截止的作業" />

      <div style={{
        padding: '10px 14px', background: '#fff7ed', borderRadius: 8,
        border: '1px solid #fed7aa', fontSize: 15, color: '#9a3412',
        marginBottom: 20, display: 'flex', alignItems: 'center', gap: 8,
      }}>
        <AlertCircle size={15} />
        紅色 = 今天到期 &nbsp; 橘色 = 3天內（緊急）&nbsp; 無標記 = 本週內
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <span style={{ fontSize: 15, color: '#10b981', fontWeight: 700, display: 'flex', alignItems: 'center', gap: 6 }}>
          <CheckCircle2 size={15} />
          本週待完成 {data.items.length} 件 &nbsp; 總未完成 {data.total_incomplete} 件
        </span>
        <button onClick={load} style={{
          display: 'flex', alignItems: 'center', gap: 6,
          padding: '7px 16px', background: '#6366f1', color: '#fff',
          border: 'none', borderRadius: 8, cursor: 'pointer', fontSize: 15, fontWeight: 600,
        }}>
          <RefreshCw size={14} /> {loading ? '載入中...' : '重新整理'}
        </button>
      </div>

      <Card title="本週待完成">
        {data.items.length === 0 && (
          <p style={{ color: '#94a3b8', fontSize: 15 }}>本週沒有待辦作業！</p>
        )}
        {data.items.map(hw => {
          const st = getMarkStyle(hw.mark)
          const label = markLabel(hw.mark)
          return (
            <div key={hw.id} style={{
              padding: '12px 14px', borderRadius: 10, marginBottom: 10,
              background: st.bg, border: `1px solid ${st.border}`,
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  {label && (
                    <span style={{
                      padding: '2px 8px', borderRadius: 12, fontSize: 13,
                      fontWeight: 700, background: st.color, color: '#fff',
                    }}>{label}</span>
                  )}
                  <span style={{ fontWeight: 600, fontSize: 16, color: st.color }}>{hw.homework_name}</span>
                </div>
                <span style={{ fontSize: 15, fontWeight: 700, color: st.color }}>剩 {hw.days_left} 天</span>
              </div>
              <div style={{ fontSize: 14, color: '#64748b', marginTop: 4 }}>
                {hw.course_name} &nbsp; 截止：{hw.deadline}
              </div>
            </div>
          )
        })}
      </Card>
    </div>
  )
}