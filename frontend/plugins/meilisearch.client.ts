// path: frontend/plugins/meilisearch.client.ts
import { Meilisearch } from 'meilisearch'

export default defineNuxtPlugin(() => {
  console.log("Meilisearch plugin executing..."); // Keep this log

  // --- CODE IS NOW UNCOMMENTED ---
  const config = useRuntimeConfig()
  const hostUrl = config.public.meiliHost as string;
  const apiKey = config.public.meiliKey as string;

  let meiliClient: Meilisearch | null = null; // Initialize as null

  if (!hostUrl || !apiKey) {
    console.error('Meilisearch host URL or API Key is not configured correctly in runtimeConfig.public.');
    // Keep meiliClient as null
  } else {
    try {
      // Try to initialize the client
      meiliClient = new Meilisearch({
        host: hostUrl,
        apiKey: apiKey,
      });
      console.log('Meilisearch client initialized successfully.'); // Log for success
    } catch (error) {
      // If initialization fails, keep meiliClient as null
      console.error('Failed to initialize Meilisearch client:', error);
      meiliClient = null; // Ensure it's null on error
    }
  }
  // --- END UNCOMMENTED CODE ---

  // Provide the client instance (which might be null)
  return {
    provide: {
      meili: meiliClient
    }
  } as const;
})