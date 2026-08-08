/**
 * Reusable test utility functions for the Salesforce login automation framework.
 * Provides helper methods for random string generation, email validation, and common test actions.
 */

/**
 * Generates a random alphanumeric string of the specified length.
 * Useful for creating dynamic test data like invalid usernames or passwords.
 * @param length - The desired length of the generated string (default: 10)
 */
export function generateRandomString(length: number = 10): string {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

/**
 * Validates whether a given string conforms to a basic email format.
 * This is a simple regex-based check and does not verify domain existence.
 * @param email - The email string to validate
 */
export function isValidEmailFormat(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Pauses execution for a fixed number of milliseconds.
 * NOTE: Prefer Playwright auto-waiting in tests. Use this only for controlled timing scenarios
 * like waiting for animations to complete or for debugging purposes during development.
 * @param ms - Number of milliseconds to pause
 */
export async function controlledPause(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
}