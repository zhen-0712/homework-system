import { useState, useEffect } from 'react'
import { Plus, Trash2 } from 'lucide-react'
import { getSemesters, getCourses, createCourse, deleteCourse } from '../api'
import Card from '../components/Card'
import PageHeader from '../components/PageHeader'

const S = {
  row:   { display: 'flex', gap: 12, alignItems: 'center', marginBottom: 12 },
  label: { width: 80, fontSize: 15, color: '#64748b', flexShrink: 0 },
  input: { flex: 1, padding: '9px 12px', border: '1px solid #e2e8f0', borderRadius: 8, fontSize: 15, background: '#fff' },
  btn:   (c) => ({ display: 'flex', alignItems: 'center', gap: 6, padding: '10px 20px', background: c, color: '#fff', border: 'none', borderRadius: 8, cursor: 'pointer', fontWeight: 600, fontSize: 15 }),
  item:  { display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 14px', borderRadius: 8, background: '#f8fafc', marginBottom: 8, fontSize: 15, color: '#334155' },
}

export default function Courses() {
  const [semesters, setSemesters] = useState([])
  const [courses, setCourses]     = useState([])
  const [selectedSem, setSelectedSem] = useState('')
  const [form, setForm] = useState({ course_name: '', teacher: '', class_time: '', credits: 3 })
  const [msg, setMsg]   = useState('')

  useEffect(() => { getSemesters().then(list => { setSemesters(list); if (list[0]) setSelectedSem(list[0].id) }) }, [])
  useEffect(() => { if (selectedSem) getCourses(selectedSem).then(setCourses) }, [selectedSem])
  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const submit = async () => {
    if (!form.course_name || !form.teacher || !selectedSem) { setMsg('請填寫必要欄位'); return }
    try {
      await createCourse({ ...form, semester_id: selectedSem, credits: Number(form.credits) })
      setMsg('ok')
      setForm({ course_name: '', teacher: '', class_time: '', credits: 3 })
      getCourses(selectedSem).then(setCourses)
    } catch (e) { setMsg(e.response?.data?.detail || '新增失敗') }
  }

  return (
    <div>
      <PageHeader title="課程管理" subtitle="管理各學期的課程資訊" />
      <Card title="新增課程">
        <div style={S.row}>
          <span style={S.label}>選擇學期</span>
          <select style={S.input} value={selectedSem} onChange={e => setSelectedSem(e.target.value)}>
            {semesters.map(s => <option key={s.id} value={s.id}>{s.year} 學年 {s.grade}{s.semester}</option>)}
          </select>
        </div>
        {[['課程名稱','course_name','例如：資料庫系統'],['授課教師','teacher','例如：王老師'],['上課時間','class_time','例如：週一 13:00']].map(([lbl,key,ph]) => (
          <div key={key} style={S.row}>
            <span style={S.label}>{lbl}</span>
            <input style={S.input} placeholder={ph} value={form[key]} onChange={e => set(key, e.target.value)} />
          </div>
        ))}
        <div style={S.row}>
          <span style={S.label}>學分數</span>
          <input style={{ ...S.input, flex: 'none', width: 80 }} type="number" value={form.credits} onChange={e => set('credits', e.target.value)} />
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginTop: 4 }}>
          <button style={S.btn('#10b981')} onClick={submit}><Plus size={15} /> 新增課程</button>
          {msg && <span style={{ fontSize: 15, color: msg === 'ok' ? '#10b981' : '#ef4444' }}>{msg === 'ok' ? '新增成功！' : msg}</span>}
        </div>
      </Card>

      <Card title="課程列表">
        {courses.length === 0 && <p style={{ color: '#94a3b8', fontSize: 15 }}>尚無課程資料</p>}
        {courses.map(c => (
          <div key={c.id} style={S.item}>
            <div>
              <span style={{ fontWeight: 600 }}>{c.course_name}</span>
              <span style={{ color: '#64748b', marginLeft: 10 }}>{c.teacher} · {c.credits} 學分</span>
              {c.class_time && <span style={{ color: '#94a3b8', marginLeft: 8, fontSize: 14 }}>{c.class_time}</span>}
            </div>
            <button onClick={() => deleteCourse(c.id).then(() => getCourses(selectedSem).then(setCourses))}
              style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', display: 'flex', alignItems: 'center' }}>
              <Trash2 size={14} />
            </button>
          </div>
        ))}
      </Card>
    </div>
  )
}