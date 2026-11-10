/**
 * Modul Keamanan Informasi (Konsep 5A: Authentication, Authorization, Accounting, Auditing, Availability/Assurance)
 * Sistem: Luxury Store E-Commerce
 */

// Key penyimpanan localStorage
const AUDIT_LOG_KEY = 'luxury_audit_logs'
const LOGIN_ATTEMPTS_KEY = 'luxury_login_attempts'
const MAX_ATTEMPTS = 3
const LOCKOUT_DURATION_MS = 60 * 1000 // 60 detik lockout

// Inisialisasi log awal jika kosong (seeding sample logs)
export const initAuditLogs = () => {
  const existing = localStorage.getItem(AUDIT_LOG_KEY)
  if (!existing) {
    const initialLogs = [
      {
        id: 'LOG-' + (Date.now() - 3600000),
        timestamp: new Date(Date.now() - 3600000).toLocaleString('id-ID'),
        actor: 'system',
        role: 'system',
        category: 'System',
        action: 'SYSTEM_BOOT',
        details: 'Inisialisasi sistem Luxury Store dan modul keamanan 5A',
        severity: 'INFO',
        status: 'SUCCESS',
        ip_hint: '127.0.0.1 (Localhost / Client Web)'
      },
      {
        id: 'LOG-' + (Date.now() - 1800000),
        timestamp: new Date(Date.now() - 1800000).toLocaleString('id-ID'),
        actor: 'admin',
        role: 'admin',
        category: 'Authentication',
        action: 'AUTH_LOGIN_SUCCESS',
        details: 'Login Administrator berhasil melalui verifikasi kredensial',
        severity: 'SUCCESS',
        status: 'SUCCESS',
        ip_hint: '192.168.1.10 (Admin Console)'
      }
    ]
    localStorage.setItem(AUDIT_LOG_KEY, JSON.stringify(initialLogs))
  }
}

// -------------------------------------------------------------
// 1. ACCOUNTING & AUDITING: Perekaman Jejak Aktivitas (Audit Logger)
// -------------------------------------------------------------
export const logSecurityEvent = ({
  action,
  details,
  category = 'General',
  severity = 'INFO', // INFO, WARNING, DANGER, SUCCESS
  status = 'SUCCESS',
  actor = null,
  role = null
}) => {
  try {
    initAuditLogs()
    const logs = JSON.parse(localStorage.getItem(AUDIT_LOG_KEY) || '[]')
    
    // Tentukan actor jika tidak disediakan
    const currentActor = actor || (localStorage.getItem('token') ? 'admin' : 'guest')
    const currentRole = role || (localStorage.getItem('token') ? 'Administrator' : 'Public')

    const newLog = {
      id: 'LOG-' + Date.now() + '-' + Math.floor(Math.random() * 1000),
      timestamp: new Date().toLocaleString('id-ID'),
      actor: currentActor,
      role: currentRole,
      category,
      action,
      details,
      severity,
      status,
      ip_hint: navigator.userAgent.substring(0, 45) + '...'
    }

    // Simpan maksimal 200 log terbaru (FIFO)
    logs.unshift(newLog)
    if (logs.length > 200) {
      logs.pop()
    }

    localStorage.setItem(AUDIT_LOG_KEY, JSON.stringify(logs))
    return newLog
  } catch (err) {
    console.error('Audit Logger Error:', err)
  }
}

export const getAuditLogs = () => {
  initAuditLogs()
  try {
    return JSON.parse(localStorage.getItem(AUDIT_LOG_KEY) || '[]')
  } catch {
    return []
  }
}

export const clearAuditLogs = () => {
  const resetLogs = [
    {
      id: 'LOG-' + Date.now(),
      timestamp: new Date().toLocaleString('id-ID'),
      actor: 'admin',
      role: 'Administrator',
      category: 'Auditing',
      action: 'AUDIT_LOGS_PURGED',
      details: 'Audit logs telah direset oleh Administrator berwenang',
      severity: 'WARNING',
      status: 'SUCCESS',
      ip_hint: navigator.userAgent.substring(0, 45) + '...'
    }
  ]
  localStorage.setItem(AUDIT_LOG_KEY, JSON.stringify(resetLogs))
}

