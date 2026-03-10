import { useState, useEffect } from 'react'
import { Save } from 'lucide-react'
import { getSemesters, getCourses, createHomework } from '../api'
import Card from '../components/Card'
import PageHeader from '../components/PageHeader'

const S = {
  row:   { display: 'flex', gap: 12, alignItems: 'center', marginBottom: 12 },
  label: { width: 80, fontSize: 15, color: '#64748b', flexShrink: 0 },
  input: { flex: 1, padding: '9px 12px', border: '1px solid #e2e8f0', borderRadius: 8, fontSize: 15, background: '#fff' },
  btn:   (c) => ({ display: 'flex', alignItems: 'center', gap: 6, padding: '10px 20px', background: c, color: '#fff', border: 'none', borderRadius: 8, cursor: 'pointer', fontWeight: 600, fontSize: 15 }),
}

const DIFFICULTIES = ['簡單', '中等', '困難']
const DIFF_COLOR = { '簡單': '#10b981', '中等': '#f59e0b', '困難': '#ef4444' }

export default function Homeworks() {
  const [semesters, setSemesters] = useState([])
  const [courses, setCourses]     = useState([])
  const [selectedSem, setSelectedSem] = useState('')
  const [form, setForm] = useState({ course_id: '', homework_name: '', deadline: '', difficulty: '中等', description: '' })
  const [msg, setMsg]   = useState('')

  useEffect(() => { getSemesters().then(list => { setSemesters(list); if (list[0]) setSelectedSem(list[0].id) }) }, [])
  useEffect(() => {
    if (selectedSem) getCourses(selectedSem).then(list => { setCourses(list); if (list[0]) setForm(f => ({ ...f, course_id: list[0].id })) })
  }, [selectedSem])
  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const submit = async () => {
    if (!form.course_id || !form.homework_name || !form.deadline) { setMsg('請填寫必要欄位'); return }
    try {
      await createHomework(form)
      setMsg('ok')
      setForm(f => ({ ...f, homework_name: '', deadline: '', description: '' }))
    } catch { setMsg('新增失敗') }
  }

  return (
    <div>
      <PageHeader title="新增作業" subtitle="記錄課程作業與截止日期" />
      <Card title="作業資訊">
        <div style={S.row}>
          <span style={S.label}>選擇學期</span>
          <select style={S.input} value={selectedSem} onChange={e => setSelectedSem(e.target.value)}>
            {semesters.map(s => <option key={s.id} value={s.id}>{s.year} 學年 {s.grade}{s.semester}</option>)}
          </select>
        </div>
        <div style={S.row}>
          <span style={S.label}>選擇課程</span>
          <select style={S.input} value={form.course_id} onChange={e => set('course_id', e.target.value)}>
            {courses.map(c => <option key={c.id} value={c.id}>{c.course_name}</option>)}
          </select>
        </div>
        <div style={S.row}>
          <span style={S.label}>作業名稱</span>
          <input style={S.input} placeholder="例如：期中報告" value={form.homework_name} onChange={e => set('homework_name', e.target.value)} />
        </div>
        <div style={S.row}>
          <span style={S.label}>截止日期</span>
          <input style={S.input} type="date" value={form.deadline} onChange={e => set('deadline', e.target.value)} />
        </div>
        <div style={S.row}>
          <span style={S.label}>難度</span>
          <div style={{ display: 'flex', gap: 8 }}>
            {DIFFICULTIES.map(d => (
              <button key={d} onClick={() => set('difficulty', d)} style={{
                padding: '6px 16px', borderRadius: 20, border: '2px solid',
                borderColor: form.difficulty === d ? DIFF_COLOR[d] : '#e2e8f0',
                background: form.difficulty === d ? DIFF_COLOR[d] : '#fff',
                color: form.difficulty === d ? '#fff' : '#64748b',
                cursor: 'pointer', fontSize: 14, fontWeight: 600,
              }}>{d}</button>
            ))}
          </div>
        </div>
        <div style={{ ...S.row, alignItems: 'flex-start' }}>
          <span style={{ ...S.label, paddingTop: 8 }}>作業說明</span>
          <textarea style={{ ...S.input, height: 80, resize: 'vertical' }}
            value={form.description} onChange={e => set('description', e.target.value)} />
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <button style={S.btn('#6366f1')} onClick={submit}><Save size={15} /> 儲存作業</button>
          {msg && <span style={{ fontSize: 15, color: msg === 'ok' ? '#10b981' : '#ef4444' }}>{msg === 'ok' ? '作業新增成功！' : msg}</span>}
        </div>
      </Card>
    </div>
  )
}