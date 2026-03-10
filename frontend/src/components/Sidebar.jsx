import { NavLink } from 'react-router-dom'
import { CalendarDays, BookOpen, PenLine, Search, Zap, ClipboardList, Bell } from 'lucide-react'

const nav = [
  { to: '/semesters', Icon: CalendarDays,  label: '學期管理' },
  { to: '/courses',   Icon: BookOpen,      label: '課程管理' },
  { to: '/homeworks', Icon: PenLine,       label: '新增作業' },
  { to: '/search',    Icon: Search,        label: '作業查詢' },
  { to: '/urgent',    Icon: Zap,           label: '本週待辦' },
  { to: '/exams',     Icon: ClipboardList, label: '考試管理' },
  { to: '/alerts',    Icon: Bell,          label: '考試提醒' },
]

export default function Sidebar() {
  return (
    <aside style={{
      width: 200, minHeight: '100vh', background: '#0f172a',
      display: 'flex', flexDirection: 'column', flexShrink: 0,
    }}>
      <div style={{ padding: '20px 16px 12px', color: '#fff', fontSize: 17, fontWeight: 700, display: 'flex', alignItems: 'center', gap: 8 }}>
        <BookOpen size={18} color="#6366f1" />
        課程助理
      </div>
      <div style={{ height: 1, background: '#1e293b', margin: '0 12px 8px' }} />
      <nav style={{ flex: 1 }}>
        {nav.map((item) => (
          <NavLink key={item.to} to={item.to} style={({ isActive }) => ({
            display: 'flex', alignItems: 'center', gap: 10,
            padding: '11px 20px', textDecoration: 'none', fontSize: 15,
            color: isActive ? '#fff' : '#94a3b8',
            background: isActive ? '#6366f1' : 'transparent',
            borderLeft: isActive ? '3px solid #fff' : '3px solid transparent',
          })}>
            <item.Icon size={15} />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <div style={{ padding: 12, fontSize: 13, color: '#334155' }}>v2.0 網頁版</div>
    </aside>
  )
}