// -------------------------------------------------------------
// 2. AUTHENTICATION: Proteksi Serangan Brute-Force
// -------------------------------------------------------------
export const checkBruteForceLockout = () => {
  const data = JSON.parse(localStorage.getItem(LOGIN_ATTEMPTS_KEY) || '{"count": 0, "lockedUntil": 0}')
  const now = Date.now()

  if (data.lockedUntil && now < data.lockedUntil) {
    const remainingSeconds = Math.ceil((data.lockedUntil - now) / 1000)
    return {
      isLocked: true,
      remainingSeconds,
      attempts: data.count
    }
  }

  // Jika lockout sudah lewat, reset
  if (data.lockedUntil && now >= data.lockedUntil) {
    localStorage.removeItem(LOGIN_ATTEMPTS_KEY)
    return { isLocked: false, remainingSeconds: 0, attempts: 0 }
  }

  return {
    isLocked: false,
    remainingSeconds: 0,
    attempts: data.count || 0
  }
}

export const recordFailedLoginAttempt = (username) => {
  const current = checkBruteForceLockout()
  const newCount = current.attempts + 1
  const now = Date.now()

  if (newCount >= MAX_ATTEMPTS) {
    const lockedUntil = now + LOCKOUT_DURATION_MS
    localStorage.setItem(LOGIN_ATTEMPTS_KEY, JSON.stringify({ count: newCount, lockedUntil }))
    
    // Log Security Alert
    logSecurityEvent({
      action: 'AUTH_BRUTE_FORCE_LOCKOUT',
      category: 'Authentication',
      severity: 'DANGER',
      status: 'LOCKED',
      actor: username || 'Unknown',
      details: `Percobaan login gagal mencapai batas maksimum (${MAX_ATTEMPTS}x). Akses dikunci sementara selama 60 detik.`
    })

    return {
      isLocked: true,
      remainingSeconds: 60,
      attempts: newCount
    }
  }

  localStorage.setItem(LOGIN_ATTEMPTS_KEY, JSON.stringify({ count: newCount, lockedUntil: 0 }))
  
  logSecurityEvent({
    action: 'AUTH_LOGIN_FAILED',
    category: 'Authentication',
    severity: 'WARNING',
    status: 'FAILED',
    actor: username || 'Unknown',
    details: `Percobaan login gagal (${newCount}/${MAX_ATTEMPTS}). Kredensial tidak valid.`
  })

  return {
    isLocked: false,
    remainingSeconds: 0,
    attempts: newCount
  }
}

export const recordSuccessfulLogin = (username) => {
  // Reset failed attempts
  localStorage.removeItem(LOGIN_ATTEMPTS_KEY)
  
  logSecurityEvent({
    action: 'AUTH_LOGIN_SUCCESS',
    category: 'Authentication',
    severity: 'SUCCESS',
    status: 'SUCCESS',
    actor: username,
    details: `Autentikasi akun ${username} berhasil. Sesi token diterbitkan.`
  })
}

// -------------------------------------------------------------
// 3. AVAILABILITY & ASSURANCE: Sanitasi Input (Cegah XSS)
// -------------------------------------------------------------
export const sanitizeInput = (input) => {
  if (typeof input !== 'string') return input
  return input
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;')
}

// -------------------------------------------------------------
// 4. EXPORT AUDIT LOG (Untuk Keperluan Compliance & Wawancara)
// -------------------------------------------------------------
export const exportAuditLogsToCSV = () => {
  const logs = getAuditLogs()
  if (!logs.length) return

  const headers = ['ID Log', 'Waktu', 'Aktor', 'Peran', 'Kategori', 'Aksi', 'Status', 'Tingkat Bahaya', 'Keterangan']
  const rows = logs.map(l => [
    `"${l.id}"`,
    `"${l.timestamp}"`,
    `"${l.actor}"`,
    `"${l.role}"`,
    `"${l.category}"`,
    `"${l.action}"`,
    `"${l.status}"`,
    `"${l.severity}"`,
    `"${(l.details || '').replace(/"/g, '""')}"`
  ])

  const csvContent = 'data:text/csv;charset=utf-8,\uFEFF' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n')
  const encodedUri = encodeURI(csvContent)
  const link = document.createElement('a')
  link.setAttribute('href', encodedUri)
  link.setAttribute('download', `audit_trail_luxury_store_${Date.now()}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)

  logSecurityEvent({
    action: 'AUDIT_EXPORT_CSV',
    category: 'Auditing',
    severity: 'INFO',
    details: 'Administrator mengekspor rekaman Audit Trail ke format CSV'
  })
}
