import axios from 'axios'

const api = axios.create({ baseURL: 'http://localhost:8000' })

// ── 學期 ────────────────────────────────────────────────────────
export const getSemesters = () => api.get('/semesters/').then(r => r.data)
export const createSemester = (data) => api.post('/semesters/', data).then(r => r.data)
export const deleteSemester = (id) => api.delete(`/semesters/${id}`)

// ── 課程 ────────────────────────────────────────────────────────
export const getCourses = (semester_id) =>
  api.get('/courses/', { params: semester_id ? { semester_id } : {} }).then(r => r.data)
export const createCourse = (data) => api.post('/courses/', data).then(r => r.data)
export const deleteCourse = (id) => api.delete(`/courses/${id}`)

// ── 作業 ────────────────────────────────────────────────────────
export const getHomeworks = (course_id) =>
  api.get('/homeworks/', { params: course_id ? { course_id } : {} }).then(r => r.data)
export const getUrgentHomeworks = () => api.get('/homeworks/urgent').then(r => r.data)
export const createHomework = (data) => api.post('/homeworks/', data).then(r => r.data)
export const updateHomework = (id, data) => api.patch(`/homeworks/${id}`, data).then(r => r.data)
export const deleteHomework = (id) => api.delete(`/homeworks/${id}`)

// ── 考試 ────────────────────────────────────────────────────────
export const getExams = (course_id) =>
  api.get('/exams/', { params: course_id ? { course_id } : {} }).then(r => r.data)
export const getUpcomingExams = () => api.get('/exams/upcoming').then(r => r.data)
export const createExam = (data) => api.post('/exams/', data).then(r => r.data)
export const updateExam = (id, data) => api.patch(`/exams/${id}`, data).then(r => r.data)
export const deleteExam = (id) => api.delete(`/exams/${id}`)
