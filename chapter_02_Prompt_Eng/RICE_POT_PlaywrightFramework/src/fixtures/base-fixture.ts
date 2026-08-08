import { test as base, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { EnvConfig } from '../config/env.config';

/**
 * Extended Playwright test fixture providing a pre-configured LoginPage instance.
 * Automatically navigates to the Salesforce login URL before each test and
 * performs cleanup after each test. This eliminates repetitive setup code
 * across all test spec files.
 */
export const test = base.extend<{ loginPage: LoginPage }>({
    loginPage: async ({ page }, use) => {
        const loginPage = new LoginPage(page);
        await use(loginPage);
    },
});

test.beforeEach(async ({ page }) => {
    await page.goto(EnvConfig.BASE_URL, { waitUntil: 'networkidle' });
    await page.waitForLoadState('domcontentloaded');
});

test.afterEach(async ({ page }) => {
    await page.close();
});

export { expect };