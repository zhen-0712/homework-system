import { useState, useEffect } from 'react'
import { Plus, Trash2, Save, Pencil, Check, X } from 'lucide-react'
import { getSemesters, getCourses, getExams, createExam, updateExam, deleteExam } from '../api'
import Card from '../components/Card'
import PageHeader from '../components/PageHeader'

const S = {
  row:   { display: 'flex', gap: 12, alignItems: 'center', marginBottom: 12 },
  label: { width: 80, fontSize: 15, color: '#64748b', flexShrink: 0 },
  input: { flex: 1, padding: '9px 12px', border: '1px solid #e2e8f0', borderRadius: 8, fontSize: 15, background: '#fff' },
  btn:   (c) => ({ display: 'flex', alignItems: 'center', gap: 5, padding: '9px 16px', background: c, color: '#fff', border: 'none', borderRadius: 8, cursor: 'pointer', fontWeight: 600, fontSize: 14 }),
}

export default function Exams() {
  const [semesters, setSemesters] = useState([])
  const [courses, setCourses]     = useState([])
  const [exams, setExams]         = useState([])
  const [selectedSem, setSelectedSem]       = useState('')
  const [selectedCourse, setSelectedCourse] = useState('')
  const [form, setForm]     = useState({ exam_name: '', exam_date: '', exam_time: '', location: '', scope: '', notes: '' })
  const [editing, setEditing]   = useState(null)
  const [editForm, setEditForm] = useState({ status: '未考', score: 0 })
  const [msg, setMsg] = useState('')

  useEffect(() => { getSemesters().then(list => { setSemesters(list); if (list[0]) setSelectedSem(list[0].id) }) }, [])
  useEffect(() => {
    if (selectedSem) getCourses(selectedSem).then(list => {
      setCourses(list)
      if (list[0]) { setSelectedCourse(list[0].id); getExams(list[0].id).then(setExams) }
    })
  }, [selectedSem])
  useEffect(() => { if (selectedCourse) getExams(selectedCourse).then(setExams) }, [selectedCourse])

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))
  const submit = async () => {
    if (!form.exam_name || !form.exam_date || !selectedCourse) { setMsg('請填寫必要欄位'); return }
    try {
      await createExam({ ...form, course_id: selectedCourse, semester_id: selectedSem })
      setMsg('ok')
      setForm({ exam_name: '', exam_date: '', exam_time: '', location: '', scope: '', notes: '' })
      getExams(selectedCourse).then(setExams)
    } catch { setMsg('新增失敗') }
  }
  const saveEdit = async () => { await updateExam(editing, editForm); setEditing(null); getExams(selectedCourse).then(setExams) }

  return (
    <div>
      <PageHeader title="考試管理" subtitle="記錄與追蹤考試資訊" />
      <Card title="新增考試">
        <div style={S.row}>
          <span style={S.label}>選擇學期</span>
          <select style={S.input} value={selectedSem} onChange={e => setSelectedSem(e.target.value)}>
            {semesters.map(s => <option key={s.id} value={s.id}>{s.year} 學年 {s.grade}{s.semester}</option>)}
          </select>
        </div>
        <div style={S.row}>
          <span style={S.label}>選擇課程</span>
          <select style={S.input} value={selectedCourse} onChange={e => setSelectedCourse(e.target.value)}>
            {courses.map(c => <option key={c.id} value={c.id}>{c.course_name}</option>)}
          </select>
        </div>
        {[['考試名稱','exam_name','例如：期中考','text'],['考試時間','exam_time','例如：13:00-15:00','text'],['考試地點','location','例如：A101','text']].map(([lbl,key,ph,type]) => (
          <div key={key} style={S.row}>
            <span style={S.label}>{lbl}</span>
            <input style={S.input} type={type} placeholder={ph} value={form[key]} onChange={e => set(key, e.target.value)} />
          </div>
        ))}
        <div style={S.row}>
          <span style={S.label}>考試日期</span>
          <input type="date" style={S.input} value={form.exam_date} onChange={e => set('exam_date', e.target.value)} />
        </div>
        {[['考試範圍','scope'],['注意事項','notes']].map(([lbl,key]) => (
          <div key={key} style={{ ...S.row, alignItems: 'flex-start' }}>
            <span style={{ ...S.label, paddingTop: 8 }}>{lbl}</span>
            <textarea style={{ ...S.input, height: 60, resize: 'vertical' }} value={form[key]} onChange={e => set(key, e.target.value)} />
          </div>
        ))}
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <button style={S.btn('#6366f1')} onClick={submit}><Save size={14} /> 儲存考試</button>
          {msg && <span style={{ fontSize: 15, color: msg === 'ok' ? '#10b981' : '#ef4444' }}>{msg === 'ok' ? '考試新增成功！' : msg}</span>}
        </div>
      </Card>

      <Card title="考試列表">
        {exams.length === 0 && <p style={{ color: '#94a3b8', fontSize: 15 }}>尚無考試資料</p>}
        {exams.map(ex => (
          <div key={ex.id} style={{ padding: '12px 14px', borderRadius: 10, background: '#f8fafc', marginBottom: 10, border: '1px solid #e2e8f0' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span style={{ fontWeight: 600, fontSize: 16 }}>{ex.exam_name}</span>
                <span style={{ padding: '2px 8px', borderRadius: 12, fontSize: 13, fontWeight: 600,
                  background: ex.status === '已考' ? '#d1fae5' : '#fee2e2',
                  color: ex.status === '已考' ? '#10b981' : '#ef4444' }}>{ex.status}</span>
                {ex.score > 0 && <span style={{ fontSize: 14, color: '#6366f1' }}>{ex.score} 分</span>}
              </div>
              <div style={{ display: 'flex', gap: 6 }}>
                <button style={S.btn('#6366f1')} onClick={() => { setEditing(ex.id); setEditForm({ status: ex.status, score: ex.score }) }}><Pencil size={13} /></button>
                <button style={S.btn('#ef4444')} onClick={() => deleteExam(ex.id).then(() => getExams(selectedCourse).then(setExams))}><Trash2 size={13} /></button>
              </div>
            </div>
            <div style={{ fontSize: 14, color: '#64748b', marginTop: 4 }}>
              {ex.exam_date}{ex.exam_time && ` · ${ex.exam_time}`}{ex.location && ` · ${ex.location}`}
            </div>
            {editing === ex.id && (
              <div style={{ marginTop: 10, padding: 12, background: '#fff', borderRadius: 8, border: '1px solid #e2e8f0', display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
                {['未考','已考'].map(s => (
                  <button key={s} onClick={() => setEditForm(f => ({ ...f, status: s }))} style={{
                    padding: '4px 14px', borderRadius: 16, border: '1.5px solid',
                    borderColor: editForm.status === s ? '#6366f1' : '#e2e8f0',
                    background: editForm.status === s ? '#6366f1' : '#fff',
                    color: editForm.status === s ? '#fff' : '#64748b', cursor: 'pointer', fontSize: 14,
                  }}>{s}</button>
                ))}
                <input type="number" placeholder="成績" style={{ width: 70, padding: '4px 8px', border: '1px solid #e2e8f0', borderRadius: 6, fontSize: 15 }}
                  value={editForm.score} onChange={e => setEditForm(f => ({ ...f, score: Number(e.target.value) }))} />
                <button style={S.btn('#10b981')} onClick={saveEdit}><Check size={13} /> 儲存</button>
                <button style={S.btn('#94a3b8')} onClick={() => setEditing(null)}><X size={13} /></button>
              </div>
            )}
          </div>
        ))}
      </Card>
    </div>
  )
}