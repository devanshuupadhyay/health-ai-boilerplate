<template>
  <div class="p-8 w-full max-w-4xl">
    <h1 class="text-3xl font-bold mb-6">Patient Dashboard</h1>

    <div v-if="patientStore.patients.length > 0">
      <ul class="space-y-4">
        <li v-for="patient in patientStore.patients" :key="patient.id">
          <NuxtLink :to="`/patients/${patient.id}`">
            <Card class="p-4 hover:bg-secondary-focus transition-colors duration-200 cursor-pointer">
              <div class="font-semibold">{{ formatPatientName(patient.fhir_resource) }}</div>
              <div class="text-sm text-soft dark:text-dark-soft">
                DOB: {{ patient.fhir_resource.birthDate || 'N/A' }} | Gender: {{ patient.fhir_resource.gender || 'N/A' }}
              </div>
            </Card>
          </NuxtLink>
        </li>
      </ul>
    </div>

    <div v-else>
      <p>No patients found. Create one via the API docs to see them listed here.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { usePatientStore } from '~/stores/patients'
import { onMounted } from 'vue'
import Card from '~/components/Card.vue'
// Import the FHIR type
import type { PatientFHIR } from '~/types/patient'

definePageMeta({
  middleware: ['auth']
})

const patientStore = usePatientStore()

onMounted(() => {
  patientStore.fetchPatients()
})

// The function now expects the fhir_resource part of the patient object
const formatPatientName = (patient: PatientFHIR) => {
  const name = patient?.name?.[0]
  if (!name) return 'Unknown Patient'
  return `${name.given.join(' ')} ${name.family}`
}
</script>