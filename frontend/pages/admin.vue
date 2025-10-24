<template>
  <div class="p-8 w-full max-w-4xl mx-auto"> <h1 class="text-3xl font-bold mb-6">Admin Dashboard & Tools</h1>
    <p class="mb-8 text-soft dark:text-dark-soft">
      Quick links to access the various services and dashboards running locally for this boilerplate.
    </p>

    <div class="space-y-4">
      <Card class="p-4">
        <h2 class="text-xl font-semibold mb-2">Observability</h2>
        <ul class="list-disc list-inside space-y-1">
          <li>
            <a href="http://localhost:3001" target="_blank" rel="noopener noreferrer" class="text-accent dark:text-dark-accent hover:underline">
              Grafana Dashboard (Logs & Metrics)
            </a>
            <span class="text-sm text-soft dark:text-dark-soft"> - View logs and performance metrics. (Login: admin/admin)</span>
          </li>
          <li>
            <a href="http://localhost:9090/targets" target="_blank" rel="noopener noreferrer" class="text-accent dark:text-dark-accent hover:underline">
              Prometheus Targets
            </a>
            <span class="text-sm text-soft dark:text-dark-soft"> - Check metric scraping status.</span>
          </li>
           <li>
             <a href="http://localhost:8008/metrics" target="_blank" rel="noopener noreferrer" class="text-accent dark:text-dark-accent hover:underline">
               Backend Metrics Endpoint
             </a>
             <span class="text-sm text-soft dark:text-dark-soft"> - See raw Prometheus metrics from FastAPI.</span>
          </li>
          <li>
            <a href="https://sentry.io/" target="_blank" rel="noopener noreferrer" class="text-accent dark:text-dark-accent hover:underline">
              Sentry Dashboard
            </a>
            <span class="text-sm text-soft dark:text-dark-soft"> - View captured application errors. (Login required)</span>
          </li>
          </ul>
      </Card>

      <Card class="p-4">
        <h2 class="text-xl font-semibold mb-2">Backend & Data</h2>
        <ul class="list-disc list-inside space-y-1">
          <li>
            <a href="http://localhost:8008/docs" target="_blank" rel="noopener noreferrer" class="text-accent dark:text-dark-accent hover:underline">
              Backend API Docs (Swagger UI)
            </a>
            <span class="text-sm text-soft dark:text-dark-soft"> - Test API endpoints.</span>
          </li>
          <li>
            <a href="http://localhost:7700" target="_blank" rel="noopener noreferrer" class="text-accent dark:text-dark-accent hover:underline">
              Meilisearch (API Endpoint)
            </a>
            <span class="text-sm text-soft dark:text-dark-soft"> - No built-in UI, but API is accessible. (Key: Use Master Key from .env for testing)</span>
          </li>
          <li>
            <span class="text-soft dark:text-dark-soft">(Database access requires a separate client like pgAdmin or DBeaver on port 5432)</span>
          </li>
          <li>
            <span class="text-soft dark:text-dark-soft">(Redis access requires a separate client like RedisInsight on port 6379)</span>
          </li>
        </ul>
      </Card>

    </div>
  </div>
</template>

<script setup lang="ts">
import Card from '~/components/Card.vue'; // Import Card component

// Protect this page with authentication middleware
definePageMeta({
  middleware: ['auth']
})

// No specific script logic needed for this page yet
</script>

<style scoped>
/* Add any page-specific styles if needed */
li a {
  font-weight: 500;
}
</style>