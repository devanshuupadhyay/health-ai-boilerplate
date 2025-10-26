// frontend/cypress/e2e/rpa-workflow.cy.ts

describe('RPA Workflow Simulation', () => {
  const testEmail = 'test@example.com';
  const testPassword = 'password123';
  // Add a timestamp to note content to make it unique for each run
  const noteContent = `Patient feeling well today. No acute complaints. Follow up in 3 months. ${new Date().toISOString()}`;

  const showDemoToast = (message: string) => {
    // This function is now called throughout the test
    cy.window().invoke('showDemoToast', message);
  };

  beforeEach(() => {
    cy.viewport(1200, 800);
    cy.log('Starting RPA workflow...');
  });

  it('should complete the standard clinical note workflow', () => {
    // --- 0. Visit Login Page and Seed Data ---
    cy.log('Step 0: Visiting Login Page');
    cy.visit('/login');
    cy.wait(2000); // Wait for hydration
    showDemoToast('Step 0: On login page');

    //cy.log('Step 0a: Setting up API intercept for seeding');
    //cy.intercept('POST', '/api/v1/debug/seed-data').as('seedDataRequest');

    //cy.log('Step 0b: Clicking Seed Demo Data');
    // Find the button by its text content
    //cy.contains('button', 'Seed Demo Data').click();
    //showDemoToast('Step 0b: Seeding database...');

    //cy.log('Step 0c: Waiting for seeding API call to complete');
    //cy.wait('@seedDataRequest', { timeout: 60000 }).its('response.statusCode').should('eq', 200); // Increased timeout for seeding
    //showDemoToast('Step 0c: Seeding complete!');
    //cy.wait(2000); // Demo wait

    // --- 1. Login (Now that data is seeded) ---
    cy.log('Step 1: Starting Login');
    showDemoToast('Step 1: Starting Login');

    cy.log('Step 1a: Setting up API intercept for login');
    cy.intercept('POST', '/api/v1/auth/token').as('loginRequest');
    cy.wait(2000);
    cy.log('Step 1b: Typing email');
    cy.get('#email').type(testEmail).blur();
    showDemoToast('Step 1b: Typing email');
    cy.wait(2000); // Demo wait

    cy.log('Step 1c: Typing password');
    cy.get('#password').type(testPassword).blur();
    showDemoToast('Step 1c: Typing password');
    cy.wait(2000); // Demo wait

    cy.log('Step 1d: Clicking Sign In');
    cy.get('button[type="submit"]').click();
    showDemoToast('Step 1d: Clicking Sign In');

    // --- 2. Verify Login ---
    cy.log('Step 2: Waiting for login API call to complete');
    cy.wait('@loginRequest').its('response.statusCode').should('eq', 200);

    cy.log('Step 2a: Verifying navigation to index page');
    cy.contains('h1', 'Welcome', { timeout: 20000 }).should('be.visible');
    showDemoToast('Step 2a: Login successful!');
    cy.log('Successfully logged in and redirected.');
    cy.wait(2000); // Demo wait to show Welcome screen

    cy.log('Toggling theme to light mode');
    cy.get('nav').find('svg.text-yellow-500').click();
    cy.get('html').should('not.have.class', 'dark'); // Verify light mode
    showDemoToast('Toggled light mode');
    cy.log('Theme changed to light.');
    cy.wait(2000); // Demo wait

    cy.log('Toggling theme back to dark mode');
    cy.get('nav').find('svg.text-gray-400').click();
    cy.get('html').should('have.class', 'dark'); // Verify dark mode
    showDemoToast('Toggled dark mode');
    cy.log('Theme changed back to dark.');
    cy.wait(2000); // Demo wait

    // --- 3. Navigate to Patients page ---
    cy.log('Step 3: Navigating to Patients page');
    cy.intercept('GET', '/api/v1/patients/').as('getPatients');
    cy.get('nav').contains('a', 'Patients').click();

    cy.wait('@getPatients');
    cy.contains('h1', 'Patient Dashboard', { timeout: 20000 }).should(
      'be.visible'
    );
    showDemoToast('Step 3: Navigated to Patient Dashboard');
    cy.log('Navigated to Patients page.');
    cy.wait(2000); // Demo wait

    cy.log('Toggling theme to light mode');
    cy.get('nav').find('svg.text-yellow-500').click();
    cy.get('html').should('not.have.class', 'dark');
    showDemoToast('Toggled light mode');
    cy.log('Theme changed to light.');
    cy.wait(2000); // Demo wait

    cy.log('Toggling theme back to dark mode');
    cy.get('nav').find('svg.text-gray-400').click();
    cy.get('html').should('have.class', 'dark');
    showDemoToast('Toggled dark mode');
    cy.log('Theme changed back to dark.');
    cy.wait(2000); // Demo wait

    // --- 4. Select First Patient ---
    cy.log('Step 4: Selecting the first patient in the list');
    cy.intercept('GET', '/api/v1/patients/*').as('getPatientDetails');
    cy.intercept('GET', '/api/v1/notes/patient/*').as('getNotes');

    cy.get('ul > li a').first().click();

    cy.log('Step 4a: Verifying navigation to patient details');
    cy.wait(['@getPatientDetails', '@getNotes']);
    cy.contains('h1', 'Patient Details', { timeout: 20000 }).should(
      'be.visible'
    );
    showDemoToast('Step 4a: Loading patient details');
    cy.log('Navigated to Patient details page.');
    cy.wait(2000); // Demo wait

    cy.log('Toggling theme to light mode');
    cy.get('nav').find('svg.text-yellow-500').click();
    cy.get('html').should('not.have.class', 'dark');
    showDemoToast('Toggled light mode');
    cy.log('Theme changed to light.');
    cy.wait(2000); // Demo wait

    cy.log('Toggling theme back to dark mode');
    cy.get('nav').find('svg.text-gray-400').click();
    cy.get('html').should('have.class', 'dark');
    showDemoToast('Toggled dark mode');
    cy.log('Theme changed back to dark.');
    cy.wait(2000); // Demo wait

    // --- 5. Create a Note ---
    cy.log('Step 5: Typing a new clinical note');
    cy.intercept('POST', '/api/v1/notes/').as('createNote');

    cy.get('textarea#newNote').type(noteContent).blur();
    showDemoToast('Step 5: Typing new clinical note');
    cy.wait(2000); // Demo wait

    cy.log('Step 5a: Clicking Add Note button');
    cy.contains('button', 'Add Note').click();
    showDemoToast('Step 5a: Saving note...');

    cy.wait('@createNote').its('response.statusCode').should('eq', 200);
    cy.wait('@getNotes'); // Wait for the first (immediate) refresh

    // --- 6. Wait for Summary (and note to appear) ---
    cy.log('Step 6: Waiting for note to appear...');
    cy.contains('p', noteContent, { timeout: 60000 }).should('be.visible');
    showDemoToast('Step 6: Note saved. Generating summary...');
    cy.wait(2000); // Demo wait

    cy.log('Step 6a: Waiting for summary generation...');
    // We might need multiple @getNotes waits depending on polling interval vs summary time
    cy.wait('@getNotes', { timeout: 60000 }); // Wait for summary refresh (adjust timeout if needed)
    cy.wait(5000); // Extra wait just in case polling is slow
    cy.wait('@getNotes', { timeout: 60000 }); // Second wait for summary refresh

    cy.contains('li', noteContent)
      .find('p:contains("AI Summary:")')
      .should('not.contain', 'Summary is being generated...', { timeout: 20000 }); // Check summary text within timeout
    showDemoToast('Step 6a: AI Summary complete!');
    cy.log('Note and summary verified.');
    cy.wait(2000); // Demo wait

    cy.log('Toggling theme to light mode');
    cy.get('nav').find('svg.text-yellow-500').click();
    cy.get('html').should('not.have.class', 'dark');
    showDemoToast('Toggled light mode');
    cy.log('Theme changed to light.');
    cy.wait(2000); // Demo wait

    cy.log('Toggling theme back to dark mode');
    cy.get('nav').find('svg.text-gray-400').click();
    cy.get('html').should('have.class', 'dark');
    showDemoToast('Toggled dark mode');
    cy.log('Theme changed back to dark.');
    cy.wait(2000); // Demo wait

    // --- 7. Go to Search Note ---
    cy.log('Step 7: Navigating back to Patient Dashboard for search');
    cy.get('nav').contains('a', 'Patients').click();
    cy.get('#noteSearch', { timeout: 20000 }).should('be.visible');
    showDemoToast('Step 7: Back to Patient Dashboard');
    cy.log('Navigated back to Patients page.');
    cy.wait(2000); // Demo wait

    cy.log('Step 7a: Typing search query');
    const uniqueSearchTerm = noteContent.substring(0, 10); // Use a unique part of the note
    cy.get('#noteSearch').type(uniqueSearchTerm);
    showDemoToast(`Step 7a: Searching for "${uniqueSearchTerm}"`);
    cy.wait(2000); // Demo wait

    // --- 8. Toggle Theme ---
    cy.log('Step 8: Toggling theme to light mode');
    cy.get('nav').find('svg.text-yellow-500').click();
    cy.get('html').should('not.have.class', 'dark');
    showDemoToast('Step 8: Toggled light mode');
    cy.log('Theme changed to light.');
    cy.wait(2000); // Demo wait

    cy.log('Step 8a: Toggling theme back to dark mode');
    cy.get('nav').find('svg.text-gray-400').click();
    cy.get('html').should('have.class', 'dark');
    showDemoToast('Step 8a: Toggled dark mode');
    cy.log('Theme changed back to dark.');
    cy.wait(2000); // Demo wait

    // --- 9. Navigate to IT Admin Page ---
    cy.log('Step 9: Navigating to IT Admin page');
    cy.get('nav').contains('a', 'IT Admin').click();
    cy.url().should('include', '/admin');
    showDemoToast('Step 9: Navigating to IT Admin page');
    cy.log('Navigated to IT Admin page.');
    cy.wait(2000); // Demo wait

    // --- 10. Logout ---
    cy.log('Step 10: Logging out');
    cy.contains('button', 'Logout').click();
    showDemoToast('Step 10: Logging out...');

    cy.log('Step 10a: Verifying navigation back to login page');
    cy.url().should('include', '/login');
    cy.get('#email').should('be.visible');
    cy.wait(2000); // Demo wait
    showDemoToast('RPA workflow finished.');
    cy.log('RPA workflow finished.');
  });
});