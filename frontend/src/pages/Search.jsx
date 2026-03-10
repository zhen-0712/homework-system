import { useState, useEffect } from 'react'
import { Search as SearchIcon, Eye, Trash2, Pencil, X, Check } from 'lucide-react'
import { getSemesters, getCourses, getHomeworks, updateHomework, deleteHomework } from '../api'
import Card from '../components/Card'
import PageHeader from '../components/PageHeader'

const S = {
  input: { padding: '9px 12px', border: '1px solid #e2e8f0', borderRadius: 8, fontSize: 15, background: '#fff' },
  btn:   (c) => ({ display: 'flex', alignItems: 'center', gap: 5, padding: '9px 16px', background: c, color: '#fff', border: 'none', borderRadius: 8, cursor: 'pointer', fontWeight: 600, fontSize: 14 }),
  badge: (color) => ({ padding: '2px 8px', borderRadius: 12, fontSize: 13, fontWeight: 600, background: color + '20', color }),
}
const STATUS_COLOR = { '未完成': '#ef4444', '進行中': '#f59e0b', '已完成': '#10b981' }
const DIFF_COLOR   = { '簡單': '#10b981', '中等': '#f59e0b', '困難': '#ef4444' }

export default function Search() {
  const [semesters, setSemesters]         = useState([])
  const [courses, setCourses]             = useState([])
  const [homeworks, setHomeworks]         = useState([])
  const [selectedSem, setSelectedSem]     = useState('')
  const [selectedCourse, setSelectedCourse] = useState('')
  const [editing, setEditing]             = useState(null)
  const [editForm, setEditForm]           = useState({ status: '未完成', score: 0 })

  useEffect(() => { getSemesters().then(list => { setSemesters(list); if (list[0]) setSelectedSem(list[0].id) }) }, [])
  useEffect(() => { if (selectedSem) getCourses(selectedSem).then(list => { setCourses(list); setSelectedCourse(list[0]?.id || '') }) }, [selectedSem])

  const search   = () => { if (selectedCourse) getHomeworks(selectedCourse).then(setHomeworks) }
  const startEdit = (hw) => { setEditing(hw.id); setEditForm({ status: hw.status, score: hw.score }) }
  const saveEdit  = async () => { await updateHomework(editing, editForm); setEditing(null); getHomeworks(selectedCourse).then(setHomeworks) }

  return (
    <div>
      <PageHeader title="作業查詢" subtitle="查詢、檢視與更新作業狀態" />
      <Card>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
          <select style={S.input} value={selectedSem} onChange={e => setSelectedSem(e.target.value)}>
            {semesters.map(s => <option key={s.id} value={s.id}>{s.year} 學年 {s.grade}{s.semester}</option>)}
          </select>
          <select style={S.input} value={selectedCourse} onChange={e => setSelectedCourse(e.target.value)}>
            {courses.map(c => <option key={c.id} value={c.id}>{c.course_name}</option>)}
          </select>
          <button style={S.btn('#6366f1')} onClick={search}><SearchIcon size={14} /> 查詢</button>
        </div>
      </Card>

      {homeworks.length > 0 && (
        <Card title={`作業列表（${homeworks.length} 筆）`}>
          {homeworks.map(hw => (
            <div key={hw.id} style={{ padding: '12px 14px', borderRadius: 10, background: '#f8fafc', marginBottom: 10, border: '1px solid #e2e8f0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <span style={{ fontWeight: 600, fontSize: 16, color: '#0f172a' }}>{hw.homework_name}</span>
                  <span style={{ ...S.badge(DIFF_COLOR[hw.difficulty] || '#64748b'), marginLeft: 8 }}>{hw.difficulty}</span>
                  <span style={{ ...S.badge(STATUS_COLOR[hw.status] || '#64748b'), marginLeft: 6 }}>{hw.status}</span>
                </div>
                <div style={{ display: 'flex', gap: 6 }}>
                  <button style={S.btn('#6366f1')} onClick={() => startEdit(hw)}><Pencil size={13} /> 更新</button>
                  <button style={S.btn('#ef4444')} onClick={() => deleteHomework(hw.id).then(() => getHomeworks(selectedCourse).then(setHomeworks))}><Trash2 size={13} /></button>
                </div>
              </div>
              <div style={{ fontSize: 14, color: '#64748b', marginTop: 6 }}>截止：{hw.deadline} · 成績：{hw.score} 分</div>
              {hw.description && <div style={{ fontSize: 14, color: '#94a3b8', marginTop: 4 }}>{hw.description}</div>}

              {editing === hw.id && (
                <div style={{ marginTop: 12, padding: 12, background: '#fff', borderRadius: 8, border: '1px solid #e2e8f0' }}>
                  <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 8 }}>
                    <span style={{ fontSize: 14, color: '#64748b' }}>狀態：</span>
                    {['未完成','進行中','已完成'].map(s => (
                      <button key={s} onClick={() => setEditForm(f => ({ ...f, status: s }))} style={{
                        padding: '4px 12px', borderRadius: 16, border: '1.5px solid',
                        borderColor: editForm.status === s ? STATUS_COLOR[s] : '#e2e8f0',
                        background: editForm.status === s ? STATUS_COLOR[s] : '#fff',
                        color: editForm.status === s ? '#fff' : '#64748b',
                        cursor: 'pointer', fontSize: 14,
                      }}>{s}</button>
                    ))}
                  </div>
                  <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                    <span style={{ fontSize: 14, color: '#64748b' }}>成績：</span>
                    <input type="number" style={{ width: 70, padding: '4px 8px', border: '1px solid #e2e8f0', borderRadius: 6, fontSize: 15 }}
                      value={editForm.score} onChange={e => setEditForm(f => ({ ...f, score: Number(e.target.value) }))} />
                    <button style={S.btn('#10b981')} onClick={saveEdit}><Check size={13} /> 儲存</button>
                    <button style={S.btn('#94a3b8')} onClick={() => setEditing(null)}><X size={13} /> 取消</button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </Card>
      )}
      {homeworks.length === 0 && selectedCourse && (
        <Card><p style={{ color: '#94a3b8', fontSize: 15 }}>此課程尚無作業，點擊查詢載入</p></Card>
      )}
    </div>
  )
}