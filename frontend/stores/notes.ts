// frontend/stores/notes.ts
import { defineStore } from 'pinia'
import type { Note } from '~/types/note'

export const useNoteStore = defineStore('notes', {
  state: () => ({
    notes: [] as Note[],
  }),
  actions: {
    async fetchNotesByPatientId(patientId: string) {
      if (!patientId) {
          console.warn("fetchNotesByPatientId called with no patientId");
          this.notes = []; // Clear notes if ID is invalid
          return;
      };
      try {
        const response = await fetch(`/api/v1/notes/patient/${patientId}`, {
          cache: 'no-store' // Tells the browser not to use cached data for this request
        });

        if (response.ok) {
          this.notes = await response.json();
          console.log("Fetched notes:", this.notes); // Log fetched data for debugging
        } else {
          console.error('Failed to fetch notes, status:', response.status);
          this.notes = []; // Clear notes on failure
        }
      } catch (error) {
        console.error('API call to fetch notes failed:', error);
        this.notes = []; // Clear notes on error
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