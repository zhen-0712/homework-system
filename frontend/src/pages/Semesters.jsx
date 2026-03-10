import { useState, useEffect } from 'react'
import { Plus, Trash2 } from 'lucide-react'
import { getSemesters, createSemester, deleteSemester } from '../api'
import Card from '../components/Card'
import PageHeader from '../components/PageHeader'

const S = {
  row:   { display: 'flex', gap: 12, alignItems: 'center', marginBottom: 12 },
  label: { width: 80, fontSize: 15, color: '#64748b', flexShrink: 0 },
  input: { flex: 1, padding: '9px 12px', border: '1px solid #e2e8f0', borderRadius: 8, fontSize: 15, background: '#fff' },
  btn:   (c) => ({ display: 'flex', alignItems: 'center', gap: 6, padding: '10px 20px', background: c, color: '#fff', border: 'none', borderRadius: 8, cursor: 'pointer', fontWeight: 600, fontSize: 15 }),
  item:  { display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 14px', borderRadius: 8, background: '#f8fafc', marginBottom: 8, fontSize: 15, color: '#334155' },
}

export default function Semesters() {
  const [list, setList] = useState([])
  const [form, setForm] = useState({ year: '', grade: '大一', semester: '上學期', start_date: '', end_date: '' })
  const [msg, setMsg] = useState('')

  const load = () => getSemesters().then(setList)
  useEffect(() => { load() }, [])
  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const submit = async () => {
    if (!form.year || !form.start_date || !form.end_date) { setMsg('請填寫所有欄位'); return }
    try {
      await createSemester(form)
      setMsg('ok')
      setForm({ year: '', grade: '大一', semester: '上學期', start_date: '', end_date: '' })
      load()
    } catch (e) { setMsg(e.response?.data?.detail || '新增失敗') }
  }

  return (
    <div>
      <PageHeader title="學期管理" subtitle="管理你的學年度與學期資訊" />
      <Card title="新增學期">
        {[['學年度','year','text','例如：2024'],['開始日期','start_date','text','2024-09-01'],['結束日期','end_date','text','2025-01-31']].map(([lbl,key,type,ph]) => (
          <div key={key} style={S.row}>
            <span style={S.label}>{lbl}</span>
            <input style={S.input} type={type} placeholder={ph} value={form[key]} onChange={e => set(key, e.target.value)} />
          </div>
        ))}
        <div style={S.row}>
          <span style={S.label}>年級</span>
          <select style={S.input} value={form.grade} onChange={e => set('grade', e.target.value)}>
            {['大一','大二','大三','大四'].map(g => <option key={g}>{g}</option>)}
          </select>
        </div>
        <div style={S.row}>
          <span style={S.label}>學期</span>
          <select style={S.input} value={form.semester} onChange={e => set('semester', e.target.value)}>
            {['上學期','下學期'].map(s => <option key={s}>{s}</option>)}
          </select>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginTop: 4 }}>
          <button style={S.btn('#10b981')} onClick={submit}><Plus size={15} /> 新增學期</button>
          {msg && <span style={{ fontSize: 15, color: msg === 'ok' ? '#10b981' : '#ef4444' }}>{msg === 'ok' ? '新增成功！' : msg}</span>}
        </div>
      </Card>

      <Card title="學期列表">
        {list.length === 0 && <p style={{ color: '#94a3b8', fontSize: 15 }}>尚無學期資料</p>}
        {list.map(s => (
          <div key={s.id} style={S.item}>
            <span>{s.year} 學年 {s.grade}{s.semester}（{s.start_date} ~ {s.end_date}）</span>
            <button onClick={() => deleteSemester(s.id).then(load)}
              style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 4, fontSize: 15 }}>
              <Trash2 size={14} /> 刪除
            </button>
          </div>
        ))}
      </Card>
    </div>
  )
}