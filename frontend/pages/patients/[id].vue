<template>
  <div class="w-full max-w-4xl mx-auto">
    <Card v-if="patientStore.currentPatient" class="p-8 mb-8">
      <h1 class="text-2xl font-bold mb-4">Patient Details</h1>
      <div class="grid grid-cols-2 gap-4">
        <div v-if="patientName" class="mb-2">
          <strong>Name:</strong> {{ patientName }}
        </div>
        <div v-if="patientStore.currentPatient.gender" class="mb-2">
          <strong>Gender:</strong> {{ patientStore.currentPatient.gender }}
        </div>
        <div v-if="patientStore.currentPatient.birthDate" class="mb-2">
          <strong>Date of Birth:</strong> {{ patientStore.currentPatient.birthDate }}
        </div>
      </div>
    </Card>
    <div v-else class="text-center">
      <p>Loading patient details...</p>
    </div>

    <Card class="p-8">
      <h2 class="text-xl font-bold mb-4">Clinical Notes</h2>

      <form @submit.prevent="handleCreateNote" class="mb-6">
        <textarea
          v-model="newNoteContent"
          class="form-input"
          rows="4"
          placeholder="Enter new clinical note..."
          required
        ></textarea>
        <button type="submit" class="btn-primary mt-2 !w-auto">
          Add Note
        </button>
      </form>

      <ul v-if="noteStore.notes.length > 0" class="space-y-4">
        <li v-for="note in noteStore.notes" :key="note.id">
          <div class="p-4 bg-primary dark:bg-dark-primary rounded-lg">
            <p class="text-text dark:text-dark-text">{{ note.content }}</p>
          </div>
        </li>
      </ul>
      <p v-else class="text-soft dark:text-dark-soft">No clinical notes found for this patient.</p>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { usePatientStore } from '~/stores/patients'
import { useNoteStore } from '~/stores/notes' // <-- Import the new store
import { computed, onMounted, ref } from 'vue'
import Card from '~/components/Card.vue'

const route = useRoute()
const patientStore = usePatientStore()
const noteStore = useNoteStore() // <-- Use the new store

const newNoteContent = ref('')

const patientId = computed(() => Array.isArray(route.params.id) ? route.params.id[0] : route.params.id)

// Fetch both patient and note data when the component is mounted
onMounted(() => {
  if (patientId.value) {
    patientStore.fetchPatientById(patientId.value)
    noteStore.fetchNotesByPatientId(patientId.value) // <-- Fetch notes
  }
})

const patientName = computed(() => {
  const name = patientStore.currentPatient?.name?.[0]
  if (!name) return 'N/A'
  return `${name.given.join(' ')} ${name.family}`
})

const handleCreateNote = async () => {
  if (!patientId.value || !newNoteContent.value.trim()) return

  const success = await noteStore.createNote(parseInt(patientId.value), newNoteContent.value)
  if (success) {
    newNoteContent.value = '' // Clear the textarea on success
  } else {
    alert('Failed to create note.')
  }
}
</script>