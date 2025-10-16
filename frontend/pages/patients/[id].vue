<template>
  <div v-if="patientStore.currentPatient" class="w-full max-w-2xl">
    <Card class="p-8">
      <h1 class="text-2xl font-bold mb-4">Patient Details</h1>
      <div v-if="patientName" class="mb-2">
        <strong>Name:</strong> {{ patientName }}
      </div>
      <div v-if="patientStore.currentPatient.gender" class="mb-2">
        <strong>Gender:</strong> {{ patientStore.currentPatient.gender }}
      </div>
      <div v-if="patientStore.currentPatient.birthDate" class="mb-2">
        <strong>Date of Birth:</strong> {{ patientStore.currentPatient.birthDate }}
      </div>
    </Card>
  </div>
  <div v-else>
    <p>Loading patient details...</p>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { usePatientStore } from '~/stores/patients'
import { computed, onMounted } from 'vue'
import Card from '~/components/Card.vue'

const route = useRoute()
const patientStore = usePatientStore()

// Fetch the patient data when the component is mounted
onMounted(() => {
  const patientId = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id;
  if (patientId) {
    patientStore.fetchPatientById(patientId)
  }
})

// Computed property to safely format the patient's name
const patientName = computed(() => {
  const name = patientStore.currentPatient?.name?.[0]
  if (!name) return 'N/A'
  return `${name.given.join(' ')} ${name.family}`
})
</script>