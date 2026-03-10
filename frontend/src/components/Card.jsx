export default function Card({ title, children, style }) {
  return (
    <div style={{
      background: '#fff', borderRadius: 12, padding: 20,
      marginBottom: 20, boxShadow: '0 1px 3px rgba(0,0,0,0.08)',
      ...style
    }}>
      {title && (
        <>
          <div style={{ fontWeight: 700, fontSize: 15, color: '#6366f1', marginBottom: 12 }}>
            {title}
          </div>
          <div style={{ height: 1, background: '#e2e8f0', marginBottom: 16 }} />
        </>
      )}
      {children}
    </div>
  )
}