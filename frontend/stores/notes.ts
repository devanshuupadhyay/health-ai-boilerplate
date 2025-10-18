// frontend/stores/notes.ts
import { defineStore } from 'pinia'
import type { Note } from '~/types/note'

export const useNoteStore = defineStore('notes', {
  state: () => ({
    notes: [] as Note[],
  }),
  actions: {
    async fetchNotesByPatientId(patientId: string) {
      if (!patientId) return
      try {
        const response = await fetch(`/api/v1/notes/patient/${patientId}`)
        if (response.ok) {
          this.notes = await response.json()
        } else {
          console.error('Failed to fetch notes')
          this.notes = []
        }
      } catch (error) {
        console.error('API call to fetch notes failed:', error)
        this.notes = []
      }
    },
    async createNote(patientId: number, content: string) {
      try {
        const response = await fetch('/api/v1/notes/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ patient_id: patientId, content }),
        })
        if (response.ok) {
          const newNote = await response.json()
          this.notes.push(newNote) // Add the new note to the list
          return true
        }
        return false
      } catch (error) {
        console.error('API call to create note failed:', error)
        return false
      }
    },
  },
})