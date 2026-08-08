import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright configuration for the enterprise Salesforce login test framework.
 * Supports multi-browser execution, auto-screenshot on failure, and trace retention.
 */
export default defineConfig({
    testDir: './src/tests',
    fullyParallel: true,
    forbidOnly: !!process.env.CI,
    retries: process.env.CI ? 2 : 0,
    workers: process.env.CI ? 1 : undefined,
    reporter: [
        ['html', { open: 'never' }],
        ['list'],
    ],
    use: {
        baseURL: process.env.BASE_URL || 'https://login.salesforce.com/?locale=in',
        screenshot: 'only-on-failure',
        trace: 'retain-on-failure',
    },
    timeout: 30000,
    expect: {
        timeout: 10000,
    },
    projects: [
        {
            name: 'chromium',
            use: { ...devices['Desktop Chrome'] },
        },
        {
            name: 'firefox',
            use: { ...devices['Desktop Firefox'] },
        },
        {
            name: 'webkit',
            use: { ...devices['Desktop Safari'] },
        },
    ],
});