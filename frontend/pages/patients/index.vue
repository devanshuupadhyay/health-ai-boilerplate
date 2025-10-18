<template>
  <div class="p-4 md:p-8 w-full max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Patient Dashboard</h1>

    <div class="mb-8 p-6 md:p-8 bg-secondary dark:bg-dark-secondary rounded-lg shadow"> 
      <h2 class="text-2xl font-semibold mb-4">Search Notes</h2>
      <NoteSearch />
    </div>

    <div> 
       <h2 class="text-2xl font-semibold mb-4">Patients</h2>
       <div v-if="isLoading" class="text-center text-soft dark:text-dark-soft"> 
         Loading patients...
       </div>
       <ul v-else-if="patientStore.patients.length > 0" class="space-y-4">
         <li v-for="patient in patientStore.patients" :key="patient.id">
           <NuxtLink :to="`/patients/${patient.id}`">
             <Card class="p-4 hover:bg-primary dark:hover:bg-dark-primary transition-colors duration-200 cursor-pointer"> 
               <div class="font-semibold">{{ formatPatientName(patient.fhir_resource) }}</div>
               <div class="text-sm text-soft dark:text-dark-soft">
                 DOB: {{ patient.fhir_resource?.birthDate || 'N/A' }} | Gender: {{ patient.fhir_resource?.gender || 'N/A' }} 
               </div>
             </Card>
           </NuxtLink>
         </li>
       </ul>
       <div v-else class="text-center text-soft dark:text-dark-soft"> 
         <p>No patients found. Create one via the API docs to see them listed here.</p>
       </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { usePatientStore } from '~/stores/patients'
import { onMounted, ref } from 'vue' // Added ref
import Card from '~/components/Card.vue'
import NoteSearch from '~/components/NoteSearch.vue'; // Import search component
import type { PatientFHIR } from '~/types/patient'

definePageMeta({
  middleware: ['auth']
})

const patientStore = usePatientStore()
const isLoading = ref(true); // Added loading state ref

onMounted(async () => { // Make async
  isLoading.value = true;
  try {
      await patientStore.fetchPatients();
  } catch (error) {
      console.error("Failed to fetch patients:", error);
      // Optionally show an error message to the user
  } finally {
      isLoading.value = false;
  }
})

// Safer name formatting function
const formatPatientName = (patientResource: PatientFHIR | null | undefined) => {
  const name = patientResource?.name?.[0]
  if (!name) return 'Unknown Patient'
  const givenName = Array.isArray(name.given) ? name.given.join(' ') : '';
  return `${givenName} ${name.family || ''}`.trim() || 'Unnamed Patient'; // Fallback added
}
</script>

<style scoped>
/* Add any page-specific styles if needed */
</style>