import { test, expect } from '../fixtures/base-fixture';
import { generateRandomString, isValidEmailFormat } from '../utils/test-helpers';

/**
 * Invalid Login Test Suite — Negative test scenarios for the Salesforce login page.
 *
 * Tests cover:
 *   - Wrong password with valid username
 *   - Empty username with valid password
 *   - Empty password with valid username
 *   - Both fields empty
 *   - Invalid email format in username field
 */
test.describe('Salesforce Login — Invalid Scenarios', () => {

    test('Verify error is displayed when using an incorrect password', async ({ loginPage }) => {
        await loginPage.doLogin('testuser@example.com', generateRandomString(12));
        const isErrorVisible = await loginPage.isErrorMessageDisplayed();
        expect(isErrorVisible).toBe(true);

        const errorText = await loginPage.getErrorMessage();
        expect(errorText.length).toBeGreaterThan(0);
    });

    test('Verify validation when username field is left empty', async ({ loginPage }) => {
        await loginPage.enterPassword(generateRandomString(8));
        await loginPage.clickLogin();
        const isErrorVisible = await loginPage.isErrorMessageDisplayed();
        expect(isErrorVisible).toBe(true);
    });

    test('Verify validation when password field is left empty', async ({ loginPage }) => {
        await loginPage.enterUsername('testuser@example.com');
        await loginPage.clickLogin();
        const isErrorVisible = await loginPage.isErrorMessageDisplayed();
        expect(isErrorVisible).toBe(true);
    });

    test('Verify validation when both fields are empty', async ({ loginPage }) => {
        await loginPage.clearFields();
        await loginPage.clickLogin();
        const isErrorVisible = await loginPage.isErrorMessageDisplayed();
        expect(isErrorVisible).toBe(true);
    });

    test('Verify error for invalid email format in username field', async ({ loginPage }) => {
        const invalidEmail = generateRandomString(8);
        expect(isValidEmailFormat(invalidEmail)).toBe(false);

        await loginPage.doLogin(invalidEmail, generateRandomString(8));
        const isErrorVisible = await loginPage.isErrorMessageDisplayed();
        expect(isErrorVisible).toBe(true);
    });

});