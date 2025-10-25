import { defineConfig } from 'cypress'

export default defineConfig({
  env: {
    CYPRESS_RUNNING: 'true'
  },
  e2e: {
    viewportWidth: 1920,
    viewportHeight: 1080,
    baseUrl: 'http://localhost:3000',
    chromeWebSecurity: false, 
    setupNodeEvents(on, config) {
      on('before:browser:launch', (browser, launchOptions) => {
        // This targets Chrome and other Chromium-based browsers
        if (browser.family === 'chromium') {
          launchOptions.preferences.default['credentials_enable_service'] = false
          launchOptions.preferences.default['profile.password_manager_enabled'] =
            false
        }

        return launchOptions
      })
    },
  },
})