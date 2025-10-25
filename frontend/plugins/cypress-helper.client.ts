// frontend/plugins/cypress-helper.client.ts

export default defineNuxtPlugin(() => {
  // This code only runs on the client AND when Cypress is in control
  if (process.client && (window as any).Cypress) {
    const { show } = useDemoToaster();

    // Attach our 'show' function to the window,
    // so Cypress can call it.
    (window as any).showDemoToast = (message: string) => {
      show(message);
    };
    
    console.log('✅ Cypress helper attached to window');
  }
});