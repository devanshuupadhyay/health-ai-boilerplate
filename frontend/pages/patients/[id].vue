<template>
  <div class="w-full max-w-4xl mx-auto p-4 md:p-8">

    <Card v-if="patientStore.currentPatient" class="p-6 md:p-8 mb-8">
      <h1 class="text-2xl font-bold mb-4">Patient Details</h1>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
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
     <div v-else-if="isLoadingPatient" class="text-center p-8">
       <p class="text-soft dark:text-dark-soft">Loading patient details...</p>
     </div>
     <div v-else class="text-center p-8 form-error-message">
       <p>Could not load patient details.</p>
     </div>

    <Card class="p-6 md:p-8">
      <h2 class="text-xl font-bold mb-4">Clinical Notes</h2>

      <form @submit.prevent="handleCreateNote" class="mb-6">
        <label for="newNote" class="form-label sr-only">New Clinical Note</label>
        <textarea
          id="newNote"
          v-model="newNoteContent"
          v-bind="newNoteAttrs"
          class="form-input" :class="{ 'invalid': noteErrors.newNoteContent }" rows="4"
          placeholder="Enter new clinical note..."
          :disabled="isSubmittingNote"
        ></textarea>
        <p v-if="noteErrors.newNoteContent" class="form-error-message"> {{ noteErrors.newNoteContent }}
        </p>
        <button type="submit" class="btn-primary mt-2 !w-auto" :disabled="isSubmittingNote"> {{ isSubmittingNote ? 'Adding...' : 'Add Note' }}
        </button>
      </form>

      <div v-if="isLoadingNotes" class="text-center">
        <p class="text-soft dark:text-dark-soft">Loading notes...</p>
      </div>
      <ul v-else-if="noteStore.notes.length > 0" class="space-y-4">
        <li v-for="note in noteStore.notes" :key="note.id">
           <div class="p-4 bg-primary dark:bg-dark-primary rounded-lg shadow">
            <p class="text-text dark:text-dark-text mb-2 whitespace-pre-wrap">{{ note.content }}</p>

            <div v-if="note.summary" class="mt-2 pt-2 border-t border-soft/50 dark:border-dark-soft/50">
                <p class="text-sm text-soft dark:text-dark-soft italic">
                    <strong>AI Summary:</strong> {{ note.summary }}
                </p>
            </div>
            <div v-else class="mt-2 pt-2 border-t border-soft/50 dark:border-dark-soft/50">
                <p class="text-sm text-soft dark:text-dark-soft italic">
                    Summary is being generated...
                </p>
            </div>
          </div>
        </li>
      </ul>
      <p v-else class="text-soft dark:text-dark-soft">No clinical notes found for this patient.</p>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import { usePatientStore } from '~/stores/patients';
import { useNoteStore } from '~/stores/notes';
import { computed, onMounted, ref, onUnmounted } from 'vue'; // <-- Import onUnmounted
import Card from '~/components/Card.vue';
import { useForm } from 'vee-validate';
import * as zod from 'zod';
import { toTypedSchema } from '@vee-validate/zod';

definePageMeta({
  middleware: ['auth']
});

const route = useRoute();
const patientStore = usePatientStore();
const noteStore = useNoteStore();

const isLoadingPatient = ref(true);
const isLoadingNotes = ref(true);
const isSubmittingNote = ref(false);
const pollingIntervalId = ref<NodeJS.Timeout | null>(null); // <-- Ref to store interval ID

const patientId = computed(() => {
  const idParam = route.params.id;
  return Array.isArray(idParam) ? idParam[0] : idParam;
});

const noteValidationSchema = toTypedSchema(
  zod.object({
    newNoteContent: zod.string()
      .trim()
      .min(1, 'Note content cannot be empty')
      .max(5000, 'Note cannot exceed 5000 characters')
  })
);

const { handleSubmit: handleNoteSubmit, errors: noteErrors, defineField: defineNoteField, resetForm: resetNoteForm } = useForm({
  validationSchema: noteValidationSchema,
});

const [newNoteContent, newNoteAttrs] = defineNoteField('newNoteContent');

