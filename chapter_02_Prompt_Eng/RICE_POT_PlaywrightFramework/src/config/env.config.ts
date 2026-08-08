/**
 * Environment configuration for the Salesforce login test framework.
 * All values are sourced from environment variables with secure fallback defaults.
 * Credentials should NEVER be hardcoded — provide via process.env in CI or a .env file locally.
 */
export const EnvConfig = {
    BASE_URL: process.env.BASE_URL || 'https://login.salesforce.com/?locale=in',
    VALID_USERNAME: process.env.SF_USERNAME || 'PLACEHOLDER_USERNAME',
    VALID_PASSWORD: process.env.SF_PASSWORD || 'PLACEHOLDER_PASSWORD',
    TIMEOUT: parseInt(process.env.TEST_TIMEOUT || '30000', 10),
    NAVIGATION_TIMEOUT: parseInt(process.env.NAVIGATION_TIMEOUT || '15000', 10),
} as const;