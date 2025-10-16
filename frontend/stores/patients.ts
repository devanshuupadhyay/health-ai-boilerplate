// frontend/stores/patients.ts
import { defineStore } from 'pinia'
// Import our new type
import type { PatientAPIResponse } from '~/types/patient'

export const usePatientStore = defineStore('patients', {
  state: () => ({
    // The state now holds the full API response object
    patients: [] as PatientAPIResponse[],
    currentPatient: null as PatientAPIResponse['fhir_resource'] | null,
  }),
  actions: {
    async fetchPatients() {
      try {
        const response = await fetch('/api/v1/patients/')
        if (response.ok) {
          const data = await response.json()
          this.patients = data
        } else {
          console.error('Failed to fetch patients:', await response.json())
        }
      } catch (error) {
        console.error('API call to fetch patients failed:', error)
      }
    },
    async fetchPatientById(id: string) {
      try {
        const response = await fetch(`/api/v1/patients/${id}`)
        if (response.ok) {
          // The API returns the fhir_resource directly for a single patient
          this.currentPatient = await response.json()
          return this.currentPatient
        } else {
          console.error('Failed to fetch patient:', await response.json())
          return null
        }
      } catch (error) {
        console.error('API call to fetch patient failed:', error)
        return null
      }
    },
  },
})