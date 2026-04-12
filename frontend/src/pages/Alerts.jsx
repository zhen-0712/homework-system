import { useState, useEffect } from 'react'
import { RefreshCw, Info } from 'lucide-react'
import { getUpcomingExams } from '../api'
import Card from '../components/Card'
import PageHeader from '../components/PageHeader'

const MARK_STYLE = {
  today:  { bg: '#fef2f2', color: '#ef4444', border: '#fecaca' },
  urgent: { bg: '#fff7ed', color: '#f97316', border: '#fed7aa' },
  week:   { bg: '#eff6ff', color: '#3b82f6', border: '#bfdbfe' },
  normal: { bg: '#f8fafc', color: '#334155', border: '#e2e8f0' },
}

function getMarkStyle(mark) {
  if (mark === '今天') return MARK_STYLE.today
  if (mark === '緊急') return MARK_STYLE.urgent
  if (mark === '本週') return MARK_STYLE.week
  return MARK_STYLE.normal
}

function markLabel(mark) {
  return mark || ''
}

function fetchExams(setter) {
  return getUpcomingExams().then(d => setter(d))
}

export default function Alerts() {
  const [data, setData]       = useState({ items: [], total_upcoming: 0 })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    let cancelled = false
    getUpcomingExams().then(d => {
      if (!cancelled) setData(d)
    })
    return () => { cancelled = true }
  }, [])

  const load = () => {
    setLoading(true)
    fetchExams(setData).then(() => setLoading(false))
  }

  return (
    <div>
      <PageHeader title="考試提醒" subtitle="未來兩週內的考試預覽" />

      <div style={{
        padding: '10px 14px', background: '#eff6ff', borderRadius: 8,
        border: '1px solid #bfdbfe', fontSize: 15, color: '#1d4ed8',
        marginBottom: 20, display: 'flex', alignItems: 'center', gap: 8,
      }}>
        <Info size={15} />
        紅色 = 今天 &nbsp; 橘色 = 緊急（3天內）&nbsp; 藍色 = 本週 &nbsp; 無標記 = 兩週內
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <span style={{ fontSize: 15, color: '#ef4444', fontWeight: 700 }}>
          未來兩週考試：{data.items.length} 場 &nbsp; 總未考：{data.total_upcoming} 場
        </span>
        <button onClick={load} style={{
          display: 'flex', alignItems: 'center', gap: 6,
          padding: '7px 16px', background: '#6366f1', color: '#fff',
          border: 'none', borderRadius: 8, cursor: 'pointer', fontSize: 15, fontWeight: 600,
        }}>
          <RefreshCw size={14} /> {loading ? '載入中...' : '重新整理'}
        </button>
      </div>

      <Card title="近期考試">
        {data.items.length === 0 && (
          <p style={{ color: '#94a3b8', fontSize: 15 }}>未來兩週沒有考試！</p>
        )}
        {data.items.map(ex => {
          const st = getMarkStyle(ex.mark)
          const label = markLabel(ex.mark)
          return (
            <div key={ex.id} style={{
              padding: '14px 16px', borderRadius: 10, marginBottom: 10,
              background: st.bg, border: `1px solid ${st.border}`,
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  {label && (
                    <span style={{
                      padding: '2px 8px', borderRadius: 12, fontSize: 13,
                      fontWeight: 700, background: st.color, color: '#fff',
                    }}>{label}</span>
                  )}
                  <span style={{ fontWeight: 600, fontSize: 16, color: st.color }}>{ex.exam_name}</span>
                </div>
                <span style={{ fontSize: 15, fontWeight: 700, color: st.color }}>剩 {ex.days_left} 天</span>
              </div>
              <div style={{ fontSize: 14, color: '#64748b', marginTop: 6 }}>
                {ex.course_name}
                {ex.exam_date && <span> &nbsp; {ex.exam_date}</span>}
                {ex.exam_time && <span> &nbsp; {ex.exam_time}</span>}
                {ex.location  && <span> &nbsp; {ex.location}</span>}
              </div>
            </div>
          )
        })}
      </Card>
    </div>
  )
}