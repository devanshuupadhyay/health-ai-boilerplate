<template>
  <div class="w-full max-w-sm">
    <Card class="p-8">
      <form @submit="handleLogin">
        <div class="mb-4">
          <label for="email" class="form-label">Email</label>
          <input
            v-model="email"
            v-bind="emailAttrs"
            @input="clearLoginError" type="email"
            id="email"
            name="email"
            class="form-input"
            :class="{ 'invalid': errors.email }"  />
          <p v-if="errors.email" class="form-error-message">{{ errors.email }}</p>
        </div>
        <div class="mb-6">
          <label for="password" class="form-label">Password</label>
          <input
            v-model="password"
            v-bind="passwordAttrs"
            @input="clearLoginError" type="password"
            id="password"
            name="password"
            class="form-input"
            :class="{ 'invalid': errors.password }" />
          <p v-if="errors.password" class="form-error-message">{{ errors.password }}</p>
        </div>

        <p v-if="loginError" class="form-error-message mb-4 text-center">{{ loginError }}</p>
        <div class="flex items-center justify-between">
          <button
            type="submit"
            class="btn-primary"
          >
            Sign In
          </button>
        </div>
      </form>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from '#imports';
import { useAuthStore } from '~/stores/auth';
import Card from '~/components/Card.vue';
import { useForm } from 'vee-validate';
import * as zod from 'zod'; // Import Zod
import { toTypedSchema } from '@vee-validate/zod'; // Zod adapter

// --- DEFINE VALIDATION SCHEMA ---
const validationSchema = toTypedSchema(
  zod.object({
    email: zod.string().min(1, 'Email is required').email('Must be a valid email'),
    password: zod.string().min(1, 'Password is required').min(8, 'Password must be at least 8 characters'),
  })
);
// --- SETUP VEE-VALIDATE FORM ---
const { handleSubmit, errors, defineField } = useForm({
  validationSchema,
});

// Use defineField for email and password refs
const [email, emailAttrs] = defineField('email');
const [password, passwordAttrs] = defineField('password');

const authStore = useAuthStore();
const router = useRouter();
const loginError = ref<string | null>(null);

const handleLogin = handleSubmit(async (values) => {
  loginError.value = null; // Clear previous error

  let result: { success: boolean; message: string | null };

  try {
    result = await authStore.login(values.email, values.password);

    if (result.success) {
      router.push('/');
    } else {
      console.error("Login attempt failed:", result.message);
      loginError.value = result.message || 'An unknown error occurred.';
      console.log('loginError ref was set to:', loginError.value);
    }
  } catch (error) {
    console.error("Error during login process:", error);
    loginError.value = 'An unexpected error occurred during login.';
     console.log('loginError ref was set after catch:', loginError.value);
  }
});

const clearLoginError = () => {
  loginError.value = null;
}
</script>