onMounted(async () => {
    const currentPatientId = patientId.value;
    if (currentPatientId) {
        isLoadingPatient.value = true;
        isLoadingNotes.value = true;
        try {
            await Promise.all([
                patientStore.fetchPatientById(currentPatientId),
                noteStore.fetchNotesByPatientId(currentPatientId)
            ]);
        } catch (error) {
            console.error("Error fetching patient details or notes:", error);
        } finally {
            isLoadingPatient.value = false;
            isLoadingNotes.value = false;
        }
    } else {
        isLoadingPatient.value = false;
        isLoadingNotes.value = false;
        console.error("Patient ID is missing from the route.");
    }
});

// --- Lifecycle hook to clear interval when component is unmounted ---
onUnmounted(() => {
    if (pollingIntervalId.value) {
        clearInterval(pollingIntervalId.value);
        console.log("Polling stopped on component unmount.");
    }
});
// --- End lifecycle hook ---

const patientName = computed(() => {
    const patient = patientStore.currentPatient
    const name = patient?.name?.[0]
    if (!name) return 'N/A'
    const givenName = Array.isArray(name.given) ? name.given.join(' ') : ''
    return `${givenName} ${name.family || ''}`.trim() || 'Unnamed Patient'
});

const handleCreateNote = handleNoteSubmit(async (values) => {
    const currentPatientId = patientId.value;
    if (!currentPatientId) {
        alert('Patient ID is missing.');
        return;
    }
    isSubmittingNote.value = true;
    try {
        const numericPatientId = parseInt(currentPatientId, 10);
        if (isNaN(numericPatientId)) {
            alert('Invalid Patient ID.');
            return;
        }
        // --- Call createNote ---
        const success = await noteStore.createNote(numericPatientId, values.newNoteContent);

        if (success) {
            resetNoteForm();
            // Fetch notes immediately to show the new note without summary
            await noteStore.fetchNotesByPatientId(currentPatientId);

            // --- Find the new note ID (assuming it's the latest/first) ---
            // Ensure notes array is sorted descending by ID in the store if necessary
            const newNote = noteStore.notes.length > 0 ? noteStore.notes[0] : null;
            const newNoteId = newNote?.id;

            // --- Start Polling for the summary of the new note ---
            if (newNoteId) {
                pollForSummary(currentPatientId, newNoteId);
            } else {
                console.warn("Could not determine new note ID to start polling.");
            }
            // --- End Polling Start ---

        } else {
            alert('Failed to save the note. Please try again.');
        }
    } catch (error) {
        console.error("Error creating note:", error);
        alert('An error occurred while saving the note.');
    } finally {
        isSubmittingNote.value = false;
    }
});

// --- Polling Function ---

const pollForSummary = (patientIdValue: string, noteIdToCheck: number, interval = 2500, maxAttempts = 30) => { // <-- CHANGED DEFAULTS
    let attempts = 0;

    // Clear any existing interval before starting a new one
    if (pollingIntervalId.value) {
        clearInterval(pollingIntervalId.value);
    }

    pollingIntervalId.value = setInterval(async () => {
        attempts++;
        console.log(`Polling for summary (Note ID: ${noteIdToCheck}) - Attempt ${attempts}...`);

        // Fetch notes without setting loading state to avoid UI flicker
        await noteStore.fetchNotesByPatientId(patientIdValue);

        const targetNote = noteStore.notes.find(note => note.id === noteIdToCheck);

        // Check if summary exists or max attempts reached
        if (targetNote?.summary || attempts >= maxAttempts) {
            if (pollingIntervalId.value) {
                clearInterval(pollingIntervalId.value);
                pollingIntervalId.value = null; // Clear the ref
            }
            if (!targetNote?.summary && attempts >= maxAttempts) {
                console.warn(`Polling stopped after ${attempts} attempts (max ${maxAttempts}), summary not found for note ${noteIdToCheck}.`);
            } else {
                 console.log(`Summary found for note ${noteIdToCheck}! Polling stopped.`);
            }
        }
    }, interval); // Use the interval parameter here
};
// --- End Polling Function ---

</script>

<style scoped>
.whitespace-pre-wrap {
  white-space: pre-wrap;
}
</style>