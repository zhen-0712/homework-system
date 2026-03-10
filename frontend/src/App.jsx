import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Semesters from './pages/Semesters'
import Courses   from './pages/Courses'
import Homeworks from './pages/Homeworks'
import Search    from './pages/Search'
import Urgent    from './pages/Urgent'
import Exams     from './pages/Exams'
import Alerts    from './pages/Alerts'

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ display: 'flex', minHeight: '100vh', fontFamily: 'system-ui, sans-serif' }}>
        <Sidebar />
        <main style={{ flex: 1, background: '#f4f6fb', padding: '32px 40px', overflowY: 'auto', minWidth: 0 }}>
          <Routes>
            <Route path="/" element={<Navigate to="/semesters" replace />} />
            <Route path="/semesters" element={<Semesters />} />
            <Route path="/courses"   element={<Courses />} />
            <Route path="/homeworks" element={<Homeworks />} />
            <Route path="/search"    element={<Search />} />
            <Route path="/urgent"    element={<Urgent />} />
            <Route path="/exams"     element={<Exams />} />
            <Route path="/alerts"    element={<Alerts />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}