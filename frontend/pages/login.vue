<template>
  <div class="w-full max-w-sm">
    <Card class="p-8">
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label for="email" class="form-label">Email</label>
          <input
            v-model="email"
            type="email"
            id="email"
            name="email"
            class="form-input"
          />
        </div>
        <div class="mb-6">
          <label for="password" class="form-label">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            name="password"
            class="form-input"
          />
        </div>
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

const email = ref('');
const password = ref('');
const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  const success = await authStore.login(email.value, password.value);
  if (success) {
    router.push('/');
  }
};
</script>