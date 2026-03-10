export default function PageHeader({ title, subtitle }) {
  return (
    <div style={{ marginBottom: 24 }}>
      <h1 style={{ fontSize: 26, fontWeight: 700, color: '#0f172a', margin: 0 }}>{title}</h1>
      {subtitle && <p style={{ color: '#64748b', fontSize: 15, marginTop: 4 }}>{subtitle}</p>}
    </div>
  )
}