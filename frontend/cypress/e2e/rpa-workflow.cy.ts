// frontend/cypress/e2e/rpa-workflow.cy.ts

describe('RPA Workflow Simulation', () => {
  const testEmail = 'test@example.com';
  const testPassword = 'password123';
  // Add a timestamp to note content to make it unique for each run
  const noteContent = `Patient feeling well today. No acute complaints. Follow up in 3 months. ${new Date().toISOString()}`;

  beforeEach(() => {
    cy.viewport(1200, 800);
    cy.log('Starting RPA workflow...');
  });

  it('should complete the standard clinical note workflow', () => {
    // --- 1. Login ---
    cy.log('Step 1: Visiting Login Page');
    cy.visit('/login');

    cy.log('Toggling theme to light mode');
    // We start in dark mode, so find the SunIcon (yellow) and click its parent button
    cy.get('nav').find('svg.text-yellow-500').click();
    cy.get('html').should('not.have.class', 'dark'); // Verify light mode
    cy.log('Theme changed to light.');
    cy.wait(1000); // Demo wait

    cy.log('SToggling theme back to dark mode');
    // Now we're in light mode, so find the MoonIcon (gray) and click it
    cy.get('nav').find('svg.text-gray-400').click();
    cy.get('html').should('have.class', 'dark'); // Verify dark mode
    cy.log('Theme changed back to dark.');
    cy.wait(1000); // Demo wait

    cy.log('Step 1a: Setting up API intercept');
    cy.intercept('POST', '/api/v1/auth/token').as('loginRequest');

    cy.log('Step 1b: Typing email');
    cy.get('#email').type(testEmail).blur(); 

    cy.log('Step 1c: Typing password');
    cy.get('#password').type(testPassword).blur();

    cy.log('Step 1d: Clicking Sign In');
    cy.get('button[type="submit"]').click();


    // --- 2. Verify Login ---
    cy.log('Step 2: Waiting for login API call to complete');
    cy.wait('@loginRequest').its('response.statusCode').should('eq', 200);

    cy.log('Step 2a: Verifying navigation to index page');
    cy.contains('h1', 'Welcome', { timeout: 20000 }).should('be.visible');
    cy.log('Successfully logged in and redirected.');
    cy.wait(1000); // Demo wait to show Welcome screen

    cy.log('Toggling theme to light mode');
    // We start in dark mode, so find the SunIcon (yellow) and click its parent button
    cy.get('nav').find('svg.text-yellow-500').click();
    cy.get('html').should('not.have.class', 'dark'); // Verify light mode
    cy.log('Theme changed to light.');
    cy.wait(1000); // Demo wait

    cy.log('SToggling theme back to dark mode');
    // Now we're in light mode, so find the MoonIcon (gray) and click it
    cy.get('nav').find('svg.text-gray-400').click();
    cy.get('html').should('have.class', 'dark'); // Verify dark mode
    cy.log('Theme changed back to dark.');
    cy.wait(1000); // Demo wait

    // --- 3. Navigate to Patients page ---
    cy.log('Step 3: Navigating to Patients page');
    cy.intercept('GET', '/api/v1/patients/').as('getPatients');
    cy.get('nav').contains('a', 'Patients').click();

    // **RELIABLE WAIT:** Wait for the API call to finish
    cy.wait('@getPatients'); 
    cy.contains('h1', 'Patient Dashboard', { timeout: 20000 }).should('be.visible');
    cy.log('Navigated to Patients page.');
    cy.wait(1000); // Demo wait to show Welcome screen

    cy.log('Toggling theme to light mode');
    // We start in dark mode, so find the SunIcon (yellow) and click its parent button
    cy.get('nav').find('svg.text-yellow-500').click();
    cy.get('html').should('not.have.class', 'dark'); // Verify light mode
    cy.log('Theme changed to light.');
    cy.wait(1000); // Demo wait

    cy.log('SToggling theme back to dark mode');
    // Now we're in light mode, so find the MoonIcon (gray) and click it
    cy.get('nav').find('svg.text-gray-400').click();
    cy.get('html').should('have.class', 'dark'); // Verify dark mode
    cy.log('Theme changed back to dark.');
    cy.wait(1000); // Demo wait

    // --- 4. Select First Patient ---
    cy.log('Step 4: Selecting the first patient in the list');
    cy.intercept('GET', '/api/v1/patients/*').as('getPatientDetails');
    cy.intercept('GET', '/api/v1/notes/patient/*').as('getNotes');
    
    cy.get('ul > li a')
      .first()
      .click();

    cy.log('Step 4a: Verifying navigation to patient details');
    // **RELIABLE WAIT:** Wait for patient data to load
    cy.wait(['@getPatientDetails', '@getNotes']);
    cy.contains('h1', 'Patient Details', { timeout: 20000 }).should('be.visible');
    cy.log('Navigated to Patient details page.');
    cy.wait(1000); // Demo wait to show Welcome screen

    cy.log('Toggling theme to light mode');
    // We start in dark mode, so find the SunIcon (yellow) and click its parent button
    cy.get('nav').find('svg.text-yellow-500').click();
    cy.get('html').should('not.have.class', 'dark'); // Verify light mode
    cy.log('Theme changed to light.');
    cy.wait(1000); // Demo wait

    cy.log('SToggling theme back to dark mode');
    // Now we're in light mode, so find the MoonIcon (gray) and click it
    cy.get('nav').find('svg.text-gray-400').click();
    cy.get('html').should('have.class', 'dark'); // Verify dark mode
    cy.log('Theme changed back to dark.');
    cy.wait(1000); // Demo wait

    // --- 5. Create a Note ---
    cy.log('Step 5: Typing a new clinical note');
    cy.intercept('POST', '/api/v1/notes/').as('createNote');
    
    cy.get('textarea#newNote').type(noteContent).blur();

    cy.log('Step 5a: Clicking Add Note button');
    cy.contains('button', 'Add Note').click();

    // **RELIABLE WAIT:** Wait for the note to be created
    cy.wait('@createNote').its('response.statusCode').should('eq', 200);
    cy.wait('@getNotes'); // Wait for the first (immediate) refresh

    // --- 6. Wait for Summary (and note to appear) ---
    cy.log('Step 6: Waiting for note to appear...');
    cy.contains('p', noteContent, { timeout: 20000 }).should('be.visible');


    cy.log('Step 6a: Waiting for summary generation...');
    // **RELIABLE WAIT:** Wait for the second (delayed) summary refresh
    cy.wait('@getNotes', { timeout: 20000 }); // Wait up to 10s for the 5s timer
    
    cy.contains('li', noteContent) // Find the specific note
      .find('p:contains("AI Summary:")') // Find its summary
      .should('not.contain', 'Summary is being generated...'); // Assert text changed
    cy.log('Note and summary verified.');
    cy.wait(1000); // Demo wait to show Welcome screen

    cy.log('Toggling theme to light mode');
    // We start in dark mode, so find the SunIcon (yellow) and click its parent button
    cy.get('nav').find('svg.text-yellow-500').click();
    cy.get('html').should('not.have.class', 'dark'); // Verify light mode
    cy.log('Theme changed to light.');
    cy.wait(1000); // Demo wait

    cy.log('SToggling theme back to dark mode');
    // Now we're in light mode, so find the MoonIcon (gray) and click it
    cy.get('nav').find('svg.text-gray-400').click();
    cy.get('html').should('have.class', 'dark'); // Verify dark mode
    cy.log('Theme changed back to dark.');
    cy.wait(1000); // Demo wait

    // --- 8. Go to Search Note ---
    cy.log('Step 8: Navigating back to Patient Dashboard for search');
    cy.get('nav').contains('a', 'Patients').click();
    cy.get('#noteSearch', { timeout: 20000 }).should('be.visible');
    cy.log('Navigated back to Patients page.');
    cy.wait(1000); // Demo wait before searching

    cy.log('Step 8a: Typing search query');
    // Using the dynamic term to ensure we find the note we just made
    const uniqueSearchTerm = "feeling"; 
    cy.get('#noteSearch').type(uniqueSearchTerm);
    cy.wait(1000); // Demo wait to show query

    // --- 8. Toggle Theme ---
    cy.log('Step 8: Toggling theme to light mode');
    // We start in dark mode, so find the SunIcon (yellow) and click its parent button
    cy.get('nav').find('svg.text-yellow-500').click();
    cy.get('html').should('not.have.class', 'dark'); // Verify light mode
    cy.log('Theme changed to light.');
    cy.wait(1000); // Demo wait

    cy.log('Step 8a: Toggling theme back to dark mode');
    // Now we're in light mode, so find the MoonIcon (gray) and click it
    cy.get('nav').find('svg.text-gray-400').click();
    cy.get('html').should('have.class', 'dark'); // Verify dark mode
    cy.log('Theme changed back to dark.');
    cy.wait(1000); // Demo wait

    // --- 8. Navigate to IT Admin Page ---
    cy.log('Step 8: Navigating to IT Admin page');
    cy.get('nav').contains('a', 'IT Admin').click();
    cy.url().should('include', '/admin');
    cy.log('Navigated to IT Admin page.');
    cy.wait(2000); // Demo wait to show admin page

    // --- 9. Logout ---
    cy.log('Step 9: Logging out');
    cy.contains('button', 'Logout').click();

    cy.log('Step 9a: Verifying navigation back to login page');
    cy.url().should('include', '/login');
    cy.get('#email').should('be.visible');
    cy.wait(1000); // Demo wait to show logged-out screen
    cy.log('RPA workflow finished.');
  });
});