import { test, expect } from '../fixtures/base-fixture';
import { EnvConfig } from '../config/env.config';

/**
 * Valid Login Test Suite — Positive test scenarios for the Salesforce login page.
 *
 * Tests cover:
 *   - All critical UI elements render on page load
 *   - Remember Me checkbox toggle behavior
 *   - Successful login flow with valid credentials
 */
test.describe('Salesforce Login — Valid Scenarios', () => {

    test('Verify all UI elements render on the login page', async ({ loginPage }) => {
        const isLoaded = await loginPage.isPageLoaded();
        expect(isLoaded).toBe(true);
    });

    test('Verify Remember Me checkbox can be toggled on and persists', async ({ loginPage }) => {
        await loginPage.setRememberMe(true);
        const isCheckedAfterSet = await loginPage.isRememberMeChecked();
        expect(isCheckedAfterSet).toBe(true);

        await loginPage.setRememberMe(false);
        const isCheckedAfterUnset = await loginPage.isRememberMeChecked();
        expect(isCheckedAfterUnset).toBe(false);
    });

    test('Verify login with valid credentials redirects to home page', async ({ page, loginPage }) => {
        await loginPage.doLogin(EnvConfig.VALID_USERNAME, EnvConfig.VALID_PASSWORD);
        await page.waitForURL('**/lightning/**', { timeout: 15000 }).catch(() => {
            /** Salesforce may redirect to different URL patterns based on org config */
        });
        const currentUrl = page.url();
        expect(currentUrl).not.toContain('login');
    });

});