<template>
  <div class="w-full max-w-sm">
    <Card class="p-8">
      <form @submit.prevent="handleLogin" class="mb-6">
        <div class="mb-2">
          <label for="email" class="form-label">Email</label>
          <input
            v-model="email"
            v-bind="emailAttrs"
            @input="clearLoginError"
            type="email"
            id="email"
            name="email"
            class="form-input"
            :class="{ invalid: errors.email }"
          />
          <p v-if="errors.email" class="form-error-message">
            {{ errors.email }}
          </p>
        </div>
        <div class="mb-4">
          <label for="password" class="form-label">Password</label>
          <input
            v-model="password"
            v-bind="passwordAttrs"
            @input="clearLoginError"
            type="password"
            id="password"
            name="password"
            class="form-input"
            :class="{ invalid: errors.password }"
          />
          <p v-if="errors.password" class="form-error-message">
            {{ errors.password }}
          </p>
        </div>

        <p v-if="loginError" class="form-error-message mb-4 text-center">
          {{ loginError }}
        </p>

        <div class="mb-4">
          <button type="submit" class="btn-primary" :disabled="isLoggingIn">
            {{ isLoggingIn ? "Signing In..." : "Sign In" }}
          </button>
        </div>
      </form>

      <hr class="my-2 border-soft dark:border-dark-soft" />

      <div>
        <p class="mb-2 text-xs text-left text-soft dark:text-dark-soft px-2">
          Credentials for demo user: 
          <div>Username: <strong>test@example.com</strong></div>
          <div>Password: <strong>password123</strong></div>
        </p>
        <button
          @click="handleSeedData"
          class="w-full bg-secondary dark:bg-dark-secondary hover:bg-opacity-80 text-soft dark:text-dark-soft border border-soft dark:border-dark-soft text-sm m-2 py-2 px-4 rounded focus:outline-none transition-colors duration-200"
          :disabled="isSeeding"
        >
          <span v-if="isSeeding" class="flex items-center justify-center">
            <svg
              class="animate-spin h-5 w-5 mr-3 text-accent dark:text-dark-accent"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Bootstrapping...
          </span>
          <span v-else> Bootstrap FHIR Environment </span>
        </button>
        <p class="mt-2 text-xs text-center text-soft dark:text-dark-soft px-2">
          Clicking this button will <strong>delete</strong> all existing data (users,
          patients, notes) and create a fresh set of demo data.
        </p>
        <p
          v-if="seedMessage"
          class="mt-2 text-xs text-center"
          :class="
            seedError
              ? 'text-red-500 dark:text-red-400'
              : 'text-green-600 dark:text-green-400'
          "
        >
          {{ seedMessage }}
        </p>
        <div
          v-if="seedSummary"
          class="mt-2 text-xs text-center text-soft dark:text-dark-soft"
        >
          <p>Created:</p>
          <ul class="list-disc list-inside ml-4 text-left">
            <li>Users: {{ seedSummary.users }}</li>
            <li>Patients: {{ seedSummary.patients }}</li>
            <li>Notes: {{ seedSummary.notes }}</li>
          </ul>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "#imports";
import { toTypedSchema } from "@vee-validate/zod";
import { useForm } from "vee-validate";
import { ref } from "vue";
import * as zod from "zod";
import Card from "~/components/Card.vue";
import { useAuthStore } from "~/stores/auth";

// Validation Schema
const validationSchema = toTypedSchema(
  zod.object({
    email: zod
      .string()
      .min(1, "Email is required")
      .email("Must be a valid email"),
    password: zod
      .string()
      .min(1, "Password is required")
      .min(8, "Password must be at least 8 characters"),
  })
);
// Vee-Validate Form Setup
const { handleSubmit, errors, defineField } = useForm({
  validationSchema,
});
const [email, emailAttrs] = defineField("email");
const [password, passwordAttrs] = defineField("password");

// State
const authStore = useAuthStore();
const router = useRouter();
const isLoggingIn = ref(false);
const loginError = ref<string | null>(null);
const isSeeding = ref(false);
const seedMessage = ref<string | null>(null);
const seedError = ref(false);
const seedSummary = ref<{
  users: number;
  patients: number;
  notes: number;
} | null>(null);

// Login Handler
const handleLogin = handleSubmit(async (values) => {
  isLoggingIn.value = true;
  loginError.value = null;
  try {
    const result = await authStore.login(values.email, values.password);
    if (result.success) {
      router.push("/");
    } else {
      loginError.value = result.message || "An unknown error occurred.";
    }
  } catch (error) {
    console.error("Error during login process:", error);
    loginError.value = "An unexpected error occurred during login.";
  } finally {
    isLoggingIn.value = false;
  }
});

// Clear Login Error
const clearLoginError = () => {
  loginError.value = null;
};

// Seed Data Handler
const handleSeedData = async () => {
  isSeeding.value = true;
  seedMessage.value = null;
  seedError.value = false;
  seedSummary.value = null;

  try {
    const response = await fetch("/api/v1/debug/seed-data", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });

    const data = await response.json();

    if (
      response.ok &&
      data.status === "success" &&
      data.summary &&
      data.summary.created
    ) {
      seedMessage.value = "Demo data seeded successfully!";
      seedSummary.value = data.summary.created;
      seedError.value = false;
      setTimeout(() => {
        seedMessage.value = null;
      }, 5000);
    } else {
      const errorMessage =
        data.detail ||
        data.summary?.error ||
        "Failed to seed data or parse summary.";
      throw new Error(errorMessage);
    }
  } catch (error) {
    console.error("Error seeding data:", error);
    seedMessage.value =
      error instanceof Error
        ? error.message
        : "An unexpected error occurred during seeding.";
    seedError.value = true;
  } finally {
    isSeeding.value = false;
  }
};
</script>
